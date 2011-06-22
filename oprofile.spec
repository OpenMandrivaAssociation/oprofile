Summary:	Transparent low-overhead system-wide profiler
Name:		oprofile
Version:	0.9.6
Release:	%mkrel 5
Group:		Development/Other
License:	GPL
URL:		http://oprofile.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/%name/%name-%version.tar.gz
# Use -module -avoid-version for agents:
Patch2:		oprofile-agents-ldflags.patch
Patch10: oprofile-0.4-guess2.patch
Patch63: oprofile-0.7-libs.patch
Patch83: oprofile-0.9.5-xen.patch
#Patch104: oprofile-jvmpi-lgpl.patch
#Patch105: oprofile-0.9.5-timer.patch
Patch106: oprofile-sect.patch
Patch120: oprofile-iaperf.patch
Patch121: oprofile-nehalem.patch
Patch122: oprofile-amd.patch
Patch123: oprofile-westmere.patch
Patch124: oprofile-check.patch
Patch130: oprofile-unmutable.patch
Patch131: oprofile-qt4.patch
Patch132: oprofile-opcontrol.patch
Source11:	%name-16.png
Source12:	%name-32.png
Source13:	%name-48.png
BuildRequires:	binutils-devel qt4-devel libpopt-devel gettext-devel
BuildRequires:	java-rpmbuild
BuildRoot:	%{_tmppath}/%{name}-buildroot

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

%package	gui
Summary:	GUI for starting the OProfile profiler
Group:		Development/Other
Requires:	usermode usermode-consoleonly
Requires:	%{name} = %{version}

%description gui
OProfile is a system-wide profiler for Linux systems, capable of
profiling all running code at low overhead. OProfile is released
under the GNU GPL. 

This package provides a convenient QT GUI for starting the
profiler.

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
%patch2 -p1
%patch10 -p1 -b .guess2
%patch63 -p1 -b .libs
%patch83 -p1
%patch106 -p1 -b .sect
%patch120 -p1
%patch121 -p1
%patch122 -p1
%patch123 -p1
%patch124 -p1
%patch130 -p1
%patch131 -p1
%patch132 -p1

%build
# fixes build
touch NEWS AUTHORS # strange, autoreconf does not create these
autoreconf -if
%configure2_5x \
    --with-kernel-support \
    --enable-gui=qt4 \
    --with-java=%{java_home}

%make

%install
rm -rf %{buildroot}
%makeinstall_std
rm -f %{buildroot}%{_datadir}/doc/%{name}/*.html

# root dialog
install -d -m755 %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/oprof_start %{buildroot}%{_sbindir}/oprof_start
ln -s consolehelper %{buildroot}%{_bindir}/oprof_start

install -d -m755 %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=OProfile starter
Comment=Start OProfile profiler
Exec=%{_bindir}/oprof_start
Icon=%{name}
Terminal=false
Type=Application
Categories=Development;Profiling;Qt;
EOF

install -m644 %{SOURCE11} -D %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

rm %{buildroot}%{_libdir}/oprofile/*a

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post gui
%{update_menus}
%endif

%if %mdkversion < 200900
%postun gui
%{clean_menus}
%endif

%pre jit
%_pre_useradd oprofile "%{_var}/lib/oprofile" /bin/nologin

%postun jit
%_postun_userdel oprofile

%files
%defattr(-,root,root)
%doc README TODO COPYING ChangeLog* doc/*.html
%{_bindir}/opannotate
%{_bindir}/oparchive
%{_bindir}/opcontrol
%{_bindir}/opgprof
%{_bindir}/ophelp
%{_bindir}/opreport
%{_bindir}/oprofiled
%{_bindir}/opimport
%{_bindir}/opjitconv
%{_datadir}/%{name}
%{_mandir}/man1/op*

%files gui
%defattr(-,root,root)
%doc COPYING
%{_bindir}/oprof_start
%{_sbindir}/oprof_start
%{_datadir}/applications/mandriva-*.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

%files jit
%defattr(-,root,root)
%dir %{_libdir}/oprofile
%{_libdir}/oprofile/libjvmti_oprofile.so
%{_libdir}/oprofile/libopagent.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/opagent.h
%{_libdir}/oprofile/libopagent.so

