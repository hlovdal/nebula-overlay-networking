Name:           nebula-overlay-networking
Version:        1.4.0
Release:        2%{?dist}
Summary:        A scalable overlay networking tool

License:        MIT
URL:            https://github.com/slackhq/nebula
Source0:        https://github.com/slackhq/nebula/releases/download/v%{version}/nebula-linux-amd64.tar.gz
Source1:        https://github.com/slackhq/nebula/raw/v%{version}/examples/config.yml
Source2:        https://github.com/slackhq/nebula/raw/v%{version}/LICENSE
Source3:        https://github.com/slackhq/nebula/raw/v%{version}/examples/service_scripts/nebula.service
Source4:	nebula.xml

%if 0%{?rhel} < 8
BuildRequires:  systemd
%else
BuildRequires:  systemd-rpm-macros
%endif
Requires:       firewalld

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
cp %{SOURCE4} .

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
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/firewalld/services
cp -a nebula.xml ${RPM_BUILD_ROOT}/%{_sysconfdir}/firewalld/services/.

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_syntax
%post
%systemd_post nebula.service
if [ $1 == 1 ]
then
	# First time install
	firewall-cmd --permanent --zone=public --add-service=nebula
	firewall-cmd --reload --quiet
fi
exit 0

%preun
%systemd_preun nebula.service
if [ $1 == 0 ]
then
	# Complete uninstall
	firewall-cmd --permanent --zone=public --remove-service=nebula
	firewall-cmd --reload --quiet
fi
exit 0

%postun
%systemd_postun_with_restart nebula.service
exit 0


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_unitdir}/*
%config(noreplace) %{_sysconfdir}/nebula/*
%config(noreplace) %{_sysconfdir}/firewalld/services/*
%license LICENSE

%changelog
* Tue Sep 07 2021 Håkon Løvdal <kode@denkule.no> - 1.4.0-2
- Add service restart support.
- Add firewall support.

* Mon Sep 06 2021 Håkon Løvdal <kode@denkule.no> - 1.4.0-1
- Initial version
