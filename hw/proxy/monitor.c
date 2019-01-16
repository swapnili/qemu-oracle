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

#include "qemu/osdep.h"
#include "qapi/qapi-types-block-core.h"
#include "qapi/qapi-commands-block-core.h"
#include "monitor/monitor.h"
#include "qemu/option.h"
#include "hmp.h"
#include "hw/boards.h"
#include "hw/i386/pc.h"
#include "hw/proxy/qemu-proxy.h"

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
