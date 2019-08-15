/*
 * Communication channel between QEMU and remote device process
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

#include <assert.h>
#include <errno.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>
#include <limits.h>
#include <poll.h>

#include "qemu/module.h"
#include "io/proxy-link.h"
#include "qemu/log.h"

GSourceFuncs gsrc_funcs;

static void proxy_link_inst_init(Object *obj)
{
    ProxyLinkState *s = PROXY_LINK(obj);

    s->ctx = g_main_context_default();
    s->loop = g_main_loop_new(s->ctx, FALSE);
}

static const TypeInfo proxy_link_info = {
    .name = TYPE_PROXY_LINK,
    .parent = TYPE_OBJECT,
    .instance_size = sizeof(ProxyLinkState),
    .instance_init = proxy_link_inst_init,
};

static void proxy_link_register_types(void)
{
    type_register_static(&proxy_link_info);
}

type_init(proxy_link_register_types)

ProxyLinkState *proxy_link_create(void)
{
    return PROXY_LINK(object_new(TYPE_PROXY_LINK));
}

void proxy_link_finalize(ProxyLinkState *s)
{
    g_main_loop_unref(s->loop);
    g_main_context_unref(s->ctx);
    g_main_loop_quit(s->loop);

    proxy_link_destroy_channel(s->com);

    object_unref(OBJECT(s));
}

void proxy_proc_send(ProxyLinkState *s, ProcMsg *msg, ProcChannel *chan)
{
    int rc;
    uint8_t *data, *buf = NULL;
    union {
        char control[CMSG_SPACE(REMOTE_MAX_FDS * sizeof(int))];
        struct cmsghdr align;
    } u;
    struct msghdr hdr;
    struct cmsghdr *chdr;
    int sock = chan->sock;
    QemuMutex *lock = &chan->lock;

    struct iovec iov = {
        .iov_base = (char *) msg,
        .iov_len = PROC_HDR_SIZE,
    };

    memset(&hdr, 0, sizeof(hdr));
    memset(&u, 0, sizeof(u));

    hdr.msg_iov = &iov;
    hdr.msg_iovlen = 1;

    if (msg->num_fds > REMOTE_MAX_FDS) {
        qemu_log_mask(LOG_REMOTE_DEBUG, "%s: Max FDs exceeded\n", __func__);
        return;
    }

    if (msg->num_fds > 0) {
        size_t fdsize = msg->num_fds * sizeof(int);

        hdr.msg_control = &u;
        hdr.msg_controllen = sizeof(u);

        chdr = CMSG_FIRSTHDR(&hdr);
        chdr->cmsg_len = CMSG_LEN(fdsize);
        chdr->cmsg_level = SOL_SOCKET;
        chdr->cmsg_type = SCM_RIGHTS;
        memcpy(CMSG_DATA(chdr), msg->fds, fdsize);
        hdr.msg_controllen = CMSG_SPACE(fdsize);
    }

    qemu_mutex_lock(lock);

    do {
        rc = sendmsg(sock, &hdr, 0);
    } while (rc < 0 && (errno == EINTR || errno == EAGAIN));

    if (rc < 0) {
        qemu_log_mask(LOG_REMOTE_DEBUG, "%s - sendmsg rc is %d, errno is %d,"
                      " sock %d\n", __func__, rc, errno, sock);
        qemu_mutex_unlock(lock);
        return;
    }

    if (msg->bytestream) {
        data = msg->data2;
    } else {
        data = (uint8_t *)msg + PROC_HDR_SIZE;
    }

    if (msg->size_id > 0) {
        buf = calloc(1, msg->size + msg->size_id);
        assert(buf);
        memcpy(buf, data, msg->size);
        memcpy(buf + msg->size, msg->id, msg->size_id);
        data = buf;
    }
    do {
        rc = write(sock, data, msg->size + msg->size_id);
    } while (rc < 0 && (errno == EINTR || errno == EAGAIN));

    free(buf);

    qemu_mutex_unlock(lock);
}


int proxy_proc_recv(ProxyLinkState *s, ProcMsg *msg, ProcChannel *chan)
{
    int rc;
    uint8_t *data, *buf = NULL;
    union {
        char control[CMSG_SPACE(REMOTE_MAX_FDS * sizeof(int))];
        struct cmsghdr align;
    } u;
    struct msghdr hdr;
    struct cmsghdr *chdr;
    size_t fdsize;
    int sock = chan->sock;
    QemuMutex *lock = &chan->lock;

    struct iovec iov = {
        .iov_base = (char *) msg,
        .iov_len = PROC_HDR_SIZE,
    };

    memset(&hdr, 0, sizeof(hdr));
    memset(&u, 0, sizeof(u));

    hdr.msg_iov = &iov;
    hdr.msg_iovlen = 1;
    hdr.msg_control = &u;
    hdr.msg_controllen = sizeof(u);

    qemu_mutex_lock(lock);

    do {
        rc = recvmsg(sock, &hdr, 0);
    } while (rc < 0 && (errno == EINTR || errno == EAGAIN));

    if (rc < 0) {
        qemu_log_mask(LOG_REMOTE_DEBUG, "%s - recvmsg rc is %d, errno is %d,"
                      " sock %d\n", __func__, rc, errno, sock);
        qemu_mutex_unlock(lock);
        return rc;
    }

    msg->num_fds = 0;
    for (chdr = CMSG_FIRSTHDR(&hdr); chdr != NULL;
         chdr = CMSG_NXTHDR(&hdr, chdr)) {
        if ((chdr->cmsg_level == SOL_SOCKET) &&
            (chdr->cmsg_type == SCM_RIGHTS)) {
            fdsize = chdr->cmsg_len - CMSG_LEN(0);
            msg->num_fds = fdsize / sizeof(int);
            memcpy(msg->fds, CMSG_DATA(chdr), fdsize);
            break;
        }
    }

    if (msg->size && msg->bytestream) {
        msg->data2 = calloc(1, msg->size);
        data = msg->data2;
    } else {
        data = (uint8_t *)&msg->data1;
    }

     if (msg->size) {
        if (msg->size_id > 0) {
            buf = calloc(1, msg->size + msg->size_id);
            data = buf;
        }
        do {
            rc = read(sock, data, msg->size + msg->size_id);
        } while (rc < 0 && (errno == EINTR || errno == EAGAIN));
        if (rc < 0) {
            fprintf(stderr, "Read sock is an error!\n");
            return rc;
        }
    }
    if (msg->size && msg->bytestream) {
        memcpy(msg->data2, data, msg->size);
    } else {
        memcpy((uint8_t *)&msg->data1, data, msg->size);
    }

    if (msg->size_id > 0) {
        msg->id = calloc(1, msg->size_id);
        memcpy(msg->id, data + msg->size, msg->size_id);
    }

    qemu_mutex_unlock(lock);

    return rc;
}

uint64_t wait_for_remote(int efd)
{
    struct pollfd pfd = { .fd = efd, .events = POLLIN };
    uint64_t val;
    int ret;

    ret = poll(&pfd, 1, 1000);

    switch (ret) {
    case 0:
        qemu_log_mask(LOG_REMOTE_DEBUG, "Error wait_for_remote: Timed out\n");
        /* TODO: Kick-off error recovery */
        return ULLONG_MAX;
    case -1:
        qemu_log_mask(LOG_REMOTE_DEBUG, "Poll error wait_for_remote: %s\n",
                      strerror(errno));
        return ULLONG_MAX;
    default:
        if (read(efd, &val, sizeof(val)) == -1) {
            qemu_log_mask(LOG_REMOTE_DEBUG, "Error wait_for_remote: %s\n",
                          strerror(errno));
            return ULLONG_MAX;
        }
    }

    val = (val == ULLONG_MAX) ? val : (val - 1);

    return val;
}

void notify_proxy(int efd, uint64_t val)
{
    val = (val == ULLONG_MAX) ? val : (val + 1);

    if (write(efd, &val, sizeof(val)) == -1) {
        qemu_log_mask(LOG_REMOTE_DEBUG, "Error notify_proxy: %s\n",
                      strerror(errno));
    }
}

static gboolean proxy_link_handler_prepare(GSource *gsrc, gint *timeout)
{
    g_assert(timeout);

    *timeout = -1;

    return FALSE;
}

static gboolean proxy_link_handler_check(GSource *gsrc)
{
    ProcChannel *chan = (ProcChannel *)gsrc;

    return chan->gpfd.events & chan->gpfd.revents;
}

static gboolean proxy_link_handler_dispatch(GSource *gsrc, GSourceFunc func,
                                            gpointer data)
{
    ProxyLinkState *s = (ProxyLinkState *)data;
    ProcChannel *chan = (ProcChannel *)gsrc;

    s->callback(chan->gpfd.revents, chan);

    if ((chan->gpfd.revents & G_IO_HUP) || (chan->gpfd.revents & G_IO_ERR)) {
        return G_SOURCE_REMOVE;
    }

    return G_SOURCE_CONTINUE;
}

void proxy_link_set_callback(ProxyLinkState *s, proxy_link_callback callback)
{
    s->callback = callback;
}

void proxy_link_init_channel(ProxyLinkState *s, ProcChannel **chan, int fd)
{
    ProcChannel *src;

    gsrc_funcs = (GSourceFuncs){
        .prepare = proxy_link_handler_prepare,
        .check = proxy_link_handler_check,
        .dispatch = proxy_link_handler_dispatch,
        .finalize = NULL,
    };

    src = (ProcChannel *)g_source_new(&gsrc_funcs, sizeof(ProcChannel));

    src->sock = fd;
    qemu_mutex_init(&src->lock);

    g_source_set_callback(&src->gsrc, NULL, (gpointer)s, NULL);
    src->gpfd.fd = fd;
    src->gpfd.events = G_IO_IN | G_IO_HUP | G_IO_ERR;
    g_source_add_poll(&src->gsrc, &src->gpfd);

    *chan = src;
}

void proxy_link_destroy_channel(ProcChannel *chan)
{
    g_source_unref(&chan->gsrc);
    close(chan->sock);
    qemu_mutex_destroy(&chan->lock);
}

void start_handler(ProxyLinkState *s)
{

    g_assert(g_source_attach(&s->com->gsrc, s->ctx));

    g_main_loop_run(s->loop);
}
