#include "qemu/osdep.h"
#include "qemu-common.h"

#include "hw/i386/remote.h"
#include "io/channel.h"
#include "io/mpqemu-link.h"
#include "qapi/error.h"
#include "sysemu/runstate.h"
#include "io/channel-util.h"
#include "hw/pci/pci.h"

static void process_connect_dev_msg(MPQemuMsg *msg, QIOChannel *com,
                                    Error **errp);
static void process_config_write(QIOChannel *ioc, PCIDevice *dev,
                                 MPQemuMsg *msg);
static void process_config_read(QIOChannel *ioc, PCIDevice *dev,
                                MPQemuMsg *msg);

gboolean mpqemu_process_msg(QIOChannel *ioc, GIOCondition cond,
                            gpointer opaque)
{
    DeviceState *dev = (DeviceState *)opaque;
    PCIDevice *pci_dev = PCI_DEVICE(dev);
    Error *local_err = NULL;
    MPQemuMsg msg = { 0 };

    if (cond & G_IO_HUP) {
        qemu_system_shutdown_request(SHUTDOWN_CAUSE_GUEST_SHUTDOWN);
    }

    if (cond & (G_IO_ERR | G_IO_NVAL)) {
        error_setg(&local_err, "Error %d while processing message from proxy \
                   in remote process pid=%d", errno, getpid());
        return FALSE;
    }

    if (mpqemu_msg_recv(&msg, ioc) < 0) {
        return FALSE;
    }

    if (!mpqemu_msg_valid(&msg)) {
        error_report("Received invalid message from proxy \
                     in remote process pid=%d", getpid());
        return TRUE;
    }

    switch (msg.cmd) {
    case CONNECT_DEV:
        process_connect_dev_msg(&msg, ioc, &local_err);
        break;
    case PCI_CONFIG_WRITE:
        process_config_write(ioc, pci_dev, &msg);
        break;
    case PCI_CONFIG_READ:
        process_config_read(ioc, pci_dev, &msg);
        break;
    default:
        error_setg(&local_err, "Unknown command (%d) received from proxy \
                   in remote process pid=%d", msg.cmd, getpid());
    }

    if (msg.data2) {
        free(msg.data2);
    }

    if (local_err) {
        error_report_err(local_err);
        return FALSE;
    }

    return TRUE;
}

static void process_connect_dev_msg(MPQemuMsg *msg, QIOChannel *com,
                                    Error **errp)
{
    char *devid = (char *)msg->data2;
    QIOChannel *dioc = NULL;
    DeviceState *dev = NULL;
    MPQemuMsg ret = { 0 };
    int rc = 0;

    g_assert(devid && (devid[msg->size - 1] == '\0'));

    dev = qdev_find_recursive(sysbus_get_default(), devid);
    if (!dev || !object_dynamic_cast(OBJECT(dev), TYPE_PCI_DEVICE)) {
        rc = 0xff;
        goto exit;
    }

    dioc = qio_channel_new_fd(msg->fds[0], errp);

    qio_channel_add_watch(dioc, G_IO_IN | G_IO_HUP, mpqemu_process_msg,
                          (void *)dev, NULL);

exit:
    ret.cmd = RET_MSG;
    ret.bytestream = 0;
    ret.data1.u64 = rc;
    ret.size = sizeof(ret.data1);

    mpqemu_msg_send(&ret, com);
}

static void process_config_write(QIOChannel *ioc, PCIDevice *dev,
                                 MPQemuMsg *msg)
{
    struct conf_data_msg *conf = (struct conf_data_msg *)msg->data2;
    MPQemuMsg ret = { 0 };

    if (conf->addr >= PCI_CFG_SPACE_EXP_SIZE) {
        error_report("Bad address received when writing PCI config, pid %d",
                     getpid());
        ret.data1.u64 = UINT64_MAX;
    } else {
        pci_default_write_config(dev, conf->addr, conf->val, conf->l);
    }

    ret.cmd = RET_MSG;
    ret.bytestream = 0;
    ret.size = sizeof(ret.data1);

    mpqemu_msg_send(&ret, ioc);
}

static void process_config_read(QIOChannel *ioc, PCIDevice *dev,
                                MPQemuMsg *msg)
{
    struct conf_data_msg *conf = (struct conf_data_msg *)msg->data2;
    MPQemuMsg ret = { 0 };

    if (conf->addr >= PCI_CFG_SPACE_EXP_SIZE) {
        error_report("Bad address received when reading PCI config, pid %d",
                     getpid());
        ret.data1.u64 = UINT64_MAX;
    } else {
        ret.data1.u64 = pci_default_read_config(dev, conf->addr, conf->l);
    }

    ret.cmd = RET_MSG;
    ret.bytestream = 0;
    ret.size = sizeof(ret.data1);

    mpqemu_msg_send(&ret, ioc);
}
