
#!/usr/bin/env python
#
# qemu_regdump.py
#
# sosreport plugin to invoke qmp-regdump on QEMU virtual machines
#
# Copyright (C) 2017, Oracle and/or its affiliates. All rights reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms and conditions of the GNU General Public
# License, version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program; If not, see <http://www.gnu.org/licenses/>.

import os
import re
import glob

try:
    # Try to load SOS 3 API
    from sos.plugins import Plugin, RedHatPlugin
except ImportError:
    # Failed import, revert to 1.x/2.2 SOS API: alias the Plugin and
    # RedHatPlugin classes to the old PluginBase class
    import sos.plugintools
    Plugin = RedHatPlugin = sos.plugintools.PluginBase


class qemu_regdump(Plugin, RedHatPlugin):
    """
    QEMU monitor VM register dump

    """
    plugin_name = 'qemu_regdump'
    version = '1.0'

    option_list = [
        ('path', 'path to QMP dump script', '', '/usr/bin/qmp-regdump'),
        ('socket', 'QMP socket (unix or TCP)', '', ''),
        ('kernel', 'location of VM vmlinux kernel file', '', ''),
        ('mapfile', 'location of VM System.map file', '', ''),
    ]

    def setup(self):
        path = self.get_option('path')
        socket = self.get_option('socket')
        kernel = self.get_option('kernel')
        mapfile = self.get_option('mapfile')

        qemupath = None

        for qemubinary in glob.glob('/usr/bin/qemu-system-*'):
            if os.path.exists(qemubinary):
                qemupath = qemubinary
                break

        # capture QEMU version
        if qemupath is None:
            self.add_custom_text('No qemu-system-* binary found')
            return

        self.add_cmd_output(qemupath + ' --version',
                            suggest_filename='qemu-version')

        # check if QMP regdump script exists
        if not os.path.isfile(path):
            self.add_alert('qmp-regdump tool \'%s\' not found' % path)
            return

        if socket:
            sockets = [socket]
        else:
            # find all QMP sockets
            sockets = []
            pids = []

            for proc_file in os.listdir('/proc'):
                if proc_file.isdigit():
                    pids.append(proc_file)

            for pid in pids:
                try:
                    with open(os.path.join('/proc', pid, 'cmdline')) as fd:
                        cmdline = fd.read()
                        socket = re.search(
                            '.*qemu-system-.*-qmp.*[unix|tcp]:([^\x00|,]*)',
                            cmdline)

                        if socket and socket.group(1):
                            sockets.append(socket.group(1))

                except IOError:
                    # process has already terminated
                    continue

        if not sockets:
            self.add_custom_text('No QEMU processes with QMP sockets found')
            return

        cmd = path

        if kernel:
            cmd += ' -k %s ' % kernel
        if mapfile:
            cmd += ' -m %s ' % mapfile

        for socket in sockets:
            sockcmd = cmd + ' -s ' + socket
            self.add_cmd_output(sockcmd,
                                suggest_filename='qmp-regdump-%s' % socket)
