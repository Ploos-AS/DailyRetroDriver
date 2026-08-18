# RetroDailyDriver

RetroDailyDriver is a reproducible, DietPi-based retro-computing appliance for
Raspberry Pi keyboard computers. The host is infrastructure: later milestones
will boot into a small machine selector and run a selected emulator fullscreen,
while keeping Linux administration separate.

## M0 / M0.1 status

M0 establishes the repository contracts, hardware and appliance profile
schemas, asset manifest format, DietPi/Debian provisioning foundation, and a
non-destructive diagnostic tool. M0.1 generalizes family handling through a
declarative registry and adds Atari 8-bit, ZX Spectrum, and MSX profiles. It
does **not** install or launch emulators,
ROMs, operating systems, or a graphical interface.

Initial hardware targets are Raspberry Pi 400, Raspberry Pi 500, and Raspberry
Pi 500+. The six first-class platform families are Amiga (Amiberry), Atari ST /
TT / Falcon (Hatari), Commodore 8-bit (VICE), Atari 8-bit (Atari800), ZX
Spectrum (Fuse), and MSX (openMSX). Their canonical example profiles are
A1200, STE, C64, 800XL, 128K, and MSX2 respectively; emulator stacks remain
deferred.

DietPi is used as a small, Debian-compatible base whose package and service
surface can be provisioned declaratively. It is not intended to be the visible
desktop experience.

## Development and provisioning

Requirements are Python 3, PyYAML, and Ansible. On a development machine:

```bash
make check
make doctor
```

`make check` validates YAML models, runs unit tests, compiles Python sources,
performs the Ansible syntax check, and checks common repository hygiene.
`make doctor` diagnoses the current machine and may report expected failures on
a non-Raspberry Pi development host.

Review `ansible/inventory/hosts.example.yml`, copy it outside version control,
and provision a target with:

```bash
ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/provision.yml
```

The playbook is designed to be idempotent. It validates Debian-family systems,
creates the service identity and canonical runtime tree, resolves hardware by
capabilities, deploys public configuration, and verifies the result. Run it a
second time and inspect the recap for unintended changes.

## Asset policy

Proprietary ROMs, operating systems, disk images, and commercial software must
never be committed. Users provide software they are legally entitled to use;
manifests record provenance and SHA-256 identity. A checksum demonstrates
identity and integrity, **not** permission to distribute a work. See
[`docs/ASSETS.md`](docs/ASSETS.md).

Architecture, storage policy, and milestone acceptance criteria are documented
under [`docs/`](docs/).

Family metadata and menu ordering are declarative in
[`families/registry.yml`](families/registry.yml). Adding a family requires a
registry entry and profiles, not a Python allow-list or launcher code change.

## License

Project-authored code and documentation are licensed under the MIT License.
That license does not apply to user-supplied assets.
