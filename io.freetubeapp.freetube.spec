%global debug_package %{nil}
%define app FreeTube
%define _app freetube
%define app_id io.freetubeapp.FreeTube
%define dev FreeTubeApp
%define release_tag ${TAG} # this line gets updated automatically by Github Actions

Name: %{app_id}
Version: %{release_tag}
Release: 2%{?dist}
Summary: Open source desktop YouTube player built with privacy in mind.
License: AGPL-3.0-only

URL: https://github.com/%{dev}/%{app}
Source0: https://github.com/%{dev}/%{app}/archive/refs/tags/v%{version}-beta.tar.gz

BuildRequires: nodejs
BuildRequires: yarnpkg
BuildRequires: libxcrypt-compat
BuildRequires: npm
BuildRequires: git

ExclusiveArch:  x86_64

Obsoletes:      %{_app} <= %{version}

%description
Open source desktop YouTube player built with privacy in mind.

%prep
%autosetup -n %{_builddir}/%{app}-%{version}-beta -p1

sed -i "s/targets = Platform.LINUX.*/targets = Platform.LINUX.createTarget(['dir'], arch)/" "%{_builddir}/%{app}-%{version}-beta/_scripts/build.js"

# create a .desktop file
cat << EOF > %{app_id}.desktop
[Desktop Entry]
Name=%{app_id}
Exec=%{app_id} %U
Terminal=false
Type=Application
Icon=%{app_id}
StartupWMClass=%{app_id}
Comment=An open source desktop YouTube player built with privacy in mind.
MimeType=x-scheme-handler/%{app_id};
Categories=Network;
EOF

%build
yarn install
yarn run build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/%{app_id}
mkdir -p %{buildroot}/%{_datadir}/applications
mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/scalable/apps
mkdir -p %{buildroot}/%{_datadir}/licenses/%{app_id}

cp -r %{_builddir}/%{app}-%{version}-beta/build/linux-unpacked/* %{buildroot}/%{_libdir}/%{app_id}
cp %{_builddir}/%{app}-%{version}-beta/LICENSE %{buildroot}/%{_datadir}/licenses/%{app_id}
ln -srf %{_libdir}/%{app_id}/%{_app} %{buildroot}%{_bindir}/%{app_id}

install -Dm644 %{app_id}.desktop %{buildroot}%{_datadir}/applications/%{app_id}.desktop
install -Dm644 %{_builddir}/%{app}-%{version}-beta/_icons/icon.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{app_id}.svg

%files
%{_datadir}/licenses/%{app_id}/LICENSE
%{_bindir}/%{app_id}
%{_libdir}/%{app_id}
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{app_id}.svg

%changelog
%autochangelog
