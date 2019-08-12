HXCOMM Use DEFHEADING() to define headings in both help text and texi
HXCOMM Text between STEXI and ETEXI are copied to texi version and
HXCOMM discarded from C version
HXCOMM DEF(command, args, callback, arg_string, help) is used to construct
HXCOMM monitor commands
HXCOMM HXCOMM can be used for comments, discarded from both texi and C

STEXI
@table @option
ETEXI

    {
        .name       = "help|?",
        .args_type  = "name:S?",
        .params     = "[cmd]",
        .help       = "show the help",
        .cmd        = do_help_cmd,
        .flags      = "p",
    },

STEXI
@item help or ? [@var{cmd}]
@findex help
Show the help for all commands or just for command @var{cmd}.
ETEXI

    {
        .name       = "q|quit",
        .args_type  = "",
        .params     = "",
        .help       = "quit the emulator",
        .cmd        = hmp_quit,
    },

STEXI
@item q or quit
@findex quit
Quit the emulator.
ETEXI

    {
        .name       = "block_resize",
        .args_type  = "device:B,size:o",
        .params     = "device size",
        .help       = "resize a block image",
        .cmd        = hmp_block_resize,
    },

STEXI
@item block_resize
@findex block_resize
Resize a block image while a guest is running.  Usually requires guest
action to see the updated size.  Resize to a lower size is supported,
but should be used with extreme caution.  Note that this command only
resizes image files, it can not resize block devices like LVM volumes.
ETEXI

    {
        .name       = "block_stream",
        .args_type  = "device:B,speed:o?,base:s?",
        .params     = "device [speed [base]]",
        .help       = "copy data from a backing file into a block device",
        .cmd        = hmp_block_stream,
    },

STEXI
@item block_stream
@findex block_stream
Copy data from a backing file into a block device.
ETEXI

    {
        .name       = "block_job_set_speed",
        .args_type  = "device:B,speed:o",
        .params     = "device speed",
        .help       = "set maximum speed for a background block operation",
        .cmd        = hmp_block_job_set_speed,
    },

STEXI
@item block_job_set_speed
@findex block_job_set_speed
Set maximum speed for a background block operation.
ETEXI

    {
        .name       = "block_job_cancel",
        .args_type  = "force:-f,device:B",
        .params     = "[-f] device",
        .help       = "stop an active background block operation (use -f"
                      "\n\t\t\t if you want to abort the operation immediately"
                      "\n\t\t\t instead of keep running until data is in sync)",
        .cmd        = hmp_block_job_cancel,
    },

STEXI
@item block_job_cancel
@findex block_job_cancel
Stop an active background block operation (streaming, mirroring).
ETEXI

    {
        .name       = "block_job_complete",
        .args_type  = "device:B",
        .params     = "device",
        .help       = "stop an active background block operation",
        .cmd        = hmp_block_job_complete,
    },

STEXI
@item block_job_complete
@findex block_job_complete
Manually trigger completion of an active background block operation.
For mirroring, this will switch the device to the destination path.
ETEXI

    {
        .name       = "block_job_pause",
        .args_type  = "device:B",
        .params     = "device",
        .help       = "pause an active background block operation",
        .cmd        = hmp_block_job_pause,
    },

STEXI
@item block_job_pause
@findex block_job_pause
Pause an active block streaming operation.
ETEXI

    {
        .name       = "block_job_resume",
        .args_type  = "device:B",
        .params     = "device",
        .help       = "resume a paused background block operation",
        .cmd        = hmp_block_job_resume,
    },

STEXI
@item block_job_resume
@findex block_job_resume
Resume a paused block streaming operation.
ETEXI

    {
        .name       = "eject",
        .args_type  = "force:-f,device:B",
        .params     = "[-f] device",
        .help       = "eject a removable medium (use -f to force it)",
        .cmd        = hmp_eject,
    },

STEXI
@item eject [-f] @var{device}
@findex eject
Eject a removable medium (use -f to force it).
ETEXI

    {
        .name       = "drive_del",
        .args_type  = "id:B",
        .params     = "device",
        .help       = "remove host block device",
        .cmd        = hmp_drive_del,
    },

STEXI
@item drive_del @var{device}
@findex drive_del
Remove host block device.  The result is that guest generated IO is no longer
submitted against the host device underlying the disk.  Once a drive has
been deleted, the QEMU Block layer returns -EIO which results in IO
errors in the guest for applications that are reading/writing to the device.
These errors are always reported to the guest, regardless of the drive's error
actions (drive options rerror, werror).
ETEXI

    {
        .name       = "change",
        .args_type  = "device:B,target:F,arg:s?,read-only-mode:s?",
        .params     = "device filename [format [read-only-mode]]",
        .help       = "change a removable medium, optional format",
        .cmd        = hmp_change,
    },

STEXI
@item change @var{device} @var{setting}
@findex change
Change the configuration of a device.

@table @option
@item change @var{diskdevice} @var{filename} [@var{format} [@var{read-only-mode}]]
Change the medium for a removable disk device to point to @var{filename}. eg

@example
(qemu) change ide1-cd0 /path/to/some.iso
@end example

@var{format} is optional.

@var{read-only-mode} may be used to change the read-only status of the device.
It accepts the following values:

@table @var
@item retain
Retains the current status; this is the default.

@item read-only
Makes the device read-only.

@item read-write
Makes the device writable.
@end table

@item change vnc @var{display},@var{options}
Change the configuration of the VNC server. The valid syntax for @var{display}
and @var{options} are described at @ref{sec_invocation}. eg

@example
(qemu) change vnc localhost:1
@end example

@item change vnc password [@var{password}]

Change the password associated with the VNC server. If the new password is not
supplied, the monitor will prompt for it to be entered. VNC passwords are only
significant up to 8 letters. eg

@example
(qemu) change vnc password
Password: ********
@end example

@end table
ETEXI

    {
        .name       = "device_add",
        .args_type  = "device:O",
        .params     = "driver[,prop=value][,...]",
        .help       = "add device, like -device on the command line",
        .cmd        = hmp_device_add,
        .command_completion = device_add_completion,
    },

STEXI
@item device_add @var{config}
@findex device_add
Add device.
ETEXI

    {
        .name       = "device_del",
        .args_type  = "id:s",
        .params     = "device",
        .help       = "remove device",
        .cmd        = hmp_device_del,
        .command_completion = device_del_completion,
    },

STEXI
@item device_del @var{id}
@findex device_del
Remove device @var{id}. @var{id} may be a short ID
or a QOM object path.
ETEXI

    {
        .name       = "drive_backup",
        .args_type  = "reuse:-n,full:-f,compress:-c,device:B,target:s,format:s?",
        .params     = "[-n] [-f] [-c] device target [format]",
        .help       = "initiates a point-in-time\n\t\t\t"
                      "copy for a device. The device's contents are\n\t\t\t"
                      "copied to the new image file, excluding data that\n\t\t\t"
                      "is written after the command is started.\n\t\t\t"
                      "The -n flag requests QEMU to reuse the image found\n\t\t\t"
                      "in new-image-file, instead of recreating it from scratch.\n\t\t\t"
                      "The -f flag requests QEMU to copy the whole disk,\n\t\t\t"
                      "so that the result does not need a backing file.\n\t\t\t"
                      "The -c flag requests QEMU to compress backup data\n\t\t\t"
                      "(if the target format supports it).\n\t\t\t",
        .cmd        = hmp_drive_backup,
    },
STEXI
@item drive_backup
@findex drive_backup
Start a point-in-time copy of a block device to a specificed target.
ETEXI

    {
        .name       = "drive_add",
        .args_type  = "node:-n,pci_addr:s,opts:s",
        .params     = "[-n] [[<domain>:]<bus>:]<slot>\n"
                      "[file=file][,if=type][,bus=n]\n"
                      "[,unit=m][,media=d][,index=i]\n"
                      "[,snapshot=on|off][,cache=on|off]\n"
                      "[,readonly=on|off][,copy-on-read=on|off]",
        .help       = "add drive to PCI storage controller",
        .cmd        = hmp_drive_add,
    },

STEXI
@item drive_add
@findex drive_add
Add drive to PCI storage controller.
ETEXI

    {
        .name       = "chardev-add",
        .args_type  = "args:s",
        .params     = "args",
        .help       = "add chardev",
        .cmd        = hmp_chardev_add,
        .command_completion = chardev_add_completion,
    },

STEXI
@item chardev-add args
@findex chardev-add
chardev-add accepts the same parameters as the -chardev command line switch.

ETEXI

    {
        .name       = "chardev-change",
        .args_type  = "id:s,args:s",
        .params     = "id args",
        .help       = "change chardev",
        .cmd        = hmp_chardev_change,
    },

STEXI
@item chardev-change args
@findex chardev-change
chardev-change accepts existing chardev @var{id} and then the same arguments
as the -chardev command line switch (except for "id").

ETEXI

    {
        .name       = "chardev-remove",
        .args_type  = "id:s",
        .params     = "id",
        .help       = "remove chardev",
        .cmd        = hmp_chardev_remove,
        .command_completion = chardev_remove_completion,
    },

STEXI
@item chardev-remove id
@findex chardev-remove
Removes the chardev @var{id}.

ETEXI

    {
        .name       = "chardev-send-break",
        .args_type  = "id:s",
        .params     = "id",
        .help       = "send a break on chardev",
        .cmd        = hmp_chardev_send_break,
        .command_completion = chardev_remove_completion,
    },

STEXI
@item chardev-send-break id
@findex chardev-send-break
Send a break on the chardev @var{id}.

ETEXI

    {
        .name       = "info",
        .args_type  = "item:s?",
        .params     = "[subcommand]",
        .help       = "show various information about the system state",
        .cmd        = hmp_info_help,
        .sub_table  = hmp_info_cmds,
        .flags      = "p",
    },

STEXI
@end table
ETEXI
