/*
 * QEMU monitor command handler for multi-process QEMU
 *
 * Copyright 2019, Oracle and/or its affiliates.
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

#include <sys/types.h>
#include <string.h>

#include "qemu/osdep.h"
#include "qapi/qapi-types-block-core.h"
#include "qapi/qapi-commands-block-core.h"
#include "monitor/monitor.h"
#include "qemu/option.h"
#include "hmp.h"
#include "hw/boards.h"
#include "hw/i386/pc.h"
#include "hw/proxy/qemu-proxy.h"
#include "qapi/qapi-commands-misc.h"
#include "monitor/qdev.h"
#include "qapi/qmp/qdict.h"
#include "qapi/qmp/qjson.h"
#include "qapi/qmp/qstring.h"
#include "qapi/error.h"
#include "io/proxy-link.h"
#include "sysemu/sysemu.h"

/*
 * TODO: Is there a callback where the allocated memory for QMP could be free'd
 */
RemoteProcList *qmp_query_remote(Error **errp)
{
    PCMachineState *pcms = PC_MACHINE(current_machine);
    RemoteProcList *proclist, *proc;
    GHashTableIter itr;
    PCIProxyDev *pdev;
    PCIProxyDevClass *k;
    DeviceState *d;
    char *id;

    proclist = NULL;

    g_hash_table_iter_init(&itr, pcms->remote_devs);

    while (g_hash_table_iter_next(&itr, (gpointer *)&id, (gpointer *)&pdev)) {
        k = PCI_PROXY_DEV_GET_CLASS(pdev);
        d = DEVICE(pdev);

        proc = g_malloc0(sizeof(RemoteProcList));
        proc->next = proclist;
        proclist = proc;
        proc->value = g_malloc0(sizeof(RemoteProc));
        proc->value->pid = pdev->remote_pid;
        proc->value->id = g_strdup(d->id);
        proc->value->proc = g_strdup(k->command);
    }

    return proclist;
}

void hmp_remote_proc_list(Monitor *mon, const QDict *qdict)
{
    PCMachineState *pcms = PC_MACHINE(current_machine);
    GHashTableIter itr;
    PCIProxyDev *pdev;
    PCIProxyDevClass *k;
    char *id;

    g_hash_table_iter_init(&itr, pcms->remote_devs);

    monitor_printf(mon, "%8.8s\t%16.16s\t%16.16s\t%16.16s\n\n", "PID", "RID",
                   "QEMU ID", "PROCESS NAME");

    while (g_hash_table_iter_next(&itr, (gpointer *)&id, (gpointer *)&pdev)) {
        k = PCI_PROXY_DEV_GET_CLASS(pdev);

        monitor_printf(mon, "%8.8d\t%16.16s\t%16.16s\t%16.16s\n",
                       pdev->remote_pid, pdev->rid, id, k->command);
    }
}

static PCIProxyDev *get_proxy_device(QDict *qdict, Error **errp)
{
    PCMachineState *pcms = PC_MACHINE(current_machine);
    PCIProxyDev *pdev = NULL;
    const char *rdev_id;

    if (!qdict_haskey(qdict, "rdev_id")) {
        error_setg(errp, "Please specify a value for rdev_id");
        return NULL;
    }

    rdev_id = qdict_get_str(qdict, "rdev_id");

    pdev = (PCIProxyDev *)g_hash_table_lookup(pcms->remote_devs, rdev_id);
    if (!pdev) {
        error_setg(errp,
                   "No remote device by ID %s. Use query-remote command to get remote devices",
                   rdev_id);
    }

    return pdev;
}

static void rdevice_add_del(QDict *qdict, proc_cmd_t cmd, Error **errp)
{
    PCMachineState *pcms = PC_MACHINE(current_machine);
    ProcMsg msg = {0};
    PCIProxyDev *pdev = NULL;
    const char *id;
    QString *json;
    int wait;

    pdev = get_proxy_device(qdict, errp);
    if (*errp) {
        return;
    }

    qdict_del(qdict, "rdev_id");

    id = qdict_get_str(qdict, "id");

    json = qobject_to_json(QOBJECT(qdict));

    wait = GET_REMOTE_WAIT;

    msg.cmd = cmd;
    msg.bytestream = 1;
    msg.size = strlen(qstring_get_str(json));
    msg.data2 = (uint8_t *)qstring_get_str(json);
    msg.num_fds = 1;
    msg.fds[0] = wait;

    proxy_proc_send(pdev->proxy_link, &msg);
    (void)wait_for_remote(wait);
    PUT_REMOTE_WAIT(wait);

    qstring_destroy_obj(QOBJECT(json));

    /* TODO: Only on success */
    if (cmd == DEVICE_ADD) {
        (void)g_hash_table_insert(pcms->remote_devs, (gpointer)g_strdup(id),
                                  (gpointer)pdev);
    } else {
        (void)g_hash_table_remove(pcms->remote_devs, (gpointer)id);
    }
}

void qmp_rdevice_add(QDict *qdict, QObject **ret_data, Error **errp)
{
    rdevice_add_del(qdict, DEVICE_ADD, errp);
}

void hmp_rdevice_add(Monitor *mon, const QDict *qdict)
{
    Error *err = NULL;

    /* TODO: Is it OK to modify the QDict argument from HMP? */
    rdevice_add_del((QDict *)qdict, DEVICE_ADD, &err);

    if (err) {
        monitor_printf(mon, "rdevice_add error: %s\n",
                       error_get_pretty(err));
        error_free(err);
    }
}

void qmp_rdevice_del(QDict *qdict, QObject **ret_data, Error **errp)
{
    rdevice_add_del(qdict, DEVICE_DEL, errp);
}

void hmp_rdevice_del(Monitor *mon, const QDict *qdict)
{
    Error *err = NULL;

    /* TODO: Is it OK to modify the QDict argument from HMP? */
    rdevice_add_del((QDict *)qdict, DEVICE_DEL, &err);

    if (err) {
        monitor_printf(mon, "rdevice_del error: %s\n",
                       error_get_pretty(err));
        error_free(err);
    }
}

void hmp_rdrive_add(Monitor *mon, const QDict *qdict)
{
    PCMachineState *pcms = PC_MACHINE(current_machine);
    Error *local_err = NULL;
    ProcMsg msg = {0};
    PCIProxyDev *pdev = NULL;
    const char *id, *opts;
    char *data;
    int wait;

    pdev = get_proxy_device((QDict *)qdict, &local_err);
    if (local_err) {
        monitor_printf(mon, "rdrive_add error: %s\n",
                       error_get_pretty(local_err));
        error_free(local_err);
        return;
    }

    id = qdict_get_str(qdict, "id");

    opts = qdict_get_str(qdict, "opts");

    data = g_strdup_printf("%s,id=%s", opts, id);

    wait = GET_REMOTE_WAIT;

    msg.cmd = DRIVE_ADD;
    msg.bytestream = 1;
    msg.size = strlen(data);
    msg.data2 = (uint8_t *)data;
    msg.num_fds = 1;
    msg.fds[0] = wait;

    proxy_proc_send(pdev->proxy_link, &msg);
    (void)wait_for_remote(wait);
    PUT_REMOTE_WAIT(wait);

    /* TODO: Only on success */
    (void)g_hash_table_insert(pcms->remote_devs, (gpointer)g_strdup(id),
                              (gpointer)pdev);

    g_free(data);
}

