%define name	oprofile
%define version	0.9.3
%define rel	6

Summary:	Transparent low-overhead system-wide profiler
Name:		%name
Version:	%version
Release:	%mkrel %rel
Group:		Development/Other
License:	GPL
URL:		http://oprofile.sourceforge.net/
Source:		http://prdownloads.sourceforge.net/%name/%name-%version.tar.bz2
Source11:	%name-16.png
Source12:	%name-32.png
Source13:	%name-48.png
Patch0:		oprofile-0.9.3-fix-build.patch
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	binutils-devel qt3-devel libpopt-devel gettext-devel

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

%prep
%setup -q
%patch0 -p0

%build
export QTDIR=%{_prefix}/lib/qt3
export QTLIB=$QTDIR/%{_lib}
%configure2_5x --with-kernel-support --with-qt-libraries=$QTLIB
%make

%install
rm -rf %{buildroot}
%makeinstall
rm -f %{buildroot}%{_datadir}/doc/%{name}/*.html

# bug in makefile
mv %{buildroot}%{_datadir}/stl.pat %{buildroot}%{_datadir}/%{name}

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
%{_datadir}/%{name}
%{_mandir}/man1/op*

%files gui
%defattr(-,root,root)
%doc COPYING
%{_bindir}/oprof_start
%{_sbindir}/oprof_start
%{_datadir}/applications/mandriva-*.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
