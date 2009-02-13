%define version		1.1.0
%define release		%mkrel 1

%define major		1
%define libname		%mklibname %{name} %{major}
%define libnamedev	%mklibname %{name} %{major} -d

Summary:	Edyuk - fully-featured, highly flexible IDE for Qt 4
Name:		edyuk
Version:	%{version}
Release:	%{release}
License:	GPLv3
Group:		Development/KDE and Qt
URL:		http://edyuk.org/
Source0:	http://download.tuxfamily.org/edyuk/%{name}-%{version}.tar.bz2
Patch1:		edyuk-1.1.0.desktop.patch.bz2
Patch2:		edyuk-1.1.0.qt4.5.patch.bz2
BuildRequires:	qt4-devel
Requires:	%{libname} = %{version}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
Edyuk is an Integrated Development Environment built with Qt4 and meant to
provide a light, fast and stable environment for rapid application development
in C++/Qt4. Thanks to plugins (see III) its scope can hopefully be extended to
any possible programming related task (e.g version control, issue tracking,
management of other project formats, support for other languages/toolkits...)

%package -n %{libname}
Summary:	Edyuk shared library
Group:		System/Libraries
License:	GPLv3
Provides:	lib%{name} = %{version}

%description -n %{libname}
Shared library for edyuk.

%package -n %{libnamedev}
Summary:	Edyuk development files
Group:		Development/KDE and Qt
License:	GPLv3
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}

%description -n %{libnamedev}
Development files needed to create edyuk plugins.


%prep		
%setup -q -n %{name}-%{version}
%patch1
%patch2 

%build
%qmake_qt4
# Can not used -j option included in %make 
%_make_bin

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall INSTALL_ROOT=%{buildroot}

%__install -m755 %{name}.bin %{buildroot}%{_bindir}

# Already defined in freedesktop.org.xml
rm -rf %{buildroot}%{_datadir}/mime/packages/%{name}.xml
rm -rf %{buildroot}%{_datadir}/icons/gnome
mv %{buildroot}%{_datadir}/icons/default.kde %{buildroot}%{_datadir}/icons/hicolor
rm -f %{buildroot}%{_libdir}/libedyuk.so{.1.0,.1,}
%__install -m755 lib%{name}.so.1.0.0 %{buildroot}%{_libdir}
ln -s lib%{name}.so.1.0.0 %{buildroot}%{_libdir}/lib%{name}.so
ln -s lib%{name}.so.1.0.0 %{buildroot}%{_libdir}/lib%{name}.so.1
ln -s lib%{name}.so.1.0.0 %{buildroot}%{_libdir}/lib%{name}.so.1.0

# Fixed permission
chmod 644 %{buildroot}%{_libdir}/qt4/include/Edyuk/*

%if %mdkversion < 200900
%post
%update_menus
%update_desktop_database
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_desktop_database
%clean_icon_cache hicolor
%endif

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGELOG.txt GPL.txt README.txt TODO.txt
%{_bindir}/%{name}*
%{_datadir}/%{name}
%{_datadir}/mimelnk/text/*.desktop
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%files -n %{libname}
%defattr(-,root,root,0755) 
%doc GPL.txt
%{_libdir}/lib%{name}.so.*

%files -n %{libnamedev}
%defattr(-,root,root,0755) 
%doc GPL.txt
%{_libdir}/qt4/include/Edyuk
%{_libdir}/qt4/mkspecs/features/*.prf
%{_libdir}/lib%{name}.so
