%global debug_package %{nil}
%define app FreeTube
%define _app freetube
%define dev FreeTubeApp
%define release_tag 0.23.8

Name: %{_app}
Version: %{release_tag}
Release: 1%{?dist}
Summary: Open source desktop YouTube player built with privacy in mind.
Group: System/GUI/Internet
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
echo %{app}-%{version}-beta
%autosetup -n %{_builddir}/%{app}-%{version}-beta -p1

# create a modified build.js file to only target rpm
cat << EOF > %{_builddir}/%{app}-%{version}-beta/_scripts/build.js
const os = require('os')
const builder = require('electron-builder')
const config = require('./ebuilder.config.js')

const Platform = builder.Platform
const args = process.argv
const Arch = builder.Arch

let arch = Arch.x64
targets = Platform.LINUX.createTarget(['rpm'], arch)

builder
    .build({
        targets,
        config,
        publish: 'never'
    })
    .then(m => {
        console.log(m)
    })
    .catch(e => {
        console.error(e)
    })
EOF

# create a .desktop file
cat << EOF > %{_app}.desktop
[Desktop Entry]
Name=FreeTube
Exec=freetube %U
Terminal=false
Type=Application
Icon=FreeTube
StartupWMClass=FreeTube
Comment=An open source desktop YouTube player built with privacy in mind.
MimeType=x-scheme-handler/freetube;
Categories=Network;
EOF

%build

# clean
rm -rf yarn.lock package-lock.json node_modules
yarn install
yarn run build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/%{app}
mkdir -p %{buildroot}/%{_datadir}/applications
mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/scalable/apps
mkdir -p %{buildroot}/%{_datadir}/licenses/%{app}

cp -r %{_builddir}/%{app}-%{version}-beta/build/linux-unpacked/* %{buildroot}/%{_libdir}/%{app}
cp %{_builddir}/%{app}-%{version}-beta/LICENSE %{buildroot}/%{_datadir}/licenses/%{app}
ln -srf %{_libdir}/%{app}/%{app} %{buildroot}%{_bindir}/%{_app}

install -Dm644 %{_app}.desktop %{buildroot}%{_datadir}/applications/%{app}.desktop
install -Dm644 %{_builddir}/%{app}-%{version}-beta/_icons/icon.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{app}.svg

%files
%{_datadir}/licenses/%{app}/LICENSE
%{_bindir}/%{_app}
%{_libdir}/%{app}
%{_datadir}/applications/%{app}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{app}.svg

%changelog
%autochangelog
