# RetroDailyDriver

RetroDailyDriver is a reproducible, DietPi-based personal microcomputer
appliance for Raspberry Pi keyboard computers. It emulates computers, not game
consoles. The host is infrastructure: later milestones will boot into a small
personality selector and run the selected computer environment fullscreen, while
keeping Linux administration separate.

This is deliberately not RetroPie, Batocera, a ROM browser, a cover-art game
launcher, or a game collection manager. Games are software used from within a
computer personality. The intended experience is that the Pi 400, Pi 500, or
Pi 500+ keyboard computer feels like the selected Amiga, Atari, Commodore,
Spectrum, MSX, or modern-retro machine.

## M0–M0.3 status

M0 establishes the repository contracts, hardware and appliance profile
schemas, asset manifest format, DietPi/Debian provisioning foundation, and a
non-destructive diagnostic tool. M0.1 generalizes family handling through a
declarative registry and adds Atari 8-bit, ZX Spectrum, and MSX profiles. M0.2
adds classic BBC/Apple II/Archimedes and modern-retro X16, MEGA65, Agon,
Neo6502, Foenix, Colour Maximite 2, and X65 families, plus Spectrum Next. It
does **not** install or launch emulators,
ROMs, operating systems, or a graphical interface.

M0.3 adds the authenticity-first principle, authentic/enhanced profile intent,
and capability/runtime-assessment policy. Performance advice does not silently
forbid a profile: `not_recommended` remains user-startable with acknowledgement.

Initial hardware targets are Raspberry Pi 400, Raspberry Pi 500, and Raspberry
Pi 500+. The first-class classic families are Amiga (Amiberry), Atari ST / TT /
Falcon (Hatari), Commodore 8-bit (VICE), Atari 8-bit (Atari800), ZX Spectrum
(Fuse), MSX (openMSX), BBC, Apple II, and Acorn Archimedes. Modern-retro
families are Commander X16, MEGA65, Agon, Neo6502, Foenix F256, Colour Maximite
2, and X65. Emulator stacks remain deferred: X16 and MEGA65 have candidates,
the original six named emulators are candidates, and unresolved families have
no selected emulator.

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

The authenticity-first experience contract, display/input/audio/storage goals,
capability assessment semantics, and user-override policy are documented in
[`docs/EXPERIENCE.md`](docs/EXPERIENCE.md).

Family metadata and menu ordering are declarative in
[`families/registry.yml`](families/registry.yml). Adding a family requires a
registry entry and profiles, not a Python allow-list or launcher code change.

The registry also records classic versus `modern_retro` classification,
microcomputer experience defaults, and emulator qualification state. A doctor
`PASS` means profile/configuration integrity only; `candidate` means an emulator
has been identified but not qualified; `qualified` requires recorded evidence.
M0.3 still marks no emulator qualified and makes no measured performance claim.

## License

Project-authored code and documentation are licensed under the MIT License.
That license does not apply to user-supplied assets.
