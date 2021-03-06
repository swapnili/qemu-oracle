#include "qemu/osdep.h"
#include "qemu-common.h"

#include "migration/misc.h"
#include "migration/snapshot.h"
#include "qapi/qapi-types-migration.h"
#include "qapi/qapi-commands-migration.h"
#include "qapi/qapi-types-net.h"
#include "net/filter.h"
#include "net/colo-compare.h"

#pragma weak qmp_query_migrate_capabilities
#pragma weak qmp_query_migrate_parameters
#pragma weak migrate_announce_params
#pragma weak qmp_query_migrate
#pragma weak qmp_migrate_set_capabilities
#pragma weak qmp_migrate_set_parameters
#pragma weak qmp_migrate_incoming
#pragma weak qmp_migrate_recover
#pragma weak qmp_migrate_pause
#pragma weak qmp_migrate
#pragma weak qmp_migrate_cancel
#pragma weak qmp_migrate_continue
#pragma weak qmp_migrate_set_cache_size
#pragma weak qmp_query_migrate_cache_size
#pragma weak qmp_migrate_set_speed
#pragma weak qmp_migrate_set_downtime
#pragma weak qmp_migrate_start_postcopy
#pragma weak migration_global_dump
#pragma weak save_snapshot
#pragma weak qmp_xen_save_devices_state
#pragma weak load_snapshot
#pragma weak qmp_xen_set_replication
#pragma weak qmp_query_xen_replication_status
#pragma weak qmp_xen_colo_do_checkpoint
#pragma weak qmp_query_colo_status
#pragma weak qmp_x_colo_lost_heartbeat

MigrationInfo *qmp_query_migrate(Error **errp)
{
    qemu_debug_assert(0);

    return NULL;
}

void qmp_migrate_set_capabilities(MigrationCapabilityStatusList *params,
                                  Error **errp)
{
    qemu_debug_assert(0);
}

MigrationCapabilityStatusList *qmp_query_migrate_capabilities(Error **errp)
{
    qemu_debug_assert(0);

    return NULL;
}

void qmp_migrate_set_parameters(MigrateSetParameters *params, Error **errp)
{
    qemu_debug_assert(0);
}

MigrationParameters *qmp_query_migrate_parameters(Error **errp)
{
    qemu_debug_assert(0);

    return NULL;
}

void qmp_migrate_start_postcopy(Error **errp)
{
    qemu_debug_assert(0);
}

void qmp_migrate_cancel(Error **errp)
{
    qemu_debug_assert(0);
}

void qmp_migrate_continue(MigrationStatus state, Error **errp)
{
    qemu_debug_assert(0);
}

void qmp_migrate_set_downtime(double value, Error **errp)
{
    qemu_debug_assert(0);
}

void qmp_migrate_set_speed(int64_t value, Error **errp)
{
    qemu_debug_assert(0);
}

void qmp_migrate_set_cache_size(int64_t value, Error **errp)
{
    qemu_debug_assert(0);
}

int64_t qmp_query_migrate_cache_size(Error **errp)
{
    qemu_debug_assert(0);

    return 0;
}

void qmp_migrate(const char *uri, bool has_blk, bool blk,
                 bool has_inc, bool inc, bool has_detach, bool detach,
                 bool has_resume, bool resume, Error **errp)
{
    qemu_debug_assert(0);
}

void qmp_migrate_incoming(const char *uri, Error **errp)
{
    qemu_debug_assert(0);
}

void qmp_migrate_recover(const char *uri, Error **errp)
{
    qemu_debug_assert(0);
}

void qmp_migrate_pause(Error **errp)
{
    qemu_debug_assert(0);
}

void qmp_x_colo_lost_heartbeat(Error **errp)
{
    qemu_debug_assert(0);
}

void qmp_xen_save_devices_state(const char *filename, bool has_live, bool live,
                                Error **errp)
{
    qemu_debug_assert(0);
}

void qmp_xen_set_replication(bool enable, bool primary,
                             bool has_failover, bool failover,
                             Error **errp)
{
    qemu_debug_assert(0);
}

ReplicationStatus *qmp_query_xen_replication_status(Error **errp)
{
    qemu_debug_assert(0);

    return NULL;
}

void qmp_xen_colo_do_checkpoint(Error **errp)
{
    qemu_debug_assert(0);
}

COLOStatus *qmp_query_colo_status(Error **errp)
{
    qemu_debug_assert(0);

    return NULL;
}

void migration_global_dump(Monitor *mon)
{
    qemu_debug_assert(0);
}

int load_snapshot(const char *name, Error **errp)
{
    qemu_debug_assert(0);

    return -ENOSYS;
}

int save_snapshot(const char *name, Error **errp)
{
    qemu_debug_assert(0);

    return -ENOSYS;
}

AnnounceParameters *migrate_announce_params(void)
{
    qemu_debug_assert(0);

    return NULL;
}

void colo_notify_filters_event(int event, Error **errp)
{
    qemu_debug_assert(0);
}

void colo_notify_compares_event(void *opaque, int event, Error **errp)
{
    qemu_debug_assert(0);
}

void colo_compare_register_notifier(Notifier *notify)
{
    qemu_debug_assert(0);
}

void colo_compare_unregister_notifier(Notifier *notify)
{
    qemu_debug_assert(0);
}
