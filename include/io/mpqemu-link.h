/*
 * Communication channel between QEMU and remote device process
 *
 * Copyright © 2018, 2020 Oracle and/or its affiliates.
 *
 * This work is licensed under the terms of the GNU GPL, version 2 or later.
 * See the COPYING file in the top-level directory.
 *
 */

#ifndef MPQEMU_LINK_H
#define MPQEMU_LINK_H

#include "qom/object.h"
#include "qemu/thread.h"
#include "io/channel.h"
#include "io/channel-socket.h"
#include "exec/cpu-common.h"
#include "exec/hwaddr.h"

#define REMOTE_MAX_FDS 8

#define MPQEMU_MSG_HDR_SIZE offsetof(MPQemuMsg, data1.u64)

/**
 * MPQemuCmd:
 *
 * MPQemuCmd enum type to specify the command to be executed on the remote
 * device.
 *
 * SYNC_SYSMEM      Shares QEMU's RAM with remote device's RAM
 */
typedef enum {
    INIT = 0,
    SYNC_SYSMEM,
    RET_MSG,
    PCI_CONFIG_WRITE,
    PCI_CONFIG_READ,
    BAR_WRITE,
    BAR_READ,
    SET_IRQFD,
    GET_PCI_INFO,
    PROXY_PING,
    DEVICE_RESET,
    MAX = INT_MAX,
} MPQemuCmd;

typedef struct {
    hwaddr gpas[REMOTE_MAX_FDS];
    uint64_t sizes[REMOTE_MAX_FDS];
    off_t offsets[REMOTE_MAX_FDS];
} SyncSysmemMsg;

typedef struct {
    uint32_t addr;
    uint32_t val;
    int l;
} ConfDataMsg;

typedef struct {
    hwaddr addr;
    uint64_t val;
    unsigned size;
    bool memory;
} BarAccessMsg;

/**
 * Maximum size of data2 field in the message to be transmitted.
 */
#define MPQEMU_MSG_DATA_MAX 256

/**
 * MPQemuMsg:
 * @cmd: The remote command
 * @bytestream: Indicates if the data to be shared is structured (data1)
 *              or unstructured (data2)
 * @size: Size of the data to be shared
 * @data1: Structured data
 * @fds: File descriptors to be shared with remote device
 * @data2: Unstructured data
 *
 * MPQemuMsg Format of the message sent to the remote device from QEMU.
 *
 */

typedef struct {
    int cmd;
    int bytestream;
    size_t size;

    union {
        uint64_t u64;
        SyncSysmemMsg sync_sysmem;
        BarAccessMsg bar_access;
    } data1;

    int fds[REMOTE_MAX_FDS];
    int num_fds;

    /* Max size of data2 is MPQEMU_MSG_DATA_MAX */
    uint8_t *data2;
} MPQemuMsg;

struct MPQemuRequest {
    MPQemuMsg *msg;
    QIOChannel *ioc;
    Coroutine *co;
    bool finished;
    int error;
    long ret;
};

typedef struct MPQemuRequest MPQemuRequest;

uint64_t mpqemu_msg_send_and_await_reply(MPQemuMsg *msg, QIOChannel *ioc,
                                  Error **errp);
void mpqemu_msg_send(MPQemuMsg *msg, QIOChannel *ioc, Error **errp);
void mpqemu_msg_recv(MPQemuMsg *msg, QIOChannel *ioc, Error **errp);

bool mpqemu_msg_valid(MPQemuMsg *msg);
void mpqemu_msg_cleanup(MPQemuMsg *msg);

#endif
