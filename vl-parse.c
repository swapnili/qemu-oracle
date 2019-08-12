/*
 * Copyright (c) 2003-2008 Fabrice Bellard
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include "qemu/osdep.h"
#include "qemu/units.h"
#include "qapi/error.h"
#include "qemu/cutils.h"
#include "qemu/error-report.h"
#include "hw/qdev.h"
#include "monitor/qdev.h"
#include "sysemu/sysemu.h"
#include "qemu/option.h"
#include "qemu-options.h"
#include "sysemu/blockdev.h"

#include "chardev/char.h"
#include "monitor/monitor.h"
#include "qemu/config-file.h"

#include "sysemu/arch_init.h"

#include "vl.h"

/***********************************************************/
/* QEMU Block devices */

static const QEMUOption qemu_options[] = {
    { "h", 0, QEMU_OPTION_h, QEMU_ARCH_ALL },
#define QEMU_OPTIONS_GENERATE_OPTIONS
#include "qemu-options-wrapper.h"
    { NULL },
};

const QEMUOption *lookup_opt(int argc, char **argv,
                                    const char **poptarg, int *poptind)
{
    const QEMUOption *popt;
    int optind = *poptind;
    char *r = argv[optind];
    const char *optarg;

    loc_set_cmdline(argv, optind, 1);
    optind++;
    /* Treat --foo the same as -foo.  */
    if (r[1] == '-') {
        r++;
    }
    popt = qemu_options;
    if (!popt) {
        error_report("No valide qemu_options");
    }
    for (;;) {
        if (!popt->name) {
            error_report("invalid option*");
            exit(1);
            popt++;
            continue;
        }
        if (!strcmp(popt->name, r + 1)) {
            break;
        }
        popt++;
    }
    if (popt->flags & HAS_ARG) {
        if (optind >= argc) {
            error_report("optind %d, argc %d", optind, argc);
            error_report("requires an argument");
            exit(1);
        }
        optarg = argv[optind++];
        loc_set_cmdline(argv, optind - 2, 2);
    } else {
        optarg = NULL;
    }

    *poptarg = optarg;
    *poptind = optind;

    return popt;
}

int drive_init_func(void *opaque, QemuOpts *opts, Error **errp)
{
    BlockInterfaceType *block_default_type = opaque;

    if (!drive_new(opts, *block_default_type, errp)) {
        error_report_err(*errp);
    }

    return 0;
}

#if defined(CONFIG_MPQEMU)
int rdrive_init_func(void *opaque, QemuOpts *opts, Error **errp)
{
    DeviceState *dev;

    dev = qdev_remote_add(opts, false /* this is drive */, errp);
    if (!dev) {
        error_setg(errp, "qdev_remote_add failed for drive.");
        return -1;
    }
    object_unref(OBJECT(dev));
    return 0;
}
#endif

#if defined(CONFIG_MPQEMU)
int rdevice_init_func(void *opaque, QemuOpts *opts, Error **errp)
{
    DeviceState *dev;

    dev = qdev_remote_add(opts, true /* this is device */, errp);
    if (!dev) {
        error_setg(errp, "qdev_remote_add failed for device.");
        return -1;
    }
    return 0;
}
#endif

int device_init_func(void *opaque, QemuOpts *opts, Error **errp)
{
    DeviceState *dev;
    const char *remote = NULL;

    remote = qemu_opt_get(opts, "rid");
    if (remote) {
        return 0;
    }

    dev = qdev_device_add(opts, errp);
    if (!dev) {
        return -1;
    }
    object_unref(OBJECT(dev));
    return 0;
}

void monitor_parse(const char *optarg, const char *mode, bool pretty)
{
    static int monitor_device_index;
    QemuOpts *opts;
    const char *p;
    char label[32];

    if (strstart(optarg, "chardev:", &p)) {
        snprintf(label, sizeof(label), "%s", p);
    } else {
        snprintf(label, sizeof(label), "compat_monitor%d",
                 monitor_device_index);
        opts = qemu_chr_parse_compat(label, optarg, true);
        if (!opts) {
            error_report("parse error: %s", optarg);
            exit(1);
        }
    }

    opts = qemu_opts_create(qemu_find_opts("mon"), label, 1, &error_fatal);
    qemu_opt_set(opts, "mode", mode, &error_abort);
    qemu_opt_set(opts, "chardev", label, &error_abort);
    if (!strcmp(mode, "control")) {
        qemu_opt_set_bool(opts, "pretty", pretty, &error_abort);
    } else {
        assert(pretty == false);
    }
    monitor_device_index++;
}

int mon_init_func(void *opaque, QemuOpts *opts, Error **errp)
{
    Chardev *chr;
    bool qmp;
    bool pretty = false;
    const char *chardev;
    const char *mode;

    mode = qemu_opt_get(opts, "mode");
    if (mode == NULL) {
        mode = "readline";
    }
    if (strcmp(mode, "readline") == 0) {
        qmp = false;
    } else if (strcmp(mode, "control") == 0) {
        qmp = true;
    } else {
        error_setg(errp, "unknown monitor mode \"%s\"", mode);
        return -1;
    }

    if (!qmp && qemu_opt_get(opts, "pretty")) {
        warn_report("'pretty' is deprecated for HMP monitors, it has no effect "
                    "and will be removed in future versions");
    }
    if (qemu_opt_get_bool(opts, "pretty", 0)) {
        pretty = true;
    }

    chardev = qemu_opt_get(opts, "chardev");
    if (!chardev) {
        error_report("chardev is required");
        exit(1);
    }
    chr = qemu_chr_find(chardev);
    if (chr == NULL) {
        error_setg(errp, "chardev \"%s\" not found", chardev);
        return -1;
    }

    if (qmp) {
        monitor_init_qmp(chr, pretty);
    } else {
        monitor_init_hmp(chr, true);
    }
    return 0;
}

int chardev_init_func(void *opaque, QemuOpts *opts, Error **errp)
{
    Error *local_err = NULL;

    if (!qemu_chr_new_from_opts(opts, NULL, &local_err)) {
        if (local_err) {
            error_propagate(errp, local_err);
            return -1;
        }
        exit(0);
    }
    return 0;
}
