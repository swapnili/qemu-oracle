/*
 * Copyright © 2020 Oracle and/or its affiliates.
 *
 * This work is licensed under the terms of the GNU GPL-v2, version 2 or later.
 *
 * See the COPYING file in the top-level directory.
 *
 */

#include "qemu/osdep.h"
#include "qemu-common.h"

#include "hw/i386/remote.h"
#include "io/channel.h"
#include "io/mpqemu-link.h"
#include "qapi/error.h"
#include "sysemu/runstate.h"

gboolean mpqemu_process_msg(QIOChannel *ioc, GIOCondition cond,
                            gpointer opaque)
{
    PCIDevice *pci_dev = (PCIDevice *)opaque;
    Error *local_err = NULL;
    MPQemuMsg msg = { 0 };

    if (cond & G_IO_HUP) {
        qemu_system_shutdown_request(SHUTDOWN_CAUSE_GUEST_SHUTDOWN);
        return FALSE;
    }

    if (cond & (G_IO_ERR | G_IO_NVAL)) {
        error_report("Error %d while processing message from proxy"
                     "in remote process pid=%d", errno, getpid());
        return FALSE;
    }

    mpqemu_msg_recv_create_co(&msg, ioc, &local_err);
    if (local_err) {
        goto exit;
    }

    if (!mpqemu_msg_valid(&msg)) {
        error_report("Received invalid message from proxy"
                     "in remote process pid=%d", getpid());
        return FALSE;
    }

    switch (msg.cmd) {
    default:
        error_setg(&local_err,
                   "Unknown command (%d) received for device %s (pid=%d)",
                   msg.cmd, DEVICE(pci_dev)->id, getpid());
    }

    mpqemu_msg_cleanup(&msg);

exit:
    if (local_err) {
        error_report_err(local_err);
        return FALSE;
    }

    return TRUE;
}
