Name:           nebula-overlay-networking
Version:        1.10.1
Release:        1%{?dist}
Summary:        A scalable overlay networking tool

License:        MIT
URL:            https://github.com/slackhq/nebula
Source0:        https://github.com/slackhq/nebula/releases/download/v%{version}/nebula-linux-amd64.tar.gz
Source1:        https://github.com/slackhq/nebula/raw/v%{version}/examples/config.yml
Source2:        https://github.com/slackhq/nebula/raw/v%{version}/LICENSE
Source3:        https://github.com/slackhq/nebula/raw/v%{version}/examples/service_scripts/nebula.service
Source4:        nebula.xml
Source5:        https://github.com/slackhq/nebula/raw/v%{version}/README.md

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
cp %{SOURCE5} .

%build
sed -i s@/usr/local/bin/nebula@%{_bindir}/nebula@ nebula.service

%install
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
	firewall-cmd --reload --quiet  # Required for firewall-cmd to pick up the added service file.
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
%{_sysconfdir}/nebula
%config(noreplace) %{_sysconfdir}/nebula/*
%config(noreplace) %{_sysconfdir}/firewalld/services/*
%license LICENSE
%doc README.md

%changelog
# LC_ALL=C date +'* %a %b %d %Y Håkon Løvdal <kode@denkule.no> - 1.10.x-1'
* Thu Jan 22 2026 Håkon Løvdal <kode@denkule.no> - 1.10.1-1
- Update to version 1.10.1.

* Sun Jan 04 2026 Håkon Løvdal <kode@denkule.no> - 1.10.0-1
- Update to version 1.10.0.

* Sun Jan 04 2026 Håkon Løvdal <kode@denkule.no> - 1.9.7-1
- Update to version 1.9.7.

* Sun Jan 04 2026 Håkon Løvdal <kode@denkule.no> - 1.9.6-1
- Update to version 1.9.6.

* Sat Dec  7 2024 Håkon Løvdal <kode@denkule.no> - 1.9.5-1
- Update to version 1.9.5.

* Wed Sep  4 2024 Håkon Løvdal <kode@denkule.no> - 1.9.3-1
- Update to version 1.9.3.

* Tue Jun  4 2024 Håkon Løvdal <kode@denkule.no> - 1.9.2-1
- Update to version 1.9.2.

* Tue Jun  4 2024 Håkon Løvdal <kode@denkule.no> - 1.9.1-1
- Update to version 1.9.1.

* Thu May  9 2024 Håkon Løvdal <kode@denkule.no> - 1.9.0-1
- Update to version 1.9.0.

* Tue Jan  9 2024 Håkon Løvdal <kode@denkule.no> - 1.8.2-1
- Update to version 1.8.2.

* Wed Dec 20 2023 Håkon Løvdal <kode@denkule.no> - 1.8.1-1
- Update to version 1.8.1.

* Fri Dec 08 2023 Håkon Løvdal <kode@denkule.no> - 1.8.0-1
- Update to version 1.8.0.

* Thu Jun 01 2023 Håkon Løvdal <kode@denkule.no> - 1.7.2-1
- Update to version 1.7.2.

* Thu Jun 01 2023 Håkon Løvdal <kode@denkule.no> - 1.7.1-1
- Update to version 1.7.1.

* Thu Jun 01 2023 Håkon Løvdal <kode@denkule.no> - 1.7.0-1
- Update to version 1.7.0.

* Mon Sep 26 2022 Håkon Løvdal <kode@denkule.no> - 1.6.1-1
- Update to version 1.6.1.

* Sun Aug 14 2022 Håkon Løvdal <kode@denkule.no> - 1.6.0-1
- Update to version 1.6.0.

* Fri May 27 2022 Håkon Løvdal <kode@denkule.no> - 1.5.2-2
- Fix bug in post install script that caused adding the firewall service to fail.

* Wed Dec 15 2021 Håkon Løvdal <kode@denkule.no> - 1.5.2-1
- Update to version 1.5.2.

* Sun Dec 12 2021 Håkon Løvdal <kode@denkule.no> - 1.5.0-1
- Update to version 1.5.0.

* Fri Oct 01 2021 Håkon Løvdal <kode@denkule.no> - 1.4.0-3
- Fix a couple of fedora-review issues.

* Tue Sep 07 2021 Håkon Løvdal <kode@denkule.no> - 1.4.0-2
- Add service restart support.
- Add firewall support.

* Mon Sep 06 2021 Håkon Løvdal <kode@denkule.no> - 1.4.0-1
- Initial version
