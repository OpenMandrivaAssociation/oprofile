<<<<<<< HEAD
%define _disable_rebuild_configure 1

Summary:	Transparent low-overhead system-wide profiler
Name:		oprofile
Version:	1.1.0
Release:	3
=======
%bcond_with java

Summary:	Transparent low-overhead system-wide profiler
Name:		oprofile
Version:	1.2.0
Release:	1
>>>>>>> 3.0
License:	GPLv2+
Group:		Development/Other
Url:		http://oprofile.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
<<<<<<< HEAD
Patch0:		oprofile-verbose.patch
Source11:	%{name}-16.png
Source12:	%{name}-32.png
Source13:	%{name}-48.png
=======
# Use -module -avoid-version for agents:
Patch0:		oprofile-agents-ldflags.patch
%if %{with java}
>>>>>>> 3.0
BuildRequires:	jpackage-utils
BuildRequires:	java-devel
%endif
BuildRequires:	binutils-devel
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(popt)
<<<<<<< HEAD
Obsoletes:	oprofile-gui < %{version}-%{release}
=======
Obsoletes:	oprofile-gui  <= %{version}-%{release}
>>>>>>> 3.0

%description
OProfile is a system-wide profiler for Linux systems, capable of
profiling all running code at low overhead. OProfile is released
under the GNU GPL.

It consists of a kernel driver and a daemon for collecting sample
data, and several post-profiling tools for turning data into
information.

OProfile leverages the hardware performance counters of the CPU to
enable profiling of a wide variety of interesting statistics, which
can also be used for basic time-spent profiling. All code is
profiled: hardware and software interrupt handlers, kernel modules,
the kernel, shared libraries, and applications.

%files
%doc README TODO COPYING ChangeLog* doc/*.html
%{_bindir}/ocount
%{_bindir}/opannotate
%{_bindir}/oparchive
%{_bindir}/op-check-perfevents
%{_bindir}/operf
%{_bindir}/opgprof
%{_bindir}/ophelp
%{_bindir}/opreport
%{_bindir}/opimport
%{_bindir}/opjitconv
%{_datadir}/%{name}
%{_mandir}/man1/ocount.1*
%{_mandir}/man1/op*

<<<<<<< HEAD
#----------------------------------------------------------------------------

=======
>>>>>>> 3.0
%package jit
Summary:	Libraries for profiling Java and other JIT compiled code
Group:		Development/Other

%description jit
Libraries needed for profiling Java and other JIT compiled code.
For profiling Java code, you need to load
%{_libdir}/oprofile/libjvmti_oprofile.so
into the JVM as per the OProfile documentation.

%files jit
%dir %{_libdir}/oprofile
<<<<<<< HEAD
%{_libdir}/oprofile/libjvmti_oprofile.so.*
=======
%if %{with java}
%{_libdir}/oprofile/libjvmti_oprofile.so
%endif
>>>>>>> 3.0
%{_libdir}/oprofile/libopagent.so.*

%pre jit
%_pre_useradd oprofile "%{_var}/lib/oprofile" /bin/nologin

%postun jit
%_postun_userdel oprofile
#----------------------------------------------------------------------------

%package devel
Summary:	Development files for developing OProfile JIT agents
Group:		Development/Other
Requires:	%{name}-jit = %{EVRD}

%description devel
Header and development library symlink for libopagent, required for
compiling additional OProfile JIT agents.

%files devel
%{_includedir}/opagent.h
%{_libdir}/oprofile/libopagent.so
%{_libdir}/oprofile/libjvmti_oprofile.so

#----------------------------------------------------------------------------


%prep
%setup -q
%apply_patches

# fixes build
#touch NEWS AUTHORS INSTALL ChangeLog # strange, autoreconf does not create these
#autoreconf -if

%build
CXXFLAGS="%{optflags}"
CFLAGS="%{optflags}"
%configure \
<<<<<<< HEAD
=======
	--with-kernel-support \
%if %{with java}
>>>>>>> 3.0
	--with-java=%{java_home}
%endif

%make

%install
%makeinstall_std
rm -f %{buildroot}%{_datadir}/doc/%{name}/*.html

<<<<<<< HEAD
=======
# root dialog
install -d -m755 %{buildroot}%{_sbindir}
>>>>>>> 3.0
rm %{buildroot}%{_libdir}/oprofile/*a

