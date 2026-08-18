# RetroDailyDriver

RetroDailyDriver is a reproducible, DietPi-based retro-computing appliance for
Raspberry Pi keyboard computers. The host is infrastructure: later milestones
will boot into a small machine selector and run a selected emulator fullscreen,
while keeping Linux administration separate.

## M0 status

M0 establishes the repository contracts, hardware and appliance profile
schemas, asset manifest format, DietPi/Debian provisioning foundation, and a
non-destructive diagnostic tool. It does **not** install or launch emulators,
ROMs, operating systems, or a graphical interface.

Initial hardware targets are Raspberry Pi 400, Raspberry Pi 500, and Raspberry
Pi 500+. Planned appliance families are Amiga with Amiberry, Atari with Hatari,
and Commodore 8-bit with VICE. The example personalities are A1200/AmigaOS 3.x,
Atari STE, and Commodore 64, but their emulator stacks are deferred.

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

## License

Project-authored code and documentation are licensed under the MIT License.
That license does not apply to user-supplied assets.
