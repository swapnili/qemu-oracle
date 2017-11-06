%ifarch %{ix86}
%global kvm_package   system-x86
# need_qemu_kvm should only ever be used by x86
%global need_qemu_kvm 1
%endif
%ifarch x86_64
%global kvm_package   system-x86
# need_qemu_kvm should only ever be used by x86
%global need_qemu_kvm 1
%endif
%ifarch %{power64}
%global kvm_package   system-ppc
%endif
%ifarch s390x
%global kvm_package   system-s390x
%endif
%ifarch armv7hl
%global kvm_package   system-arm
%endif
%ifarch aarch64
%global kvm_package   system-aarch64
%endif
%ifarch %{mips}
%global kvm_package   system-mips
%endif

%global user_static 0
# glibc static libs are fubar on i386, s390 & ppc64*
# https://bugzilla.redhat.com/show_bug.cgi?id=1352625
%ifarch %{?ix86} s390 s390x %{power64}
%global user_static 0
%endif

%global have_kvm 0
%if 0%{?kvm_package:1}
%global have_kvm 1
%endif

%ifarch %{ix86} x86_64 %{arm} aarch64 %{power64} s390 s390x %{mips}
%global have_seccomp 1
%endif
%ifarch %{ix86} x86_64
%global have_spice   1
%endif

%global have_spice 0
# Toggle whether SDL should be part of the build.
%global have_sdl_gtk 0
# And KSM.
%global have_ksm 0
# Build guest agent?
%global have_agent 0
# Build Windows guest agent?
%global have_windows_agent 0
# Compat layer (qemu-kvm.sh)
%global need_qemu_kvm 0
# PulseAudio and sound cards
%global have_audio 0
# USB redirection and passthrough
%global have_usb 0
# Block devices like RBD or glusterfs or ssh
%global have_rbd 1
%global have_gluster 1
%global have_ssh 0
%global have_iscsi 1
# SmartCard?
%global have_smartcard 0
# Bluetooth
%global have_bluetooth 0
# Braille
%global have_braille 0
# Flat Device Tree (ARM)
%global have_fdt 0
# Google CPU profiler
%global have_gperftools 0
# No TPM
%global have_tpm 0
# Full emulation of different architectures
%global have_user 0
# Emulation only of x86, not the rest.
%global have_x86_emul 1
%global have_all_emul 0
# Generate documentation?
%global have_docs 0
# Support position independent executables? Note that disabling this option
# makes it extremely difficult to patch QEMU binaries.
%global have_pie 1
# Support modules?
%global have_modules 0
# Support Tiny Code Generator debugging?
%global have_tcg_debug 0
# Generate debug info?
%global have_debug_info 0
# Enable sparse checker?
%global have_sparse 0
# Enable GNU TLS support?
%global have_gnutls 1
# Enable nettle support?
%global have_nettle 0
# Enable libgcrypt support?
%global have_gcrypt 0
# Enable curses support?
%global have_curses 0
# Enable VNC?
%global have_vnc 1
# Enable VNC SASL encryption?
%global have_vnc_sasl 1
# Enable VNC JPEG compression?
%global have_vnc_jpg 0
# Enable VNC PNG compression?
%global have_vnc_png 0
# Support VirtFS?
%global have_virtfs 0
# Support curl?
%global have_curl 0
# Support migration over RDMA?
%global have_rdma 0
# Support Virtual Distributed Ethernet?
%global have_vde 0
# Support netmap?
%global have_netmap 0
# Support Linux's AIO?
%global have_linux_aio 1
# Support libcap-ng?
%global have_libcapng 0
# Support libattr?
%global have_attr 0
# Support Linux vhost-net module?
%global have_vhost_net 1
# Support NFS?
%global have_nfs 0
# Support lzo compression library?
%global have_lzo 0
# Support snappy compression library?
%global have_snappy 0
# Support bzip compression library?
%global have_bzip2 0
# Support libseccomp?
%global have_seccomp 1
# Support coroutine pool?
%global have_coroutine_pool 0
# Support libvnuma?
%global have_numa 1
# Support thread-caching malloc?
%global have_tcmalloc 0
# Support jemalloc?
%global have_jemalloc 0
# Support replication?
%global have_replication 1
# Support virtio sockets for host-guest communication?
%global have_vhost_vsock 0
# Support OpenGL?
%global have_opengl 0
# Support virgl rendering?
%global have_virgl 0
# Support xfsctl?
%global have_xfsctl 0
# Support cast debugging?
%global have_qom_cast_debug 0
# Build tools?
%global have_tools 1
# Support DMG images?
%global have_dmg 0

# Xen is available only on i386 x86_64 (from libvirt spec)
%ifarch %{ix86} x86_64
%global have_xen 0
%endif

# Matches edk2.spec ExclusiveArch
# TODO: Revisit this after we finish packaging EDK2 for BMCS.
%ifarch %{ix86} x86_64 %{arm} aarch64
%global have_edk2 0
%endif

# If we can run qemu-sanity-check, hostqemu gets defined.
%ifarch %{arm}
%global hostqemu arm-softmmu/qemu-system-arm
%endif
%ifarch aarch64
%global hostqemu arm-softmmu/qemu-system-aarch64
%endif
%ifarch %{ix86}
%global hostqemu i386-softmmu/qemu-system-i386
%endif
%ifarch x86_64
%global hostqemu x86_64-softmmu/qemu-system-x86_64
%endif

# QMP regdump tool (and sosreport plugin) is only supported on X86_64
%ifarch x86_64
%global have_qmpregdump 1
%endif

# All block-* modules should be listed here.
%global requires_all_block_modules                               \
Requires: %{name}-block-curl = %{epoch}:%{version}-%{release}    \
Requires: %{name}-block-dmg = %{epoch}:%{version}-%{release}     \
Requires: %{name}-block-gluster = %{epoch}:%{version}-%{release} \
Requires: %{name}-block-iscsi = %{epoch}:%{version}-%{release}   \
Requires: %{name}-block-nfs = %{epoch}:%{version}-%{release}     \
Requires: %{name}-block-rbd = %{epoch}:%{version}-%{release}     \
Requires: %{name}-block-ssh = %{epoch}:%{version}-%{release}

# Temp hack for https://bugzilla.redhat.com/show_bug.cgi?id=1343892
# We'll manually turn on hardened build later in this spec
%undefine _hardened_build

# Release candidate version tracking
#global rcver rc4
#if 0%{?rcver:1}
#global rcrel .%{rcver}
#global rcstr -%{rcver}
#endif


Summary: QEMU is a FAST! processor emulator
Name: qemu
Version: 2.9.0
Release: 1%{?rcrel}%{?dist}
Epoch: 12
License: GPLv2+ and LGPLv2+ and BSD
Group: Development/Tools
URL: http://www.qemu.org/
Obsoletes: qemu-kvm-ev, qemu-img-ev, qemu-kvm-common-ev

Source0: %{name}-%{version}.tar.gz

# Creates /dev/kvm
Source3: 80-kvm.rules

%if 0%{?have_ksm}
# KSM control scripts
Source4: ksm.service
Source5: ksm.sysconfig
Source6: ksmctl.c
Source7: ksmtuned.service
Source8: ksmtuned
Source9: ksmtuned.conf
%endif

%if 0%{?have_agent}
# guest agent service
Source10: qemu-guest-agent.service
# guest agent udev rules
Source11: 99-qemu-guest-agent.rules
%endif

# /etc/qemu/bridge.conf
Source12: bridge.conf

%if 0%{?need_qemu_kvm}
# qemu-kvm back compat wrapper installed as /usr/bin/qemu-kvm
Source13: qemu-kvm.sh
%endif

# /etc/modprobe.d/kvm.conf
Source20: kvm.conf

%if 0%{?have_qmpregdump}
# /usr/bin/qmp-regdump
Source21: qmp-regdump
# /usr/lib/<python sitelib>/sos/plugins/qemu_regdump.py
Source22: qemu_regdump.py
%endif

Patch0001: 0001-virtio-Set-PCI-subsystem-vendor-ID-to-Oracle.patch

# documentation deps
BuildRequires: texinfo
# For /usr/bin/pod2man
BuildRequires: perl-podlators
# For sanity test
# BuildRequires: qemu-sanity-check-nodeps
BuildRequires: kernel
# For acpi compilation
BuildRequires: iasl
# For chrpath calls in specfile
BuildRequires: chrpath

%if 0%{?have_sdl_gtk}
# -display sdl support
BuildRequires: SDL2-devel
%endif
# used in various places for compression
BuildRequires: zlib-devel
# used in various places for crypto
BuildRequires: gnutls-devel
# VNC sasl auth support
BuildRequires: cyrus-sasl-devel
# aio implementation for block drivers
BuildRequires: libaio-devel
%if 0%{?have_audio}
# pulseaudio audio output
BuildRequires: pulseaudio-libs-devel
# alsa audio output
BuildRequires: alsa-lib-devel
%endif
%if 0%{?have_iscsi}
# iscsi drive support
BuildRequires: libiscsi-devel
%endif
%if 0%{?have_nfs}
# NFS drive support
BuildRequires: libnfs-devel
%endif
# snappy compression for memory dump
BuildRequires: snappy-devel
# lzo compression for memory dump
BuildRequires: lzo-devel
# needed for -display curses
BuildRequires: ncurses-devel
# used by 9pfs
BuildRequires: libattr-devel
BuildRequires: libcap-devel
%if 0%{?have_libcapng}
# used by qemu-bridge-helper
BuildRequires: libcap-ng-devel
%endif
%if 0%{?have_spice}
# spice usb redirection support
BuildRequires: usbredir-devel >= 0.5.2
%endif
%ifnarch s390 s390x
%if 0%{?have_gperftools}
# tcmalloc support
BuildRequires: gperftools-devel
%endif
%endif
%if 0%{?have_spice:1}
# spice graphics support
BuildRequires: spice-protocol >= 0.12.2
BuildRequires: spice-server-devel >= 0.12.0
%endif
%if 0%{?have_seccomp:1}
# seccomp containment support
BuildRequires: libseccomp-devel >= 2.3.0
%endif
# For network block driver
BuildRequires: libcurl-devel
%if 0%{?have_rbd}
# For rbd block driver
BuildRequires: librbd1-devel
%endif
# We need both because the 'stap' binary is probed for by configure
BuildRequires: systemtap
BuildRequires: systemtap-sdt-devel
# For VNC JPEG support
BuildRequires: libjpeg-devel
# For VNC PNG support
BuildRequires: libpng-devel
# For uuid generation
BuildRequires: libuuid-devel
%if 0%{?have_bluetooth}
# For BlueZ device support
BuildRequires: bluez-libs-devel
%endif
%if 0%{?have_braille}
# For Braille device support
BuildRequires: brlapi-devel
%endif
%if 0%{?have_fdt}
# For FDT device tree support
BuildRequires: libfdt-devel
%endif
# Hard requirement for version >= 1.3
BuildRequires: pixman-devel
%if 0%{?have_gluster}
# For gluster support
BuildRequires: glusterfs-devel >= 3.4.0
BuildRequires: glusterfs-api-devel >= 3.4.0
%endif
%if 0%{?have_usb}
# Needed for usb passthrough for qemu >= 1.5
BuildRequires: libusbx-devel
%endif
%if 0%{?have_ssh}
# SSH block driver
BuildRequires: libssh2-devel
%endif
%if 0%{?have_sdl_gtk}
# GTK frontend
BuildRequires: gtk3-devel
BuildRequires: vte291-devel
# GTK translations
BuildRequires: gettext
%endif
# RDMA migration
%ifnarch s390 s390x
BuildRequires: librdmacm-devel
%endif
%if 0%{?have_xen}
# Xen support
BuildRequires: xen-devel
%endif
%ifarch %{ix86} x86_64 aarch64
# qemu 2.1: needed for memdev hostmem backend
BuildRequires: numactl-devel
%endif
# qemu 2.3: reading bzip2 compressed dmg images
BuildRequires: bzip2-devel
%if 0%{?have_sdl_gtk}
# qemu 2.4: needed for opengl bits
BuildRequires: libepoxy-devel
%endif
# qemu 2.5: needed for TLS test suite
BuildRequires: libtasn1-devel
%if 0%{?have_smartcard}
# qemu 2.5: libcacard is it's own project now
BuildRequires: libcacard-devel >= 2.5.0
%endif
%if 0%{?have_virgl}
# qemu 2.5: virgl 3d support
BuildRequires: virglrenderer-devel
%endif
%if 0%{?have_sdl_gtk}
# qemu 2.6: Needed for gtk GL support
BuildRequires: mesa-libgbm-devel
%endif

# BuildRequires: glibc-static pcre-static glib2-static zlib-static

%if 0%{?hostqemu:1}
# For complicated reasons, this is required so that
# /bin/kernel-install puts the kernel directly into /boot, instead of
# into a /boot/<machine-id> subdirectory (in Fedora >= 23).  This is
# so we can run qemu-sanity-check.  Read the kernel-install script to
# understand why.
BuildRequires: grubby
%endif

%if 0%{?have_user}
Requires: %{name}-user = %{epoch}:%{version}-%{release}
%endif
%if 0%{?have_all_emul}
Requires: %{name}-system-alpha = %{epoch}:%{version}-%{release}
Requires: %{name}-system-arm = %{epoch}:%{version}-%{release}
Requires: %{name}-system-cris = %{epoch}:%{version}-%{release}
Requires: %{name}-system-lm32 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-m68k = %{epoch}:%{version}-%{release}
Requires: %{name}-system-microblaze = %{epoch}:%{version}-%{release}
Requires: %{name}-system-mips = %{epoch}:%{version}-%{release}
Requires: %{name}-system-or1k = %{epoch}:%{version}-%{release}
Requires: %{name}-system-ppc = %{epoch}:%{version}-%{release}
Requires: %{name}-system-s390x = %{epoch}:%{version}-%{release}
Requires: %{name}-system-sh4 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-sparc = %{epoch}:%{version}-%{release}
Requires: %{name}-system-unicore32 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-xtensa = %{epoch}:%{version}-%{release}
Requires: %{name}-system-moxie = %{epoch}:%{version}-%{release}
Requires: %{name}-system-aarch64 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-tricore = %{epoch}:%{version}-%{release}
Requires: %{name}-system-nios2 = %{epoch}:%{version}-%{release}
%endif
%if 0%{?have_x86_emul}
Requires: %{name}-system-x86 = %{epoch}:%{version}-%{release}
%endif
Requires: %{name}-img = %{epoch}:%{version}-%{release}


%description
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation. QEMU has two operating modes:

 * Full system emulation. In this mode, QEMU emulates a full system (for
   example a PC), including a processor and various peripherials. It can be
   used to launch different Operating Systems without rebooting the PC or
   to debug system code.
 * User mode emulation. In this mode, QEMU can launch Linux processes compiled
   for one CPU on another CPU.

As QEMU requires no host kernel patches to run, it is safe and easy to use.


%package  common
Summary: QEMU common files needed by all QEMU targets
Group: Development/Tools
Requires: ipxe-roms-qemu
Requires(post): /usr/bin/getent
Requires(post): /usr/sbin/groupadd
Requires(post): /usr/sbin/useradd
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description common
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the common files needed by all QEMU targets

%if 0%{?have_ksm}
%package -n ksm
Summary: Kernel Samepage Merging services
Group: Development/Tools
Requires(post): systemd-units
Requires(postun): systemd-units
%description -n ksm
Kernel Samepage Merging (KSM) is a memory-saving de-duplication feature,
that merges anonymous (private) pages (not pagecache ones).

This package provides service files for disabling and tuning KSM.
%endif

%if 0%{?have_agent}
%package guest-agent
Summary: QEMU guest agent
Group: System Environment/Daemons
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description guest-agent
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides an agent to run inside guests, which communicates
with the host over a virtio-serial channel named "org.qemu.guest_agent.0"

This package does not need to be installed on the host OS.
%endif

%package  img
Summary: QEMU command line tool for manipulating disk images
Group: Development/Tools

%description img
This package provides a command line tool for manipulating disk images

%if 0%{?have_curl}
%package  block-curl
Summary: QEMU CURL block driver
Group: Development/Tools
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}

%description block-curl
This package provides the additional CURL block driver for QEMU.

Install this package if you want to access remote disks over
http, https, ftp and other transports provided by the CURL library.
%endif

%if 0%{?have_dmg}
%package  block-dmg
Summary: QEMU block driver for DMG disk images
Group: Development/Tools
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}

%description block-dmg
This package provides the additional DMG block driver for QEMU.

Install this package if you want to open '.dmg' files.
%endif

%if 0%{?have_gluster}
%package  block-gluster
Summary: QEMU Gluster block driver
Group: Development/Tools
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}

%description block-gluster
This package provides the additional Gluster block driver for QEMU.

Install this package if you want to access remote Gluster storage.
%endif

%if 0%{?have_iscsi}
%package  block-iscsi
Summary: QEMU iSCSI block driver
Group: Development/Tools
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}

%description block-iscsi
This package provides the additional iSCSI block driver for QEMU.

Install this package if you want to access iSCSI volumes.
%endif

%if 0%{?have_nfs}
%package  block-nfs
Summary: QEMU NFS block driver
Group: Development/Tools
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}

%description block-nfs
This package provides the additional NFS block driver for QEMU.

Install this package if you want to access remote NFS storage.
%endif

%if 0%{?have_rbd}
%package  block-rbd
Summary: QEMU Ceph/RBD block driver
Group: Development/Tools
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}

%description block-rbd
This package provides the additional Ceph/RBD block driver for QEMU.

Install this package if you want to access remote Ceph volumes
using the rbd protocol.
%endif

%if 0%{?have_ssh}
%package  block-ssh
Summary: QEMU SSH block driver
Group: Development/Tools
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}

%description block-ssh
This package provides the additional SSH block driver for QEMU.

Install this package if you want to access remote disks using
the Secure Shell (SSH) protocol.
%endif

%package -n ivshmem-tools
Summary: Client and server for QEMU ivshmem device
Group: Development/Tools

%description -n ivshmem-tools
This package provides client and server tools for QEMU's ivshmem device.


%if 0%{?have_kvm}
%package kvm
Summary: QEMU metapackage for KVM support
Group: Development/Tools
Requires: qemu-%{kvm_package} = %{epoch}:%{version}-%{release}

%description kvm
This is a meta-package that provides a qemu-system-<arch> package for native
architectures where kvm can be enabled. For example, in an x86 system, this
will install qemu-system-x86


%package kvm-core
Summary: QEMU metapackage for KVM support
Group: Development/Tools
Requires: qemu-%{kvm_package}-core = %{epoch}:%{version}-%{release}

%description kvm-core
This is a meta-package that provides a qemu-system-<arch>-core package
for native architectures where kvm can be enabled. For example, in an
x86 system, this will install qemu-system-x86-core
%endif

%if 0%{?have_user}
%package user
Summary: QEMU user mode emulation of qemu targets
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires(post): systemd-units
Requires(postun): systemd-units
# On upgrade, make qemu-user get replaced with qemu-user + qemu-user-binfmt
Obsoletes: %{name}-user < 2:2.6.0-5%{?dist}

%description user
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the user mode emulation of qemu targets
%endif

%package user-binfmt
Summary: QEMU user mode emulation of qemu targets
Group: Development/Tools
Requires: %{name}-user = %{epoch}:%{version}-%{release}
Requires(post): systemd-units
Requires(postun): systemd-units
# qemu-user-binfmt + qemu-user-static both provide binfmt rules
Conflicts: %{name}-user-static
# On upgrade, make qemu-user get replaced with qemu-user + qemu-user-binfmt
Obsoletes: %{name}-user < 2:2.6.0-5%{?dist}

%description user-binfmt
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the user mode emulation of qemu targets

%if %{user_static}
%package user-static
Summary: QEMU user mode emulation of qemu targets static build
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires(post): systemd-units
Requires(postun): systemd-units
# qemu-user-binfmt + qemu-user-static both provide binfmt rules
Conflicts: %{name}-user-binfmt
Provides: %{name}-user-binfmt

%description user-static
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the user mode emulation of qemu targets built as
static binaries
%endif


%package system-x86
Summary: QEMU system emulator for x86
Group: Development/Tools
Requires: %{name}-system-x86-core = %{epoch}:%{version}-%{release}

%description system-x86
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.


%package system-x86-core
Summary: QEMU system emulator for x86
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: seabios-bin
Requires: sgabios-bin
Requires: seavgabios-bin
%if 0%{?have_edk2}
Requires: edk2-ovmf
%endif
%if 0%{?have_seccomp:1}
Requires: libseccomp >= 1.0.0
%endif


%description system-x86-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.

%if 0%{?have_all_emul}
%package system-alpha
Summary: QEMU system emulator for Alpha
Group: Development/Tools
Requires: %{name}-system-alpha-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-alpha
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Alpha systems.

%package system-alpha-core
Summary: QEMU system emulator for Alpha
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-alpha-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Alpha systems.


%package system-arm
Summary: QEMU system emulator for ARM
Group: Development/Tools
Requires: %{name}-system-arm-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-arm
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for ARM systems.

%package system-arm-core
Summary: QEMU system emulator for ARM
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-arm-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for ARM boards.


%package system-mips
Summary: QEMU system emulator for MIPS
Group: Development/Tools
Requires: %{name}-system-mips-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-mips
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for MIPS systems.

%package system-mips-core
Summary: QEMU system emulator for MIPS
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-mips-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for MIPS boards.


%package system-cris
Summary: QEMU system emulator for CRIS
Group: Development/Tools
Requires: %{name}-system-cris-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-cris
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for CRIS systems.

%package system-cris-core
Summary: QEMU system emulator for CRIS
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-cris-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for CRIS boards.


%package system-lm32
Summary: QEMU system emulator for LatticeMico32
Group: Development/Tools
Requires: %{name}-system-lm32-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-lm32
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for LatticeMico32 systems.

%package system-lm32-core
Summary: QEMU system emulator for LatticeMico32
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-lm32-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for LatticeMico32 boards.


%package system-m68k
Summary: QEMU system emulator for ColdFire (m68k)
Group: Development/Tools
Requires: %{name}-system-m68k-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-m68k
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for ColdFire boards.

%package system-m68k-core
Summary: QEMU system emulator for ColdFire (m68k)
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-m68k-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for ColdFire boards.


%package system-microblaze
Summary: QEMU system emulator for Microblaze
Group: Development/Tools
Requires: %{name}-system-microblaze-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-microblaze
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Microblaze boards.

%package system-microblaze-core
Summary: QEMU system emulator for Microblaze
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-microblaze-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Microblaze boards.


%package system-or1k
Summary: QEMU system emulator for OpenRisc32
Group: Development/Tools
Requires: %{name}-system-or1k-core = %{epoch}:%{version}-%{release}
Obsoletes: %{name}-system-or32 < 2:2.9.0
%{requires_all_block_modules}
%description system-or1k
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for OpenRisc32 boards.

%package system-or1k-core
Summary: QEMU system emulator for OpenRisc32
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Obsoletes: %{name}-system-or32-core < 2:2.9.0
%description system-or1k-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for OpenRisc32 boards.


%package system-s390x
Summary: QEMU system emulator for S390
Group: Development/Tools
Requires: %{name}-system-s390x-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-s390x
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for S390 systems.

%package system-s390x-core
Summary: QEMU system emulator for S390
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-s390x-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for S390 systems.


%package system-sh4
Summary: QEMU system emulator for SH4
Group: Development/Tools
Requires: %{name}-system-sh4-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-sh4
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for SH4 boards.

%package system-sh4-core
Summary: QEMU system emulator for SH4
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-sh4-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for SH4 boards.


%package system-sparc
Summary: QEMU system emulator for SPARC
Group: Development/Tools
Requires: %{name}-system-sparc-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-sparc
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for SPARC and SPARC64 systems.

%package system-sparc-core
Summary: QEMU system emulator for SPARC
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: openbios
%description system-sparc-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for SPARC and SPARC64 systems.


%package system-ppc
Summary: QEMU system emulator for PPC
Group: Development/Tools
Requires: %{name}-system-ppc-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-ppc
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for PPC and PPC64 systems.

%package system-ppc-core
Summary: QEMU system emulator for PPC
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: openbios
Requires: SLOF
Requires: seavgabios-bin
%description system-ppc-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for PPC and PPC64 systems.


%package system-xtensa
Summary: QEMU system emulator for Xtensa
Group: Development/Tools
Requires: %{name}-system-xtensa-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-xtensa
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Xtensa boards.

%package system-xtensa-core
Summary: QEMU system emulator for Xtensa
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-xtensa-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Xtensa boards.


%package system-unicore32
Summary: QEMU system emulator for Unicore32
Group: Development/Tools
Requires: %{name}-system-unicore32-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-unicore32
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Unicore32 boards.

%package system-unicore32-core
Summary: QEMU system emulator for Unicore32
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-unicore32-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Unicore32 boards.


%package system-moxie
Summary: QEMU system emulator for Moxie
Group: Development/Tools
Requires: %{name}-system-moxie-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-moxie
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Moxie boards.

%package system-moxie-core
Summary: QEMU system emulator for Moxie
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-moxie-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Moxie boards.


%package system-aarch64
Summary: QEMU system emulator for AArch64
Group: Development/Tools
Requires: %{name}-system-aarch64-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-aarch64
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for AArch64.

%package system-aarch64-core
Summary: QEMU system emulator for AArch64
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%if 0%{?have_edk2:1}
Requires: edk2-aarch64
%endif
%description system-aarch64-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for AArch64.


%package system-tricore
Summary: QEMU system emulator for tricore
Group: Development/Tools
Requires: %{name}-system-tricore-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-tricore
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Tricore.

%package system-tricore-core
Summary: QEMU system emulator for tricore
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-tricore-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Tricore.


%package system-nios2
Summary: QEMU system emulator for nios2
Group: Development/Tools
Requires: %{name}-system-nios2-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-nios2
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for NIOS2.

%package system-nios2-core
Summary: QEMU system emulator for nios2
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-nios2-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for NIOS2.
%endif


%prep
%setup -q -n qemu-%{version}%{?rcstr}
%autopatch -p1


%build

# QEMU already knows how to set _FORTIFY_SOURCE
%global optflags %(echo %{optflags} | sed 's/-Wp,-D_FORTIFY_SOURCE=2//')

# drop -g flag to prevent memory exhaustion by linker
%ifarch s390
%global optflags %(echo %{optflags} | sed 's/-g//')
sed -i.debug 's/"-g $CFLAGS"/"$CFLAGS"/g' configure
%endif

# OOM killer breaks builds with parallel make on s390(x)
%ifarch s390 s390x
%global _smp_mflags %{nil}
%endif


# --build-id option is used for giving info to the debug packages.
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

# As of qemu 2.1, --enable-trace-backends supports multiple backends,
# but there's a performance impact for non-dtrace so we don't use them
tracebackends="dtrace"

%if 0%{?have_x86_emul}
    system_arch="$system_arch i386 x86_64"
%endif
%if 0%{?have_all_emul}
    system_arch="\
        aarch64 \
        alpha \
        arm \
        cris \
        lm32 \
        m68k \
        microblaze \
        microblazeel \
        mips \
        mips64 \
        mips64el \
        mipsel \
        moxie \
        nios2 \
        or1k \
        ppc \
        ppc64 \
        ppcemb \
        s390x \
        sh4 \
        sh4eb \
        sparc \
        sparc64 \
        tricore \
        unicore32 \
        xtensa \
        xtensaeb"
%endif

%if 0%{?have_user}
    user_arch="\
        aarch64 \
        alpha \
        arm \
        armeb \
        cris \
        i386 \
        hppa \
        m68k \
        microblaze \
        microblazeel \
        mips \
        mips64 \
        mips64el \
        mipsel \
        mipsn32 \
        mipsn32el \
        nios2 \
        or1k \
        ppc \
        ppc64 \
        ppc64abi32 \
        ppc64le \
        s390x \
        sh4 \
        sh4eb \
        sparc \
        sparc32plus \
        sparc64 \
        x86_64"
%endif

dynamic_targets=
static_targets=

for arch in $system_arch
do
  dynamic_targets="$dynamic_targets $arch-softmmu"
done

for arch in $user_arch
do
  dynamic_targets="$dynamic_targets $arch-linux-user"
  static_targets="$static_targets $arch-linux-user"
done


%if 0%{?have_spice}
    %global spiceflag --enable-spice
%else
    %global spiceflag --disable-spice
%endif

%if 0%{?have_iscsi}
    %global iscsiflag --enable-libiscsi
%else
    %global iscsiflag --disable-libiscsi
%endif

%if 0%{?have_smartcard}
    %global smartcardflag --enable-smartcard
%else
    %global smartcardflag --disable-smartcard
%endif

%if 0%{?have_fdt}
    %global fdtflag --enable-fdt
%else
    %global fdtflag --disable-fdt
%endif

%if 0%{?have_rbd}
    %global rbdflag --enable-rbd
%else
    %global rbdflag --disable-rbd
%endif

%if 0%{?have_sdl_gtk}
    %global sdlflag --enable-sdl --enable-virglrenderer --enable-gtk --enable-vte
%else
    %global sdlflag --disable-sdl --disable-virglrenderer --disable-gtk --disable-vte
%endif

%if 0%{?have_audio}
    %global audioflags --audio-drv-list=pa,sdl,alsa,oss
%else
    %global audioflags --audio-drv-list=""
%endif

%if 0%{?have_agent}
    %global guestflags --enable-guest-agent
%else
    %global guestflags --disable-guest-agent
%endif

%if 0%{?have_windows_agent}
    %global windowsguestflags --enable-guest-agent-msi
%else
    %global windowsguestflags --disable-guest-agent-msi
%endif

%if 0%{?have_tpm}
    %global tpmflags --enable-tpm
%else
    %global tpmflags --disable-tpm
%endif

%if 0%{?have_user}
    %global userflags --enable-user --enable-linux-user --disable-bsd-user
%else
    %global userflags --disable-user --disable-linux-user --disable-bsd-user
%endif

%if 0%{?have_docs}
    %global docsflags --enable-docs
%else
    %global docsflags --disable-docs
%endif

%if 0%{?have_pie}
    %global pieflags --enable-pie
%else
    %global pieflags --disable-pie
%endif

%if 0%{?have_modules}
    %global moduleflags --enable-modules
%else
    %global moduleflags --disable-modules
%endif

%if 0%{?have_tcg_debug}
    %global tcgdebugflags --enable-debug-tcg
%else
    %global tcgdebugflags --disable-debug-tcg
%endif

%if 0%{?have_debug_info}
    %global debuginfoflags --enable-debug-info
%else
    %global debuginfoflags --disable-debug-info
%endif

%if 0%{?have_sparse}
    %global sparseflags --enable-sparse
%else
    %global sparseflags --disable-sparse
%endif

%if 0%{?have_gnutls}
    %global gnutlsflags --enable-gnutls
%else
    %global gnutlsflags --disable-gnutls
%endif

%if 0%{?have_nettle}
    %global nettleflags --enable-nettle
%else
    %global nettleflags --disable-nettle
%endif

%if 0%{?have_gcrypt}
    %global gcryptflags --enable-gcrypt
%else
    %global gcryptflags --disable-gcrypt
%endif

%if 0%{?have_curses}
    %global cursesflags --enable-curses
%else
    %global cursesflags --disable-curses
%endif

%if 0%{?have_vnc}
    %global vncflags --enable-vnc
%else
    %global vncflags --disable-vnc
%endif

%if 0%{?have_vnc_sasl}
    %global vncsaslflags --enable-vnc-sasl
%else
    %global vncsaslflags --disable-vnc-sasl
%endif

%if 0%{?have_vnc_jpg}
    %global vncjpgflags --enable-vnc-jpeg
%else
    %global vncjpgflags --disable-vnc-jpeg
%endif

%if 0%{?have_vnc_png}
    %global vncpngflags --enable-vnc-png
%else
    %global vncpngflags --disable-vnc-png
%endif

%if 0%{?have_virtfs}
    %global virtfsflags --enable-virtfs
%else
    %global virtfsflags --disable-virtfs
%endif

%if 0%{?have_braille}
    %global brailleflags --enable-brlapi
%else
    %global brailleflags --disable-brlapi
%endif

%if 0%{?have_xen}
    %global xenflags --enable-xen --enable-xen-pci-passthrough
%else
    %global xenflags --disable-xen --disable-xen-pci-passthrough
%endif

%if 0%{?have_curl}
    %global curlflags --enable-curl
%else
    %global curlflags --disable-curl
%endif

%if 0%{?have_bluetooth}
    %global bluetoothflags --enable-bluez
%else
    %global bluetoothflags --disable-bluez
%endif

%if 0%{?have_rdma}
    %global rdmaflags --enable-rdma
%else
    %global rdmaflags --disable-rdma
%endif

%if 0%{?have_vde}
    %global vdeflags --enable-vde
%else
    %global vdeflags --disable-vde
%endif

%if 0%{?have_netmap}
    %global netmapflags --enable-netmap
%else
    %global netmapflags --disable-netmap
%endif

%if 0%{?have_linux_aio}
    %global linuxaioflags --enable-linux-aio
%else
    %global linuxaioflags --disable-linux-aio
%endif

%if 0%{?have_libcapng}
    %global libcapngflags --enable-cap-ng
%else
    %global libcapngflags --disable-cap-ng
%endif

%if 0%{?have_attr}
    %global attrflags --enable-attr
%else
    %global attrflags --disable-attr
%endif

%if 0%{?have_vhost_net}
    %global vhostnetflags --enable-vhost-net
%else
    %global vhostnetflags --disable-vhost-net
%endif

%if 0%{?have_nfs}
    %global nfsflags --enable-libnfs
%else
    %global nfsflags --disable-libnfs
%endif

%if 0%{?have_usb}
    %global usbflags --enable-libusb --enable-usb-redir
%else
    %global usbflags --disable-libusb --disable-usb-redir
%endif

%if 0%{?have_lzo}
    %global lzoflags --enable-lzo
%else
    %global lzoflags --disable-lzo
%endif

%if 0%{?have_snappy}
    %global snappyflags --enable-snappy
%else
    %global snappyflags --disable-snappy
%endif

%if 0%{?have_bzip2}
    %global bzip2flags --enable-bzip2
%else
    %global bzip2flags --disable-bzip2
%endif

%if 0%{?have_seccomp}
    %global seccompflags --enable-seccomp
%else
    %global seccompflags --disable-seccomp
%endif

%if 0%{?have_coroutine_pool}
    %global coroutineflags --enable-coroutine-pool
%else
    %global coroutineflags --disable-coroutine-pool
%endif

%if 0%{?have_gluster}
    %global glusterflags --enable-glusterfs
%else
    %global glusterflags --disable-glusterfs
%endif

%if 0%{?have_ssh}
    %global sshflags --enable-libssh2
%else
    %global sshflags --disable-libssh2
%endif

%if 0%{?have_numa}
    %global numaflags --enable-numa
%else
    %global numaflags --disable-numa
%endif

%if 0%{?have_tcmalloc}
    %global tcmallocflags --enable-tcmalloc
%else
    %global tcmallocflags --disable-tcmalloc
%endif

%if 0%{?have_jemalloc}
    %global jemallocflags --enable-jemalloc
%else
    %global jemallocflags --disable-jemalloc
%endif

%if 0%{?have_replication}
    %global replicationflags --enable-replication
%else
    %global replicationflags --disable-replication
%endif

%if 0%{?have_vhost_vsock}
    %global vhostvsockflags --enable-vhost-vsock
%else
    %global vhostvsockflags --disable-vhost-vsock
%endif

%if 0%{?have_opengl}
    %global openglflags --enable-opengl
%else
    %global openglflags --disable-opengl
%endif

%if 0%{?have_virgl}
    %global virglflags --enable-virglrenderer
%else
    %global virglflags --disable-virglrenderer
%endif

%if 0%{?have_xfsctl}
    %global xfsctlflags --enable-xfsctl
%else
    %global xfsctlflags --disable-xfsctl
%endif

%if 0%{?have_qom_cast_debug}
    %global qomcastflags --enable-qom-cast-debug
%else
    %global qomcastflags --disable-qom-cast-debug
%endif

run_configure() {
    ../configure \
        --prefix=%{_prefix} \
        --libdir=%{_libdir} \
        --sysconfdir=%{_sysconfdir} \
        --interp-prefix=%{_prefix}/qemu-%%M \
        --localstatedir=%{_localstatedir} \
        --libexecdir=%{_libexecdir} \
        --with-pkgversion=%{name}-%{version}-%{release} \
        --disable-strip \
        --disable-werror \
        --enable-kvm \
%ifarch s390 %{mips64}
        --enable-tcg-interpreter \
%endif
        --enable-trace-backend=$tracebackends \
        %{spiceflag} \
        %{iscsiflag} \
        %{smartcardflag} \
        %{fdtflag} \
        %{rbdflag} \
        %{sdlflag} \
        --with-sdlabi="2.0" \
        --with-gtkabi="3.0" \
        %{guestflags} \
        %{windowsguestflags} \
        %{tpmflags} \
        %{userflags} \
        %{docsflags} \
        %{pieflags} \
        %{moduleflags} \
        %{tcgdebugflags} \
        %{debuginfoflags} \
        %{sparseflags} \
        %{gnutlsflags} \
        %{nettleflags} \
        %{gcryptflags} \
        %{cursesflags} \
        %{vncflags} \
        %{vncsaslflags} \
        %{vncjpgflags} \
        %{vncpngflags} \
        %{virtfsflags} \
        %{xenflags} \
        %{brailleflags} \
        %{curlflags} \
        %{bluetoothflags} \
        %{rdmaflags} \
        %{vdeflags} \
        %{netmapflags} \
        %{linuxaioflags} \
        %{libcapngflags} \
        %{attrflags} \
        %{vhostnetflags} \
        %{nfsflags} \
        %{usbflags} \
        %{lzoflags} \
        %{snappyflags} \
        %{bzip2flags} \
        %{seccompflags} \
        %{coroutineflags} \
        %{glusterflags} \
        %{sshflags} \
        %{numaflags} \
        %{tcmallocflags} \
        %{jemallocflags} \
        %{replicationflags} \
        %{vhostvsockflags} \
        %{openglflags} \
        %{virglflags} \
        %{xfsctlflags} \
        %{qomcastflags} \
        "$@" || cat config.log
}

mkdir build-dynamic
pushd build-dynamic

run_configure \
%ifnarch aarch64
    --extra-ldflags="$extraldflags -specs=/usr/lib/rpm/redhat/redhat-hardened-ld -pie -Wl,-z,relro -Wl,-z,now" \
%else
    --extra-ldflags="$extraldflags -specs=/usr/lib/rpm/redhat/redhat-hardened-ld" \
%endif
    --extra-cflags="%{optflags} -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1" \
    --target-list="$dynamic_targets" \
    --enable-pie \
    --enable-modules \
    --tls-priority=@QEMU,SYSTEM \
    %{spiceflag} \
    --with-sdlabi="2.0" \
    --with-gtkabi="3.0"

echo "config-host.mak contents:"
echo "==="
cat config-host.mak
echo "==="

make V=1 %{?_smp_mflags} $buildldflags

popd

%if 0%{?user_static}
mkdir build-static
pushd build-static

run_configure \
%ifnarch aarch64
    --extra-ldflags="$extraldflags -Wl,-z,relro -Wl,-z,now" \
%else
    --extra-ldflags="$extraldflags" \
%endif
    --extra-cflags="%{optflags}" \
    --target-list="$static_targets" \
    --static \
    --disable-pie \
    --disable-tcmalloc \
    --disable-sdl \
    --disable-gtk \
    --disable-spice \
    --disable-tools \
    --disable-guest-agent \
    --disable-guest-agent-msi \
    --disable-curses \
    --disable-curl \
    --disable-gnutls \
    --disable-gcrypt \
    --disable-nettle \
    --disable-cap-ng \
    --disable-brlapi \
    --disable-libnfs \
    --disable-vnc-sasl

make V=1 %{?_smp_mflags} $buildldflags

popd
%endif

# gcc %{_sourcedir}/ksmctl.c -O2 -g -o ksmctl


%install

%global _udevdir /lib/udev/rules.d
%global qemudocdir %{_docdir}/%{name}

mkdir -p %{buildroot}%{_udevdir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/qemu

%if 0%{?have_ksm}
install -D -p -m 0644 %{_sourcedir}/ksm.service %{buildroot}%{_unitdir}
install -D -p -m 0644 %{_sourcedir}/ksm.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/ksm
install -D -p -m 0755 ksmctl %{buildroot}%{_libexecdir}/ksmctl

install -D -p -m 0644 %{_sourcedir}/ksmtuned.service %{buildroot}%{_unitdir}
install -D -p -m 0755 %{_sourcedir}/ksmtuned %{buildroot}%{_sbindir}/ksmtuned
install -D -p -m 0644 %{_sourcedir}/ksmtuned.conf %{buildroot}%{_sysconfdir}/ksmtuned.conf
%endif

install -D -p -m 0644 %{_sourcedir}/kvm.conf %{buildroot}%{_sysconfdir}/modprobe.d/kvm.conf

%if 0%{?have_agent}
# Install qemu-guest-agent service and udev rules
install -m 0644 %{_sourcedir}/qemu-guest-agent.service %{buildroot}%{_unitdir}
install -m 0644 %{_sourcedir}/99-qemu-guest-agent.rules %{buildroot}%{_udevdir}
%endif

%ifarch s390x
install -d %{buildroot}%{_sysconfdir}/sysctl.d
install -m 0644 %{_sourcedir}/50-kvm-s390x.conf %{buildroot}%{_sysconfdir}/sysctl.d
%endif

%ifarch %{power64}
install -d %{buildroot}%{_sysconfdir}/security/limits.d
install -m 0644 %{_sourcedir}/95-kvm-ppc64-memlock.conf %{buildroot}%{_sysconfdir}/security/limits.d
%endif


# Install kvm specific bits
%if %{have_kvm}
mkdir -p %{buildroot}%{_bindir}/
install -m 0644 %{_sourcedir}/80-kvm.rules %{buildroot}%{_udevdir}
%endif

%if %{user_static}
pushd build-static
make DESTDIR=%{buildroot} install

# Give all QEMU user emulators a -static suffix
for src in %{buildroot}%{_bindir}/qemu-*
do
  mv $src $src-static
done

# Update trace files to match

for src in %{buildroot}%{_datadir}/systemtap/tapset/qemu-*.stp
do
  dst=`echo $src | sed -e 's/.stp/-static.stp/'`
  mv $src $dst
  perl -i -p -e 's/(qemu-\w+)/$1-static/g; s/(qemu\.user\.\w+)/$1.static/g' $dst
done


popd
%endif

pushd build-dynamic
make DESTDIR=%{buildroot} install
popd

%if 0%{?have_sdl_gtk}
%find_lang %{name}
%endif

%if 0%{?have_docs}
chmod -x %{buildroot}%{_mandir}/man1/*
install -D -p -m 0644 -t %{buildroot}%{qemudocdir} Changelog README COPYING COPYING.LIB LICENSE
for emu in %{buildroot}%{_bindir}/qemu-system-*; do
    ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/$(basename $emu).1.gz
done
%endif

%if 0%{?need_qemu_kvm}
install -m 0755 %{_sourcedir}/qemu-kvm.sh %{buildroot}%{_bindir}/qemu-kvm
ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/qemu-kvm.1.gz
%endif

install -D -p -m 0644 qemu.sasl %{buildroot}%{_sysconfdir}/sasl2/qemu.conf

# Provided by package openbios
rm -rf %{buildroot}%{_datadir}/%{name}/openbios-ppc
rm -rf %{buildroot}%{_datadir}/%{name}/openbios-sparc32
rm -rf %{buildroot}%{_datadir}/%{name}/openbios-sparc64
# Provided by package SLOF
rm -rf %{buildroot}%{_datadir}/%{name}/slof.bin
# Provided by package ipxe
rm -rf %{buildroot}%{_datadir}/%{name}/pxe*rom
# TODO: Revisit %{buildroot}%{_datadir}/%{name}/efi*rom files
# after we finish packaging EDK2 for BMCS.
# Provided by package seavgabios
rm -rf %{buildroot}%{_datadir}/%{name}/vgabios*bin
# Provided by package seabios
rm -rf %{buildroot}%{_datadir}/%{name}/bios.bin
rm -rf %{buildroot}%{_datadir}/%{name}/bios-256k.bin
# Provided by package sgabios
rm -rf %{buildroot}%{_datadir}/%{name}/sgabios.bin
# We don't package the setuid root qemu-bridge-helper script
rm -rf %{buildroot}%{_libexecdir}/qemu-bridge-helper

%if 0%{?have_all_emul}
%else
unused_blobs="QEMU,cgthree.bin QEMU,tcx.bin bamboo.dtb palcode-clipper \
petalogix-ml605.dtb petalogix-s3adsp1800.dtb ppc_rom.bin \
s390-ccw.img s390-zipl.rom spapr-rtas.bin u-boot.e500 \
skiboot.lid"
for blob in $unused_blobs; do
   rm -rf %{buildroot}%{_datadir}/%{name}/$blob
done
%endif

# TODO: Revisit this after we finish packaging EDK2 and ipxe
# for BMCS.
pxe_link() {
  ln -s ../ipxe/$2.rom %{buildroot}%{_datadir}/%{name}/pxe-$1.rom
}

pxe_link e1000 8086100e
pxe_link ne2k_pci 10ec8029
pxe_link pcnet 10222000
pxe_link rtl8139 10ec8139
pxe_link virtio 1af41000
pxe_link eepro100 80861209
pxe_link e1000e 808610d3
pxe_link vmxnet3 15ad07b0

rom_link() {
    ln -s $1 %{buildroot}%{_datadir}/%{name}/$2
}

rom_link ../seavgabios/vgabios-isavga.bin vgabios.bin
rom_link ../seavgabios/vgabios-cirrus.bin vgabios-cirrus.bin
rom_link ../seavgabios/vgabios-qxl.bin vgabios-qxl.bin
rom_link ../seavgabios/vgabios-stdvga.bin vgabios-stdvga.bin
rom_link ../seavgabios/vgabios-vmware.bin vgabios-vmware.bin
rom_link ../seavgabios/vgabios-virtio.bin vgabios-virtio.bin
rom_link ../seabios/bios.bin bios.bin
rom_link ../seabios/bios-256k.bin bios-256k.bin
rom_link ../sgabios/sgabios.bin sgabios.bin

%if 0%{?have_user}
# Install binfmt
mkdir -p %{buildroot}%{_exec_prefix}/lib/binfmt.d
for i in dummy \
%ifnarch %{ix86} x86_64
    qemu-i386 \
%endif
%ifnarch alpha
    qemu-alpha \
%endif
%ifnarch aarch64
    qemu-aarch64 \
%endif
%ifnarch %{arm}
    qemu-arm \
%endif
    qemu-armeb \
    qemu-cris \
    qemu-microblaze qemu-microblazeel \
%ifnarch mips64
    qemu-mips64 \
%ifnarch mips
    qemu-mips \
%endif
%endif
%ifnarch mips64el
    qemu-mips64el \
%ifnarch mipsel
    qemu-mipsel \
%endif
%endif
%ifnarch m68k
    qemu-m68k \
%endif
%ifnarch ppc %{power64}
    qemu-ppc qemu-ppc64abi32 qemu-ppc64 \
%endif
%ifnarch sparc sparc64
    qemu-sparc qemu-sparc32plus qemu-sparc64 \
%endif
%ifnarch s390 s390x
    qemu-s390x \
%endif
%ifnarch sh4
    qemu-sh4 \
%endif
    qemu-sh4eb \
; do
  test $i = dummy && continue

  grep /$i:\$ %{_sourcedir}/qemu.binfmt > %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i-dynamic.conf
  chmod 644 %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i-dynamic.conf

%if %{user_static}
  grep /$i:\$ %{_sourcedir}/qemu.binfmt | tr -d '\n' > %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i-static.conf
  echo "F" >> %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i-static.conf
  perl -i -p -e "s/$i:F/$i-static:F/" %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i-static.conf
  chmod 644 %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i-static.conf
%endif

done < %{_sourcedir}/qemu.binfmt
%endif


# Install rules to use the bridge helper with libvirt's virbr0
install -m 0644 %{_sourcedir}/bridge.conf %{buildroot}%{_sysconfdir}/qemu

%if 0%{?have_qmpregdump}
# Install in /usr/bin
install -m 0755 %{_sourcedir}/qmp-regdump %{buildroot}%{_bindir}/
# Install in /usr/lib/<python sitelib>/sos/plugins/
mkdir -p %{buildroot}%{python_sitelib}/sos/plugins
install -m 0755 %{_sourcedir}/qemu_regdump.py %{buildroot}%{python_sitelib}/sos/plugins
%endif

# When building using 'rpmbuild' or 'fedpkg local', RPATHs can be left in
# the binaries and libraries (although this doesn't occur when
# building in Koji, for some unknown reason). Some discussion here:
#
# https://lists.fedoraproject.org/pipermail/devel/2013-November/192553.html
#
# In any case it should always be safe to remove RPATHs from
# the final binaries:
for f in %{buildroot}%{_bindir}/* %{buildroot}%{_libdir}/* \
         %{buildroot}%{_libexecdir}/*; do
  if file $f | grep -q ELF | grep -q -i shared; then chrpath --delete $f; fi
done

# We need to make the block device modules executable else
# RPM won't pick up their dependencies.
chmod +x %{buildroot}%{_libdir}/qemu/block-*.so


%check

# Tests are hanging on s390 as of 2.3.0
#   https://bugzilla.redhat.com/show_bug.cgi?id=1206057
# Tests seem to be a recurring problem on s390, so I'd suggest just leaving
# it disabled.
%global archs_skip_tests s390
%global archs_ignore_test_failures 0

pushd build-dynamic
%ifnarch %{archs_skip_tests}

# Check the binary runs (see eg RHBZ#998722).
b="./x86_64-softmmu/qemu-system-x86_64"
if [ -x "$b" ]; then "$b" -help; fi

%ifarch %{archs_ignore_test_failures}
make check V=1
%else
make check V=1 || :
%endif

# %if 0%{?hostqemu:1}
# Sanity-check current kernel can boot on this qemu.
# The results are advisory only.
# qemu-sanity-check --qemu=%{?hostqemu} ||:
# %endif

%endif  # archs_skip_tests
popd


%if %{have_kvm}
%post %{kvm_package}
# Default /dev/kvm permissions are 660, we install a udev rule changing that
# to 666. However trying to trigger the re-permissioning via udev has been
# a neverending source of trouble, so we just force it with chmod. For
# more info see: https://bugzilla.redhat.com/show_bug.cgi?id=950436
chmod --quiet 666 /dev/kvm || :

%ifarch s390x
%sysctl_apply 50-kvm-s390x.conf
%endif
%endif

%post system-x86-core
%if 0%{?have_kvm}
udevadm control --reload >/dev/null 2>&1 || :
udevadm trigger --subsystem-match=misc --sysname-match=kvm --action=add || :
chmod --quiet 666 /dev/kvm || :
%endif

%post common
getent group kvm >/dev/null || groupadd -g 36 -r kvm
getent group qemu >/dev/null || groupadd -g 107 -r qemu
getent passwd qemu >/dev/null || \
  useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin \
    -c "qemu user" qemu


%if 0%{?have_ksm}
%post -n ksm
%systemd_post ksm.service
%systemd_post ksmtuned.service
%preun -n ksm
%systemd_preun ksm.service
%systemd_preun ksmtuned.service
%postun -n ksm
%systemd_postun_with_restart ksm.service
%systemd_postun_with_restart ksmtuned.service
%endif

%if 0%{?have_user}
%post user
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%endif

%if 0%{?have_agent}
%post guest-agent
%systemd_post qemu-guest-agent.service
%preun guest-agent
%systemd_preun qemu-guest-agent.service
%postun guest-agent
%systemd_postun_with_restart qemu-guest-agent.service
%endif


%global kvm_files \
%{_udevdir}/80-kvm.rules

%files
# Deliberately empty

%if 0%{?have_sdl_gtk}
%files common -f %{name}.lang
%else
%files common
%endif
%if 0%{?have_docs}
%dir %{qemudocdir}
%doc %{qemudocdir}/Changelog
%doc %{qemudocdir}/COPYING
%doc %{qemudocdir}/COPYING.LIB
%doc %{qemudocdir}/LICENSE
%doc %{qemudocdir}/qemu-doc.html
%doc %{qemudocdir}/qemu-doc.txt
%doc %{qemudocdir}/qemu-ga-ref.html
%doc %{qemudocdir}/qemu-ga-ref.txt
%doc %{qemudocdir}/qemu-qmp-ref.html
%doc %{qemudocdir}/qemu-qmp-ref.txt
%doc %{qemudocdir}/README
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/virtfs-proxy-helper.1*
%{_mandir}/man7/qemu-ga-ref.7*
%{_mandir}/man7/qemu-qmp-ref.7*
%endif
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/qemu-icon.bmp
%{_datadir}/%{name}/qemu_logo_no_text.svg
%{_datadir}/%{name}/keymaps/
%{_datadir}/%{name}/trace-events-all
%{_datadir}/%{name}/vgabios.bin
%{_datadir}/%{name}/vgabios-cirrus.bin
%{_datadir}/%{name}/vgabios-qxl.bin
%{_datadir}/%{name}/vgabios-stdvga.bin
%{_datadir}/%{name}/vgabios-vmware.bin
%{_datadir}/%{name}/vgabios-virtio.bin
%{_datadir}/%{name}/pxe-e1000.rom
%{_datadir}/%{name}/efi-e1000.rom
%{_datadir}/%{name}/pxe-e1000e.rom
%{_datadir}/%{name}/efi-e1000e.rom
%{_datadir}/%{name}/pxe-eepro100.rom
%{_datadir}/%{name}/efi-eepro100.rom
%{_datadir}/%{name}/pxe-ne2k_pci.rom
%{_datadir}/%{name}/efi-ne2k_pci.rom
%{_datadir}/%{name}/pxe-pcnet.rom
%{_datadir}/%{name}/efi-pcnet.rom
%{_datadir}/%{name}/pxe-rtl8139.rom
%{_datadir}/%{name}/efi-rtl8139.rom
%{_datadir}/%{name}/pxe-virtio.rom
%{_datadir}/%{name}/efi-virtio.rom
%{_datadir}/%{name}/pxe-vmxnet3.rom
%{_datadir}/%{name}/efi-vmxnet3.rom
%if 0%{?have_virtfs}
%{_bindir}/virtfs-proxy-helper
%endif
%config(noreplace) %{_sysconfdir}/sasl2/qemu.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/kvm.conf
%dir %{_sysconfdir}/qemu
%config(noreplace) %{_sysconfdir}/qemu/bridge.conf
%dir %{_libdir}/qemu
%if 0%{?have_qmpregdump}
%config(noreplace) %{_bindir}/qmp-regdump
%config(noreplace) %{python_sitelib}/sos/plugins/qemu_regdump.py*
%endif

%if 0%{?have_ksm}
%files -n ksm
%{_libexecdir}/ksmctl
%{_sbindir}/ksmtuned
%{_unitdir}/ksmtuned.service
%{_unitdir}/ksm.service
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%config(noreplace) %{_sysconfdir}/sysconfig/ksm
%endif

%if 0%{?have_agent}
%files guest-agent
%{_bindir}/qemu-ga
%{_mandir}/man8/qemu-ga.8*
%{_unitdir}/qemu-guest-agent.service
%{_udevdir}/99-qemu-guest-agent.rules
%endif

%files img
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%if 0%{?have_docs}
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*
%endif

%if 0%{?have_curl}
%files block-curl
%{_libdir}/qemu/block-curl.so
%endif

%if 0%{?have_dmg}
%files block-dmg
%{_libdir}/qemu/block-dmg-bz2.so
%endif

%if 0%{?have_gluster}
%files block-gluster
%{_libdir}/qemu/block-gluster.so
%endif

%if 0%{?have_iscsi}
%files block-iscsi
%{_libdir}/qemu/block-iscsi.so
%endif

%if 0%{?have_nfs}
%files block-nfs
%{_libdir}/qemu/block-nfs.so
%endif

%if 0%{?have_rbd}
%files block-rbd
%{_libdir}/qemu/block-rbd.so
%endif

%if 0%{?have_ssh}
%files block-ssh
%{_libdir}/qemu/block-ssh.so
%endif

%files -n ivshmem-tools
%{_bindir}/ivshmem-client
%{_bindir}/ivshmem-server


%if %{have_kvm}
%files kvm
# Deliberately empty

%files kvm-core
# Deliberately empty
%endif

%if 0%{?have_user}
%files user
%{_bindir}/qemu-i386
%{_bindir}/qemu-x86_64
%{_bindir}/qemu-aarch64
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm
%{_bindir}/qemu-armeb
%{_bindir}/qemu-cris
%{_bindir}/qemu-hppa
%{_bindir}/qemu-m68k
%{_bindir}/qemu-microblaze
%{_bindir}/qemu-microblazeel
%{_bindir}/qemu-mips
%{_bindir}/qemu-mipsel
%{_bindir}/qemu-mips64
%{_bindir}/qemu-mips64el
%{_bindir}/qemu-mipsn32
%{_bindir}/qemu-mipsn32el
%{_bindir}/qemu-nios2
%{_bindir}/qemu-or1k
%{_bindir}/qemu-ppc
%{_bindir}/qemu-ppc64
%{_bindir}/qemu-ppc64abi32
%{_bindir}/qemu-ppc64le
%{_bindir}/qemu-s390x
%{_bindir}/qemu-sh4
%{_bindir}/qemu-sh4eb
%{_bindir}/qemu-sparc
%{_bindir}/qemu-sparc32plus
%{_bindir}/qemu-sparc64

%{_datadir}/systemtap/tapset/qemu-i386.stp
%{_datadir}/systemtap/tapset/qemu-i386-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-x86_64.stp
%{_datadir}/systemtap/tapset/qemu-x86_64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-aarch64.stp
%{_datadir}/systemtap/tapset/qemu-aarch64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-alpha.stp
%{_datadir}/systemtap/tapset/qemu-alpha-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-arm.stp
%{_datadir}/systemtap/tapset/qemu-arm-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-armeb.stp
%{_datadir}/systemtap/tapset/qemu-armeb-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-cris.stp
%{_datadir}/systemtap/tapset/qemu-cris-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-hppa.stp
%{_datadir}/systemtap/tapset/qemu-hppa-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-m68k.stp
%{_datadir}/systemtap/tapset/qemu-m68k-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-microblaze.stp
%{_datadir}/systemtap/tapset/qemu-microblaze-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-microblazeel.stp
%{_datadir}/systemtap/tapset/qemu-microblazeel-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mips.stp
%{_datadir}/systemtap/tapset/qemu-mips-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mipsel.stp
%{_datadir}/systemtap/tapset/qemu-mipsel-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mips64.stp
%{_datadir}/systemtap/tapset/qemu-mips64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mips64el.stp
%{_datadir}/systemtap/tapset/qemu-mips64el-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32el.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32el-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-nios2.stp
%{_datadir}/systemtap/tapset/qemu-nios2-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-or1k.stp
%{_datadir}/systemtap/tapset/qemu-or1k-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-ppc.stp
%{_datadir}/systemtap/tapset/qemu-ppc-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-ppc64.stp
%{_datadir}/systemtap/tapset/qemu-ppc64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-ppc64abi32.stp
%{_datadir}/systemtap/tapset/qemu-ppc64abi32-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-ppc64le.stp
%{_datadir}/systemtap/tapset/qemu-ppc64le-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-s390x.stp
%{_datadir}/systemtap/tapset/qemu-s390x-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-sh4.stp
%{_datadir}/systemtap/tapset/qemu-sh4-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-sparc.stp
%{_datadir}/systemtap/tapset/qemu-sparc-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-sparc64.stp
%{_datadir}/systemtap/tapset/qemu-sparc64-simpletrace.stp

%files user-binfmt
%{_exec_prefix}/lib/binfmt.d/qemu-*-dynamic.conf

%if %{user_static}
%files user-static
%{_exec_prefix}/lib/binfmt.d/qemu-*-static.conf
%{_bindir}/qemu-i386-static
%{_bindir}/qemu-x86_64-static
%{_bindir}/qemu-aarch64-static
%{_bindir}/qemu-alpha-static
%{_bindir}/qemu-arm-static
%{_bindir}/qemu-armeb-static
%{_bindir}/qemu-cris-static
%{_bindir}/qemu-hppa-static
%{_bindir}/qemu-m68k-static
%{_bindir}/qemu-microblaze-static
%{_bindir}/qemu-microblazeel-static
%{_bindir}/qemu-mips-static
%{_bindir}/qemu-mipsel-static
%{_bindir}/qemu-mips64-static
%{_bindir}/qemu-mips64el-static
%{_bindir}/qemu-mipsn32-static
%{_bindir}/qemu-mipsn32el-static
%{_bindir}/qemu-nios2-static
%{_bindir}/qemu-or1k-static
%{_bindir}/qemu-ppc-static
%{_bindir}/qemu-ppc64-static
%{_bindir}/qemu-ppc64abi32-static
%{_bindir}/qemu-ppc64le-static
%{_bindir}/qemu-s390x-static
%{_bindir}/qemu-sh4-static
%{_bindir}/qemu-sh4eb-static
%{_bindir}/qemu-sparc-static
%{_bindir}/qemu-sparc32plus-static
%{_bindir}/qemu-sparc64-static

%{_datadir}/systemtap/tapset/qemu-i386-static.stp
%{_datadir}/systemtap/tapset/qemu-i386-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-x86_64-static.stp
%{_datadir}/systemtap/tapset/qemu-x86_64-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-aarch64-static.stp
%{_datadir}/systemtap/tapset/qemu-aarch64-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-alpha-static.stp
%{_datadir}/systemtap/tapset/qemu-alpha-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-arm-static.stp
%{_datadir}/systemtap/tapset/qemu-arm-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-armeb-static.stp
%{_datadir}/systemtap/tapset/qemu-armeb-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-cris-static.stp
%{_datadir}/systemtap/tapset/qemu-cris-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-hppa-static.stp
%{_datadir}/systemtap/tapset/qemu-hppa-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-m68k-static.stp
%{_datadir}/systemtap/tapset/qemu-m68k-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-microblaze-static.stp
%{_datadir}/systemtap/tapset/qemu-microblaze-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-microblazeel-static.stp
%{_datadir}/systemtap/tapset/qemu-microblazeel-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-mips-static.stp
%{_datadir}/systemtap/tapset/qemu-mips-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-mipsel-static.stp
%{_datadir}/systemtap/tapset/qemu-mipsel-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-mips64-static.stp
%{_datadir}/systemtap/tapset/qemu-mips64-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-mips64el-static.stp
%{_datadir}/systemtap/tapset/qemu-mips64el-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32-static.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32el-static.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32el-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-nios2-static.stp
%{_datadir}/systemtap/tapset/qemu-nios2-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-or1k-static.stp
%{_datadir}/systemtap/tapset/qemu-or1k-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc64-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc64-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc64abi32-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc64abi32-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc64le-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc64le-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-s390x-static.stp
%{_datadir}/systemtap/tapset/qemu-s390x-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-sh4-static.stp
%{_datadir}/systemtap/tapset/qemu-sh4-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb-static.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-sparc-static.stp
%{_datadir}/systemtap/tapset/qemu-sparc-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus-static.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-sparc64-static.stp
%{_datadir}/systemtap/tapset/qemu-sparc64-simpletrace-static.stp
%endif
%endif

%files system-x86
# Deliberately empty

%if 0%{?have_x86_emul}
%files system-x86-core
%{_bindir}/qemu-system-i386
%{_bindir}/qemu-system-x86_64
%{_datadir}/systemtap/tapset/qemu-system-i386*.stp
%{_datadir}/systemtap/tapset/qemu-system-x86_64*.stp
%if 0%{?have_docs}
%{_mandir}/man1/qemu-system-i386.1*
%{_mandir}/man1/qemu-system-x86_64.1*
%endif
%endif

%if 0%{?need_qemu_kvm}
%{_bindir}/qemu-kvm
%{_mandir}/man1/qemu-kvm.1*
%endif

%{_datadir}/%{name}/acpi-dsdt.aml
%{_datadir}/%{name}/bios.bin
%{_datadir}/%{name}/bios-256k.bin
%{_datadir}/%{name}/sgabios.bin
%{_datadir}/%{name}/linuxboot.bin
%{_datadir}/%{name}/linuxboot_dma.bin
%{_datadir}/%{name}/multiboot.bin
%{_datadir}/%{name}/kvmvapic.bin
%ifarch %{ix86} x86_64
%{?kvm_files:}
%endif


%if 0%{?have_all_emul}
%files system-alpha
# Deliberately empty

%files system-alpha-core
%{_bindir}/qemu-system-alpha
%{_datadir}/systemtap/tapset/qemu-system-alpha*.stp
%{_mandir}/man1/qemu-system-alpha.1*
%{_datadir}/%{name}/palcode-clipper


%files system-arm
# Deliberately empty

%files system-arm-core
%{_bindir}/qemu-system-arm
%{_datadir}/systemtap/tapset/qemu-system-arm*.stp
%{_mandir}/man1/qemu-system-arm.1*
%ifarch armv7hl
%{?kvm_files:}
%endif


%files system-mips
# Deliberately empty

%files system-mips-core
%{_bindir}/qemu-system-mips
%{_bindir}/qemu-system-mipsel
%{_bindir}/qemu-system-mips64
%{_bindir}/qemu-system-mips64el
%{_datadir}/systemtap/tapset/qemu-system-mips*.stp
%{_mandir}/man1/qemu-system-mips.1*
%{_mandir}/man1/qemu-system-mipsel.1*
%{_mandir}/man1/qemu-system-mips64el.1*
%{_mandir}/man1/qemu-system-mips64.1*
%ifarch %{mips}
%{?kvm_files:}
%endif


%files system-cris
# Deliberately empty

%files system-cris-core
%{_bindir}/qemu-system-cris
%{_datadir}/systemtap/tapset/qemu-system-cris*.stp
%{_mandir}/man1/qemu-system-cris.1*


%files system-lm32
# Deliberately empty

%files system-lm32-core
%{_bindir}/qemu-system-lm32
%{_datadir}/systemtap/tapset/qemu-system-lm32*.stp
%{_mandir}/man1/qemu-system-lm32.1*


%files system-m68k
# Deliberately empty

%files system-m68k-core
%{_bindir}/qemu-system-m68k
%{_datadir}/systemtap/tapset/qemu-system-m68k*.stp
%{_mandir}/man1/qemu-system-m68k.1*


%files system-microblaze
# Deliberately empty

%files system-microblaze-core
%{_bindir}/qemu-system-microblaze
%{_bindir}/qemu-system-microblazeel
%{_datadir}/systemtap/tapset/qemu-system-microblaze*.stp
%{_mandir}/man1/qemu-system-microblaze.1*
%{_mandir}/man1/qemu-system-microblazeel.1*
%{_datadir}/%{name}/petalogix*.dtb


%files system-or1k
# Deliberately empty

%files system-or1k-core
%{_bindir}/qemu-system-or1k
%{_datadir}/systemtap/tapset/qemu-system-or1k*.stp
%{_mandir}/man1/qemu-system-or1k.1*


%files system-s390x
# Deliberately empty

%files system-s390x-core
%{_bindir}/qemu-system-s390x
%{_datadir}/systemtap/tapset/qemu-system-s390x*.stp
%{_mandir}/man1/qemu-system-s390x.1*
%{_datadir}/%{name}/s390-ccw.img
%ifarch s390x
%{?kvm_files:}
%{_sysconfdir}/sysctl.d/50-kvm-s390x.conf
%endif


%files system-sh4
# Deliberately empty

%files system-sh4-core
%{_bindir}/qemu-system-sh4
%{_bindir}/qemu-system-sh4eb
%{_datadir}/systemtap/tapset/qemu-system-sh4*.stp
%{_mandir}/man1/qemu-system-sh4.1*
%{_mandir}/man1/qemu-system-sh4eb.1*


%files system-sparc
# Deliberately empty

%files system-sparc-core
%{_bindir}/qemu-system-sparc
%{_bindir}/qemu-system-sparc64
%{_datadir}/systemtap/tapset/qemu-system-sparc*.stp
%{_mandir}/man1/qemu-system-sparc.1*
%{_mandir}/man1/qemu-system-sparc64.1*
%{_datadir}/%{name}/QEMU,tcx.bin
%{_datadir}/%{name}/QEMU,cgthree.bin


%files system-ppc
# Deliberately empty

%files system-ppc-core
%{_bindir}/qemu-system-ppc
%{_bindir}/qemu-system-ppc64
%{_bindir}/qemu-system-ppcemb
%{_datadir}/systemtap/tapset/qemu-system-ppc*.stp
%{_mandir}/man1/qemu-system-ppc.1*
%{_mandir}/man1/qemu-system-ppc64.1*
%{_mandir}/man1/qemu-system-ppcemb.1*
%{_datadir}/%{name}/bamboo.dtb
%{_datadir}/%{name}/ppc_rom.bin
%{_datadir}/%{name}/skiboot.lid
%{_datadir}/%{name}/spapr-rtas.bin
%{_datadir}/%{name}/u-boot.e500
%ifarch %{power64}
%{?kvm_files:}
%{_sysconfdir}/security/limits.d/95-kvm-ppc64-memlock.conf
%endif


%files system-unicore32
# Deliberately empty

%files system-unicore32-core
%{_bindir}/qemu-system-unicore32
%{_datadir}/systemtap/tapset/qemu-system-unicore32*.stp
%{_mandir}/man1/qemu-system-unicore32.1*


%files system-xtensa
# Deliberately empty

%files system-xtensa-core
%{_bindir}/qemu-system-xtensa
%{_bindir}/qemu-system-xtensaeb
%{_datadir}/systemtap/tapset/qemu-system-xtensa*.stp
%{_mandir}/man1/qemu-system-xtensa.1*
%{_mandir}/man1/qemu-system-xtensaeb.1*


%files system-moxie
# Deliberately empty

%files system-moxie-core
%{_bindir}/qemu-system-moxie
%{_datadir}/systemtap/tapset/qemu-system-moxie*.stp
%{_mandir}/man1/qemu-system-moxie.1*


%files system-aarch64
# Deliberately empty

%files system-aarch64-core
%{_bindir}/qemu-system-aarch64
%{_datadir}/systemtap/tapset/qemu-system-aarch64*.stp
%{_mandir}/man1/qemu-system-aarch64.1*
%ifarch aarch64
%{?kvm_files:}
%endif


%files system-tricore
# Deliberately empty

%files system-tricore-core
%{_bindir}/qemu-system-tricore
%{_datadir}/systemtap/tapset/qemu-system-tricore*.stp
%{_mandir}/man1/qemu-system-tricore.1*


%files system-nios2
# Deliberately empty

%files system-nios2-core
%{_bindir}/qemu-system-nios2
%{_datadir}/systemtap/tapset/qemu-system-nios2*.stp
%{_mandir}/man1/qemu-system-nios2.1*
%endif


%changelog
* Tue Apr 25 2017 Cole Robinson <crobinso@redhat.com> - 2:2.9.0-1
- Rebase to qemu-2.9.0 GA

* Thu Apr 13 2017 Cole Robinson <crobinso@redhat.com> - 2:2.9.0-0.2-rc4
- Rebase to qemu-2.9.0-rc4
- Fix ipxe rom links for aarch64

* Sat Apr 08 2017 Richard W.M. Jones <rjones@redhat.com> - 2:2.9.0-0.2-rc3
- Backport upstream fix for assertion when copy-on-read=true (RHBZ#1439922).

* Tue Apr 04 2017 Cole Robinson <crobinso@redhat.com> - 2:2.9.0-0.1-rc3
- Rebase to qemu-2.9.0-rc3

* Wed Mar 29 2017 Cole Robinson <crobinso@redhat.com> - 2:2.9.0-0.1-rc2
- Rebase to qemu-2.9.0-rc2
- Add Obsoletes for or32-or1k rename (bz 1435016)
- spec: Pull in vga and pxe roms for ppc64 (bz 1431403)

* Tue Mar 21 2017 Cole Robinson <crobinso@redhat.com> - 2:2.9.0-0.1-rc1
- Rebase to qemu-2.9.0-rc1

* Wed Mar 15 2017 Cole Robinson <crobinso@redhat.com> - 2:2.9.0-0.1-rc0
* Rebase to qemu-2.9.0-rc0

* Mon Feb 20 2017 Daniel Berrange <berrange@redhat.com> - 2:2.8.0-2
- Drop texi2html BR, since QEMU switched to using makeinfo back in 2010

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.8.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 20 2016 Cole Robinson <crobinso@redhat.com> - 2:2.8.0-1
- Rebase to qemu-2.8.0 GA

* Mon Dec 12 2016 Cole Robinson <crobinso@redhat.com> - 2:2.8.0-0.3-rc3
- Rebase to qemu-2.8.0-rc3

* Mon Dec 05 2016 Cole Robinson <crobinso@redhat.com> - 2:2.8.0-0.2-rc2
- Rebuild to pick up changed libxen* sonames

* Mon Dec 05 2016 Cole Robinson <crobinso@redhat.com> - 2:2.8.0-0.1-rc2
- Rebase to qemu-2.8.0-rc2

* Mon Nov 28 2016 Paolo Bonzini <pbonzini@redhat.com> - 2:2.7.0-10
- Do not build aarch64 with -fPIC anymore (rhbz 1232499)

* Tue Nov 15 2016 Nathaniel McCallum <npmccallum@redhat.com> - 2:2.7.0-9
- Clean up binfmt.d configuration files

* Mon Nov 14 2016 Richard W.M. Jones <rjones@redhat.com> - 2:2.7.0-8
- Create subpackages for modularized qemu block drivers (RHBZ#1393688).
- Fix qemu-sanity-check.

* Tue Oct 25 2016 Cole Robinson <crobinso@redhat.com> - 2:2.7.0-7
- Fix PPC64 build with memlock file (bz #1387601)

* Wed Oct 19 2016 Bastien Nocera <bnocera@redhat.com> - 2:2.7.0-6
- Add "F" flag to static user emulators' binfmt, to make them
  available in containers (#1384615)
- Also fixes the path of those emulators in the binfmt configurations

* Wed Oct 19 2016 Cole Robinson <crobinso@redhat.com> - 2:2.7.0-5
- Fix nested PPC 'Unknown MMU model' error (bz #1374749)
- Fix flickering display with boxes + wayland VM (bz #1266484)
- Add ppc64 kvm memlock file (bz #1293024)

* Sat Oct 15 2016 Cole Robinson <crobinso@redhat.com> - 2:2.7.0-4
- CVE-2016-7155: pvscsi: OOB read and infinite loop (bz #1373463)
- CVE-2016-7156: pvscsi: infinite loop when building SG list (bz #1373480)
- CVE-2016-7156: pvscsi: infinite loop when processing IO requests (bz
  #1373480)
- CVE-2016-7170: vmware_vga: OOB stack memory access (bz #1374709)
- CVE-2016-7157: mptsas: invalid memory access (bz #1373505)
- CVE-2016-7466: usb: xhci memory leakage during device unplug (bz #1377838)
- CVE-2016-7423: scsi: mptsas: OOB access (bz #1376777)
- CVE-2016-7422: virtio: null pointer dereference (bz #1376756)
- CVE-2016-7908: net: Infinite loop in mcf_fec_do_tx (bz #1381193)
- CVE-2016-8576: usb: xHCI: infinite loop vulnerability (bz #1382322)
- CVE-2016-7995: usb: hcd-ehci: memory leak (bz #1382669)

* Mon Oct 10 2016 Hans de Goede <hdegoede@redhat.com> - 2:2.7.0-3
- Fix interrupt endpoints not working with network/spice USB redirection
  on guest with an emulated xhci controller (rhbz#1382331)

* Tue Sep 20 2016 Michal Toman <mtoman@fedoraproject.org> - 2:2.7.0-2
- Fix build on MIPS

* Thu Sep 08 2016 Cole Robinson <crobinso@redhat.com> - 2:2.7.0-1
- Rebase to qemu 2.7.0 GA

* Fri Aug 19 2016 Cole Robinson <crobinso@redhat.com> - 2:2.7.0-0.2.rc3
- Rebase to qemu 2.7.0-rc3

* Wed Aug 03 2016 Cole Robinson <crobinso@redhat.com> - 2:2.7.0-0.1.rc2
- Rebase to qemu 2.7.0-rc2

* Sat Jul 23 2016 Richard W.M. Jones <rjones@redhat.com> - 2:2.6.0-6
- Rebuild to attempt to fix '2:qemu-system-xtensa-2.6.0-5.fc25.x86_64 requires libxenctrl.so.4.6()(64bit)'

* Wed Jul 13 2016 Daniel Berrange <berrange@redhat.com> - 2:2.6.0-5
- Introduce qemu-user-static sub-RPM

* Wed Jun 22 2016 Cole Robinson <crobinso@redhat.com> - 2:2.6.0-4
- CVE-2016-4002: net: buffer overflow in MIPSnet (bz #1326083)
- CVE-2016-4952 scsi: pvscsi: out-of-bounds access issue
- CVE-2016-4964: scsi: mptsas infinite loop (bz #1339157)
- CVE-2016-5106: scsi: megasas: out-of-bounds write (bz #1339581)
- CVE-2016-5105: scsi: megasas: stack information leakage (bz #1339585)
- CVE-2016-5107: scsi: megasas: out-of-bounds read (bz #1339573)
- CVE-2016-4454: display: vmsvga: out-of-bounds read (bz #1340740)
- CVE-2016-4453: display: vmsvga: infinite loop (bz #1340744)
- CVE-2016-5126: block: iscsi: buffer overflow (bz #1340925)
- CVE-2016-5238: scsi: esp: OOB write (bz #1341932)
- CVE-2016-5338: scsi: esp: OOB r/w access (bz #1343325)
- CVE-2016-5337: scsi: megasas: information leakage (bz #1343910)
- Fix crash with -nodefaults -sdl (bz #1340931)
- Add deps on edk2-ovmf and edk2-aarch64

* Thu May 26 2016 Cole Robinson <crobinso@redhat.com> - 2:2.6.0-3
- CVE-2016-4020: memory leak in kvmvapic.c (bz #1326904)
- CVE-2016-4439: scsi: esb: OOB write #1 (bz #1337503)
- CVE-2016-4441: scsi: esb: OOB write #2 (bz #1337506)
- Fix regression installing windows 7 with qxl/vga (bz #1339267)
- Fix crash with aarch64 gic-version=host and accel=tcg (bz #1339977)

* Fri May 20 2016 Cole Robinson <crobinso@redhat.com> - 2:2.6.0-2
- Explicitly error if spice GL setup fails
- Fix monitor resizing with virgl (bz #1337564)
- Fix libvirt noise when introspecting qemu-kvm without hw virt

* Fri May 13 2016 Cole Robinson <crobinso@redhat.com> - 2:2.6.0-1
- Rebase to v2.6.0 GA

* Mon May 09 2016 Cole Robinson <crobinso@redhat.com> - 2:2.6.0-0.2.rc5
- Fix gtk UI crash when switching to monitor (bz #1333424)
- Fix sdl2 UI lockup lockup when switching to monitor
- Rebased to qemu-2.6.0-rc5

* Mon May 02 2016 Cole Robinson <crobinso@redhat.com> 2:2.6.0-0.2.rc4
- Rebased to version 2.6.0-rc4
- Fix test suite on big endian hosts (bz 1330174)

* Mon Apr 25 2016 Cole Robinson <crobinso@redhat.com> - 2:2.6.0-0.2.rc3
- Rebuild to pick up spice GL support

* Mon Apr 18 2016 Cole Robinson <crobinso@redhat.com> 2:2.6.0-0.1.rc3
- Rebased to version 2.6.0-rc3
- Fix s390 sysctl file install (bz 1327870)
- Adjust spice gl version check to expect F24 backported version

* Thu Apr 14 2016 Cole Robinson <crobinso@redhat.com> 2:2.6.0-0.1.rc2
- Rebased to version 2.6.0-rc2
- Fix GL deps (bz 1325966)
- Ship sysctl file to fix s390x kvm (bz 1290589)
- Fix FTBFS on s390 (bz 1326247)

* Thu Apr 07 2016 Cole Robinson <crobinso@redhat.com> - 2:2.6.0-0.1.rc1
- Rebased to version 2.6.0-rc1

* Thu Mar 17 2016 Cole Robinson <crobinso@redhat.com> - 2:2.5.0-11
- CVE-2016-2857: net: out of bounds read (bz #1309564)
- CVE-2016-2392: usb: null pointer dereference (bz #1307115)

* Thu Mar 17 2016 Cole Robinson <crobinso@redhat.com> - 2:2.5.0-10
- CVE-2016-2538: Integer overflow in usb module (bz #1305815)
- CVE-2016-2841: ne2000: infinite loop (bz #1304047)
- CVE-2016-2857 net: out of bounds read (bz #1309564)
- CVE-2016-2392 usb: null pointer dereference (bz #1307115)
- Fix external snapshot any more after active committing (bz #1300209)

* Wed Mar  9 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2:2.5.0-9
- Rebuild for tcmalloc ifunc issues on non x86 arches (see rhbz 1312462)

* Tue Mar  1 2016 Paolo Bonzini <pbonzini@redhat.com> 2:2.5.0-8
- Disable xfsctl, fallocate works fine in newer kernels (bz #1305512)

* Tue Mar  1 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2:2.5.0-7
- All Fedora arches have libseccomp support (ARMv7, aarch64, Power64, s390(x))

* Mon Feb 15 2016 Cole Robinson <crobinso@redhat.com> - 2:2.5.0-6
- CVE-2015-8619: Fix sendkey out of bounds (bz #1292757)
- CVE-2016-1981: infinite loop in e1000 (bz #1299995)
- Fix Out-of-bounds read in usb-ehci (bz #1300234, bz #1299455)
- CVE-2016-2197: ahci: null pointer dereference (bz #1302952)
- Fix gdbstub for VSX registers for ppc64 (bz #1304377)
- Fix qemu-img vmdk images to work with VMware (bz #1299185)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Cole Robinson <crobinso@redhat.com> - 2:2.5.0-4
- CVE-2015-8567: net: vmxnet3: host memory leakage (bz #1289818)
- CVE-2016-1922: i386: avoid null pointer dereference (bz #1292766)
- CVE-2015-8613: buffer overflow in megasas_ctrl_get_info (bz #1284008)
- CVE-2015-8701: Buffer overflow in tx_consume in rocker.c (bz #1293720)
- CVE-2015-8743: ne2000: OOB memory access in ioport r/w functions (bz
  #1294787)
- CVE-2016-1568: Use-after-free vulnerability in ahci (bz #1297023)
- Fix modules.d/kvm.conf example syntax (bz #1298823)

* Sat Jan 09 2016 Cole Robinson <crobinso@redhat.com> - 2:2.5.0-3
- Fix virtio 9p thread pool usage
- CVE-2015-8558: DoS by infinite loop in ehci_advance_state (bz #1291309)
- Re-add dist tag

* Thu Jan 7 2016 Paolo Bonzini <pbonzini@redhat.com> - 2:2.5.0-2
- add /etc/modprobe.d/kvm.conf
- add 0001-virtio-9p-use-accessor-to-get-thread-pool.patch

* Wed Dec 23 2015 Cole Robinson <crobinso@redhat.com> 2:2.5.0-1
- Rebased to version 2.5.0

* Tue Dec 08 2015 Cole Robinson <crobinso@redhat.com> 2:2.5.0-0.1.rc3
- Rebased to version 2.5.0-rc3

* Mon Nov 30 2015 Cole Robinson <crobinso@redhat.com> 2:2.5.0-0.1.rc2
- Rebased to version 2.5.0-rc2

* Fri Nov 20 2015 Cole Robinson <crobinso@redhat.com> 2:2.5.0-0.1.rc1
- Rebased to version 2.5.0-rc1

* Wed Nov 04 2015 Cole Robinson <crobinso@redhat.com> - 2:2.4.1-1
- Rebased to version 2.4.1

* Sun Oct 11 2015 Cole Robinson <crobinso@redhat.com> - 2:2.4.0.1-2
- Rebuild for xen 4.6

* Thu Oct 08 2015 Cole Robinson <crobinso@redhat.com> - 2:2.4.0.1-1
- Rebased to version 2.4.0.1
- CVE-2015-7295: virtio-net possible remote DoS (bz #1264393)
- drive-mirror: Fix coroutine reentrance (bz #1266936)

* Mon Sep 21 2015 Cole Robinson <crobinso@redhat.com> - 2:2.4.0-4
- CVE-2015-6815: net: e1000: infinite loop issue (bz #1260225)
- CVE-2015-6855: ide: divide by zero issue (bz #1261793)
- CVE-2015-5278: Infinite loop in ne2000_receive() (bz #1263284)
- CVE-2015-5279: Heap overflow vulnerability in ne2000_receive() (bz #1263287)

* Sun Sep 20 2015 Richard W.M. Jones <rjones@redhat.com> - 2:2.4.0-3
- Fix emulation of various instructions, required by libm in F22 ppc64 guests.

* Mon Aug 31 2015 Cole Robinson <crobinso@redhat.com> - 2:2.4.0-2
- CVE-2015-5255: heap memory corruption in vnc_refresh_server_surface (bz
  #1255899)

* Tue Aug 11 2015 Cole Robinson <crobinso@redhat.com> - 2:2.4.0-1
- Rebased to version 2.4.0
- Support for virtio-gpu, 2D only
- Support for virtio-based keyboard/mouse/tablet emulation
- x86 support for memory hot-unplug
- ACPI v5.1 table support for 'virt' board

* Sun Aug 09 2015 Cole Robinson <crobinso@redhat.com> - 2:2.4.0-0.2.rc4
- CVE-2015-3209: pcnet: multi-tmd buffer overflow in the tx path (bz #1230536)
- CVE-2015-3214: i8254: out-of-bounds memory access (bz #1243728)
- CVE-2015-5158: scsi stack buffer overflow (bz #1246025)
- CVE-2015-5154: ide: atapi: heap overflow during I/O buffer memory access (bz
  #1247141)
- CVE-2015-5165: rtl8139 uninitialized heap memory information leakage to
  guest (bz #1249755)
- CVE-2015-5166: BlockBackend object use after free issue (bz #1249758)
- CVE-2015-5745: buffer overflow in virtio-serial (bz #1251160)

* Tue Jul 14 2015 Cole Robinson <crobinso@redhat.com> 2:2.4.0-0.1-rc0
- Rebased to version 2.4.0-rc0

* Fri Jul  3 2015 Richard W.M. Jones <rjones@redhat.com> - 2:2.3.0-15
- Bump and rebuild.

* Fri Jul  3 2015 Daniel P. Berrange <berrange@redhat.com> - 2:2.3.0-14
- Use explicit --(enable,disable)-spice args (rhbz #1239102)

* Thu Jul  2 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2:2.3.0-13
- Build aarch64 with -fPIC (rhbz 1232499)

* Wed Jul 01 2015 Nick Clifton <nickc@redhat.com> - 2:2.3.0-12
- Disable stack protection for AArch64.  F23's GCC thinks that it is available but F23's glibc does not support it.

* Fri Jun 26 2015 Paolo Bonzini <pbonzini@redhat.com> - 2:2.3.0-10
- Rebuild for libiscsi soname bump

* Fri Jun 19 2015 Paolo Bonzini <pbonzini@redhat.com> - 2:2.3.0-10
- Re-enable tcmalloc on arm

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Dan Horák <dan[at]danny.cz> - 2:2.3.0-8
- gperftools not available on s390(x)

* Fri Jun 05 2015 Cole Robinson <crobinso@redhat.com> - 2:2.3.0-7
- CVE-2015-4037: insecure temporary file use in /net/slirp.c (bz #1222894)

* Mon Jun  1 2015 Daniel P. Berrange <berrange@redhat.com> - 2:2.3.0-6
- Disable tcmalloc on arm since it currently hangs (rhbz #1226806)
- Re-enable tests on arm

* Wed May 13 2015 Cole Robinson <crobinso@redhat.com> - 2:2.3.0-5
- Backport upstream 2.4 patch to link with tcmalloc, enable it
- CVE-2015-3456: (VENOM) fdc: out-of-bounds fifo buffer memory access (bz
  #1221152)

* Sun May 10 2015 Paolo Bonzini <pbonzini@redhat.com> 2:2.3.0-4
- Backport upstream 2.4 patch to link with tcmalloc, enable it
- Add -p1 to autopatch

* Wed May 06 2015 Cole Robinson <crobinso@redhat.com> 2:2.3.0-3
- Fix ksm.service (bz 1218814)

* Tue May  5 2015 Dan Horák <dan[at]danny.cz> - 2:2.3.0-2
- Require libseccomp only when built with it

* Tue Mar 24 2015 Cole Robinson <crobinso@redhat.com> - 2:2.3.0-1
- Rebased to version 2.3.0 GA
- Another attempt at fixing default /dev/kvm permissions (bz 950436)

* Tue Mar 24 2015 Cole Robinson <crobinso@redhat.com> - 2:2.3.0-0.5.rc3
- Drop unneeded kvm.modules
- Fix s390/ppc64 FTBFS (bz 1212328)

* Tue Mar 24 2015 Cole Robinson <crobinso@redhat.com> - 2:2.3.0-0.4.rc3
- Rebased to version 2.3.0-rc3

* Tue Mar 24 2015 Cole Robinson <crobinso@redhat.com> - 2:2.3.0-0.3.rc2
- Rebased to version 2.3.0-rc2
- Don't install ksm services as executable (bz #1192720)
- Skip hanging tests on s390 (bz #1206057)
- CVE-2015-1779 vnc: insufficient resource limiting in VNC websockets decoder
  (bz #1205051, bz #1199572)

* Tue Mar 24 2015 Cole Robinson <crobinso@redhat.com> - 2:2.3.0-0.2.rc1
- Rebased to version 2.3.0-rc1

* Sun Mar 22 2015 Cole Robinson <crobinso@redhat.com> - 2:2.3.0-0.1.rc0
- Rebased to version 2.3.0-rc0

* Tue Feb 17 2015 Richard W.M. Jones <rjones@redhat.com> - 2:2.2.0-7
- Add -fPIC flag to build to avoid
  'relocation R_X86_64_PC32 against undefined symbol' errors.
- Add a hopefully temporary hack so that -fPIC is used to build
  NSS files in libcacard.

* Wed Feb  4 2015 Richard W.M. Jones <rjones@redhat.com> - 2:2.2.0-5
- Add UEFI support for aarch64.

* Tue Feb  3 2015 Daniel P. Berrange <berrange@redhat.com> - 2:2.2.0-4
- Re-enable SPICE after previous build fixes circular dep

* Tue Feb  3 2015 Daniel P. Berrange <berrange@redhat.com> - 2:2.2.0-3
- Rebuild for changed xen soname
- Temporarily disable SPICE to break circular build-dep on libcacard
- Stop libcacard linking against the entire world

* Wed Jan 28 2015 Daniel P. Berrange <berrange@redhat.com> - 2:2.2.0-2
- Pass package information to configure
