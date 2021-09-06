Name:           nebula-overlay-networking
Version:        1.4.0
Release:        1%{?dist}
Summary:        A scalable overlay networking tool

License:        MIT
URL:            https://github.com/slackhq/nebula
Source0:        https://github.com/slackhq/nebula/releases/download/v%{version}/nebula-linux-amd64.tar.gz
Source1:        https://github.com/slackhq/nebula/raw/v%{version}/examples/config.yml
Source2:        https://github.com/slackhq/nebula/raw/v%{version}/LICENSE
Source3:        https://github.com/slackhq/nebula/raw/v%{version}/examples/service_scripts/nebula.service

%description
Nebula is a scalable overlay networking tool with a focus on performance,
simplicity and security. It lets you seamlessly connect computers anywhere
in the world. Nebula is portable, and runs on Linux, OSX, Windows, iOS,
and Android. It can be used to connect a small number of computers,
but is also able to connect tens of thousands of computers.

Nebula incorporates a number of existing concepts like encryption,
security groups, certificates, and tunneling, and each of those individual
pieces existed before Nebula in various forms. What makes Nebula different
to existing offerings is that it brings all of these ideas together,
resulting in a sum that is greater than its individual parts.

%prep
tar zxvf %{SOURCE0}
cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .

%build
sed -i s@/usr/local/bin/nebula@%{_bindir}/nebula@ nebula.service

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}/%{_bindir}
cp -a nebula nebula-cert ${RPM_BUILD_ROOT}/%{_bindir}/.
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/nebula
cp -a config.yml ${RPM_BUILD_ROOT}/%{_sysconfdir}/nebula/.
mkdir -p ${RPM_BUILD_ROOT}/%{_unitdir}
cp -a nebula.service ${RPM_BUILD_ROOT}/%{_unitdir}/.


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_unitdir}/*
%config(noreplace) %{_sysconfdir}/nebula/*
%license LICENSE

%changelog
* Mon Sep 06 2021 Håkon Løvdal <kode@denkule.no> - 1.4.0-1
- Initial version
