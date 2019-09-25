%define api		1
%define dbusmajor	0
%define major		1
%define libname		%mklibname %{name} %{major}
%define libdbus		%mklibname %{name}-dbus %{api} %{dbusmajor}
%define develname	%mklibname -d %{name}
%define giolibname	%mklibname gio 2.0 0

%define busname		ca.desrt.dconf-editor

Name:           dconf-editor
Version:        3.34.1
Release:        1
Summary:        Configuration editor for dconf
Group:		System/Libraries
License:        LGPLv2+
URL:            https://wiki.gnome.org/Projects/dconf
Source0:        https://download.gnome.org/sources/dconf-editor/3.16/dconf-editor-%{version}.tar.xz
#Patch1:		0001-ro_syntax_error.patch
BuildRequires:  appstream-util
BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  pkgconfig(dconf)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  vala
BuildRequires:	vala-devel
BuildRequires:	gtk-doc
BuildRequires:	meson

Requires:	dbus
Requires:	dconf

%description
Graphical tool for editing the dconf configuration database.

%prep
%setup -q
%autopatch -p1

# fix invalid-desktopfile:
# missing semicolon (';') as trailing character for locale string list key "Keywords[ro]"
sed -i -e 's|configurări;configurație;setări"|configurări;configurație;setări;"|' po/ro.po

%build
%meson -Denable-gtk-doc=true
%meson_build

%install
%meson_install
#we need this beacuse ibus and gdm installs file there
install -d %{buildroot}%{_sysconfdir}/dconf/db
install -d %{buildroot}%{_sysconfdir}/dconf/profile

%find_lang dconf-editor

%check
%meson_test

%files -f dconf-editor.lang
%{_bindir}/dconf-editor
%{_mandir}/man1/dconf-editor.*
%{_datadir}/applications/%{busname}.desktop
%{_datadir}/bash-completion/completions/dconf-editor
%{_iconsdir}/hicolor/*/*/*dconf-editor*.*
%{_datadir}/metainfo/%{busname}.appdata.xml
%{_datadir}/dbus-1/services/%{busname}.service
%{_datadir}/glib-2.0/schemas/%{busname}.gschema.xml
