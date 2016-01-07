Name:           dconf-editor
Version:        3.18.2
Release:        2
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
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  vala

%description
Graphical tool for editing the dconf configuration database.

%prep
%setup -q
%apply_patches

%build
%configure
%make
%install
%make_install

%find_lang dconf

%check
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
