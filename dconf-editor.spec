Name:           dconf-editor
Version:        3.30.2
Release:        1
Summary:        Configuration editor for dconf
Group:		System/Libraries
License:        LGPLv2+
URL:            https://wiki.gnome.org/Projects/dconf
Source0:        https://download.gnome.org/sources/dconf-editor/3.16/dconf-editor-%{version}.tar.xz
Patch1:		0001-ro_syntax_error.patch
BuildRequires:  appstream-util
BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  pkgconfig(dconf)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  vala
BuildRequires:	meson

%description
Graphical tool for editing the dconf configuration database.

%prep
%setup -q
%apply_patches

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

appstream-util validate-relax --nonet $RPM_BUILD_ROOT%{_datadir}/appdata/ca.desrt.dconf-editor.appdata.xml
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/ca.desrt.dconf-editor.desktop

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%files -f dconf.lang
%doc COPYING
%{_bindir}/dconf-editor
%{_datadir}/appdata/ca.desrt.dconf-editor.appdata.xml
%{_datadir}/applications/ca.desrt.dconf-editor.desktop
%{_datadir}/dbus-1/services/ca.desrt.dconf-editor.service
%{_datadir}/glib-2.0/schemas/ca.desrt.dconf-editor.gschema.xml
%{_datadir}/icons/hicolor/*/apps/dconf-editor.png
%{_datadir}/icons/hicolor/scalable/apps/dconf-editor-symbolic.svg
%{_mandir}/man1/dconf-editor.1*
