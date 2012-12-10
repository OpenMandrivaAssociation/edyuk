%define major		1
%define libname		%mklibname %{name} %{major}
%define libnamedev	%mklibname %{name} %{major} -d

Summary:	Edyuk - fully-featured, highly flexible IDE for Qt 4
Name:		edyuk
Version:	1.1.0
Release:	5
License:	GPLv3
Group:		Development/KDE and Qt
URL:		http://edyuk.org/
Source0:	http://download.tuxfamily.org/edyuk/%{name}-%{version}.tar.bz2
Patch1:		edyuk-1.1.0.desktop.patch.bz2
Patch2:		edyuk-1.1.0.qt4.5.patch.bz2
Patch3:		edyuk-1.1.0.version.patch.bz2
BuildRequires:	qt4-devel
Requires:	%{libname} = %{version}-%{release}

%description
Edyuk is an Integrated Development Environment built with Qt4 and meant to
provide a light, fast and stable environment for rapid application development
in C++/Qt4. Thanks to plugins (see III) its scope can hopefully be extended to
any possible programming related task (e.g version control, issue tracking,
management of other project formats, support for other languages/toolkits...)

%package -n %{libname}
Summary:	Edyuk shared library
Group:		System/Libraries

%description -n %{libname}
Shared library for edyuk.

%package -n %{libnamedev}
Summary:	Edyuk development files
Group:		Development/KDE and Qt
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{libnamedev}
Development files needed to create edyuk plugins.

%prep
%setup -q
%patch1 -p0
%patch2 -p0
%patch3 -p0

%build
%qmake_qt4
# Can not used -j option included in %make
make

%install
%makeinstall INSTALL_ROOT=%{buildroot}

%__install -d -m755 %{buildroot}%{_libdir}
%__install -m755 %{name}.bin %{buildroot}%{_bindir}
%__install -m755 -p libedyuk.so %{buildroot}%{_libdir}

# Already defined in freedesktop.org.xml
rm -rf %{buildroot}%{_datadir}/mime/packages/%{name}.xml
rm -rf %{buildroot}%{_datadir}/icons/gnome
mv %{buildroot}%{_datadir}/icons/default.kde %{buildroot}%{_datadir}/icons/hicolor

%files
%doc CHANGELOG.txt GPL.txt README.txt TODO.txt
%{_bindir}/%{name}*
%{_datadir}/%{name}
%{_datadir}/mimelnk/text/*.desktop
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{libnamedev}
%doc GPL.txt
%{_prefix}/lib/qt4/include/Edyuk
%{_prefix}/lib/qt4/mkspecs/features/*.prf
%{_libdir}/lib%{name}.so

