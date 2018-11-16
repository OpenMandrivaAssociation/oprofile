=====================================
THIS IS DEAD PACKAGE REPLACED BY PERF
=====================================

Summary:	Transparent low-overhead system-wide profiler
Name:		oprofile
Version:	1.3.0
Release:	2
Group:		Development/Other
License:	GPLv2+
URL:		http://oprofile.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/%name/%name-%version.tar.gz
# Use -module -avoid-version for agents:
Patch0:		oprofile-agents-ldflags.patch
BuildRequires:	binutils-devel
BuildRequires:	pkgconfig(popt)
BuildRequires:	gettext-devel
%ifnarch %arm %mips
BuildRequires:	java-devel
BuildRequires:	javapackages-tools
%endif

Obsoletes:	oprofile-gui < 0.9.9-5

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

%package	jit
Summary:	Libraries for profiling Java and other JIT compiled code
Group:		Development/Other

%description	jit
Libraries needed for profiling Java and other JIT compiled code.
For profiling Java code, you need to load
%{_libdir}/oprofile/libjvmti_oprofile.so
into the JVM as per the OProfile documentation.

%package	devel
Summary:	Development files for developing OProfile JIT agents
Group:		Development/Other
Requires:	%{name}-jit = %{version}

%description	devel
Header and development library symlink for libopagent, required for
compiling additional OProfile JIT agents.

%prep
%setup -q
%autopatch -p1

%build
./autogen.sh

%configure	\
		--with-java=%{_prefix}/lib/jvm/java
%make_build

%install
%make_install

rm -f %{buildroot}%{_datadir}/doc/%{name}/*.html

rm %{buildroot}%{_libdir}/oprofile/*a

%pre jit
%_pre_useradd oprofile "%{_var}/lib/oprofile" /bin/nologin

%postun jit
%_postun_userdel oprofile

%files
%doc README TODO COPYING ChangeLog* doc/*.html doc/*.xsd
%{_bindir}/ocount
%{_bindir}/op-check-perfevents
%{_bindir}/opannotate
%{_bindir}/oparchive
%{_bindir}/operf
%{_bindir}/opgprof
%{_bindir}/ophelp
%{_bindir}/opreport
%{_bindir}/opimport
%{_bindir}/opjitconv
%{_datadir}/%{name}/
%{_mandir}/man1/o*.1*

%files jit
%dir %{_libdir}/oprofile
%ifnarch %arm %mips
%{_libdir}/oprofile/libjvmti_oprofile.so
%endif
%{_libdir}/oprofile/libopagent.so.*

%files devel
%{_includedir}/opagent.h
%{_libdir}/oprofile/libopagent.so
