# Summary

[Nebula](https://nebula.defined.net/docs/) is a networking overlay tool
made by [Slack](https://github.com/slackhq/nebula). This repo is creating
[rpm packages](https://copr.fedorainfracloud.org/coprs/hlovdal/nebula-overlay-networking/)
of it.

[![Copr build status](https://copr.fedorainfracloud.org/coprs/hlovdal/nebula-overlay-networking/package/nebula-overlay-networking/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/hlovdal/nebula-overlay-networking/package/nebula-overlay-networking/)

This repository is primarily created for my own personal use, but if it is
useful for others, good on them.

# Details

Nebula is a [networking overlay tool](https://slack.engineering/introducing-nebula-the-open-source-global-overlay-network-from-slack/)
that lets you connect computers in a way similar to [Tinc](https://www.tinc-vpn.org/)
or [Wireguard](https://www.wireguard.com/).

There exist multiple other projects that are also named "nebula", so choosing
"nebula-overlay-networking" to avoid naming collisions as well as being a bit
more descriptive than just "nebula".

## Rpm package

For now I lazily download and use the precompiled upstream release binaries.
Long term I should maybe compile the go source files properly, however as a
benefit it is now trivially simple to verify that the binaries I provide in
this package are 100% exactly the same as the upstream project releases.

The package installs the binaries obviously. In addition it contains

- a `nebula` firewalld service definition (UDP 4242) that is permanently added
to the `public` zone on package install and removed on package removal.
- a systemd service file. The service is not started or enabled on package
install (it does not make sense to do that before configuration is done).

### Installation example

```bash
dnf install nebula-overlay-networking
cd /etc/nebula
${EDITOR:-nano} config.yml

git add config.yml                 # Of course you are using etckeeper, right?
git commit -m "Configured nebula"

systemctl start nebula
systemctl status nebula
systemctl enable nebula

git add /etc/systemd/system/multi-user.target.wants/nebula.service
git commit -m "Enabled nebula service" -m "systemctl enable nebula"
```
