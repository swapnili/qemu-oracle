#ifndef MONITOR_QDEV_H
#define MONITOR_QDEV_H

#include "hw/qdev-core.h"

/*** monitor commands ***/

void hmp_info_qtree(Monitor *mon, const QDict *qdict);
void hmp_info_qdm(Monitor *mon, const QDict *qdict);
void hmp_info_qom_tree(Monitor *mon, const QDict *dict);
void qmp_device_add(QDict *qdict, QObject **ret_data, Error **errp);

#ifdef CONFIG_MPQEMU
#include "hw/proxy/qemu-proxy.h"
void qmp_rdevice_add(QDict *qdict, QObject **ret_data, Error **errp);
void qmp_rdevice_del(QDict *qdict, QObject **ret_data, Error **errp);
DeviceState *qdev_proxy_add(const char *rid, const char *id, Error **errp);
DeviceState *qdev_remote_add(QemuOpts *opts, bool device, Error **errp);
void qdev_proxy_fire(void);
#endif

int qdev_device_help(QemuOpts *opts);
DeviceState *qdev_device_add(QemuOpts *opts, Error **errp);
void qdev_set_id(DeviceState *dev, const char *id);

#endif
