# Architecture

## Microcomputer experience contract

RetroDailyDriver emulates computers, not game consoles. It is a multi-personality
personal computer appliance, not a ROM browser, console frontend, cover-art
launcher, or game collection manager. A future boot flow selects a personality
whose native environment then hides the host OS:

```text
POWER ON -> RetroDailyDriver -> personality -> native computer environment
```

The family registry carries shared experience defaults:

```yaml
experience_defaults:
  type: microcomputer
  boot_target: native_environment
  persistent_state: true
  game_frontend: false
  host_ui_hidden: true
```

Families and profiles can override these declaratively. Games remain expected
software, but they run inside the selected computer environment. Future
qualification must evaluate fullscreen operation, host-UI suppression, keyboard,
mouse, joystick/gamepad, audio, persistent disks/media/state, native filesystem
workflows, networking, serial/modem support, appropriate file exchange, clean
recovery, ARM64 support, and reproducible unattended installation.

## Separation of concerns

RetroDailyDriver treats DietPi as a managed host, not a desktop. Root-owned
declarative configuration lives in `/etc/retro-daily-driver`; versioned source
is deployed from `hardware/` and `profiles/`. Runtime data lives below
`/srv/retro-daily-driver`. Emulator processes will run as the unprivileged
`retro` service account and will not own host configuration.

The runtime tree separates asset inputs, immutable profile material, and mutable
state:

```text
/srv/retro-daily-driver/
├── assets/                 # user-owned inputs, indexed by manifests
├── profiles/               # materialized, reproducible profile data
├── state/{registered-family-id}/
├── media/{registered-family-id}/
├── backups/
├── logs/
└── reports/
```

The root is `root:retro` mode `0750`. Mutable child directories are
`retro:retro` mode `0750`; the reproducible `profiles/` directory is
`root:retro` mode `0750`. Nothing is world-writable. Host administrators may be
added to the separate `retro-admin` system group, which is an authorization hook
for later milestones and currently grants no sudo policy. The `retro` service
account is deliberately not a member of that group.

Configuration is reproducible and replaceable. `state/` and `media/` are mutable
and survive profile redeployment. `assets/` is user-managed but auditable by
manifest. Future sessions must distinguish immutable base configuration,
user-owned media, mutable computer state, transient session state, optional
snapshots, and backups. A file created on an Amiga Workbench disk or a BASIC
program saved on an X16 must remain available across launches. M0.3 defines the
contract but does not implement snapshots or backup/restore.

## Hardware abstraction

Each versioned hardware document contains identity matchers, SoC family,
baseline memory, storage preference, and named capabilities. Detection reads
firmware model data when available, maps aliases to a document, then consumers
choose behavior from capabilities such as `nvme` or
`high_performance_emulation`. Product names are detection inputs, never emulator
policy. A future board normally requires one new document and alias, not changes
throughout every appliance family.

The M0 playbook records detected architecture, model, resolved hardware ID, and
capabilities in `/etc/retro-daily-driver/detected-host.yml` for auditing. An
unknown model remains usable for diagnostics but is unresolved rather than
silently receiving guessed policy.

## Profile resolution

The declarative family registry in `families/registry.yml` is the
launcher-facing catalog. It supplies a stable family ID, display name,
classification, canonical profile, emulator qualification metadata, menu order,
and lifecycle status. Generic code consumes this registry; it does not contain
a family allow-list. M0.2 promotes BBC, Apple II, and Archimedes to classic
families and adds Commander X16, MEGA65, Agon, Neo6502, Foenix F256, Colour
Maximite 2, and X65 as modern-retro families. ZX Spectrum Next is a
modern-retro profile under Spectrum, while Spectrum 128K remains canonical.

An appliance profile declares its family and emulator boundary, virtual machine
parameters, display and input policy, asset references, mutable-state location,
and required/preferred hardware capabilities. Resolution will follow this order:

1. detect a host and produce its capability set;
2. load the family registry and validate a selected appliance profile;
3. reject missing `hardware_requirements.all` capabilities;
4. resolve logical assets through the local manifest and verify checksums;
5. render emulator-specific configuration into a session workspace;
6. start the emulator under supervision.

M0.3 implements document validation, registry resolution, experience defaults,
capability requirements, and assessment policy; hardware resolution remains
declarative. The conceptual dependency is
`family -> profile -> emulator adapter -> session`. Emulator adapters will own
translation from the generic profile contract into Amiberry, Hatari, VICE,
Atari800, Fuse, or openMSX configuration; generic code will not manipulate
emulator flags. A new family can exist in the catalog before its adapter is
implemented.

Emulator metadata has explicit `unresolved`, `candidate`, and `qualified`
states. Existing named emulators are candidates, not qualifications. A
qualified entry must carry evidence for emulator version, supported hardware,
architecture, DietPi version, graphics backend, and result. No M0.3 entry is
qualified. Candidate research should use authoritative upstream evidence and
consider Linux/ARM64 support, maintenance, accuracy, keyboard-computer fit,
fullscreen and CLI behavior, persistence, audio/input, licensing, and
reproducible installation. MAME is not selected merely for broad platform
coverage.

Capability requirements and runtime assessment policy are defined in
[`docs/EXPERIENCE.md`](EXPERIENCE.md). Required capabilities are correctness
prerequisites; recommended capabilities affect advice only. Assessment status
is independent of emulator qualification, and performance alone can never make
a profile blocked.

## Expected boot and session flow

After host initialization, a future dedicated graphical session will start a
small appliance manager. Its conceptual top-level menu is:

```text
RETRO DAILY DRIVER

Classic Computers
Amiga
Atari ST / TT / Falcon
Commodore
Atari 8-bit
ZX Spectrum
MSX
BBC
Apple II
Acorn Archimedes

Modern Retro
Commander X16
MEGA65
Agon
Neo6502
Foenix F256
Colour Maximite 2
X65

More...
Administration
```

The manager will derive this menu from the family registry and profile
classification/order and eligibility, not literal F1-F10 bindings. It will
validate configuration and
assets, present eligible profiles, launch exactly one fullscreen emulator,
collect logs, and return to the selector on a clean exit or crash. A session
supervisor will enforce process ownership and recovery. Linux administration
remains available on a separate console or explicitly enabled administrative
path.

No launcher, graphical session, supervisor, or emulator is implemented in M0.3.

## Keyboard-computer hardware contract

Official appliance qualification initially targets only Raspberry Pi 400,
Raspberry Pi 500, and Raspberry Pi 500+. Their integrated keyboard form factor
is intentional: it supports the illusion that the physical appliance is the
selected computer. The architecture remains portable, but generic Raspberry Pi
boards are not official M0.3 targets. Peripherals are treated as computer
interfaces rather than desktop conveniences: keyboard, mouse, joystick/gamepad,
USB import, networking, serial interfaces, audio, and sensible GPIO
experimentation are future adapter concerns. M0.3 does not forward GPIO or
complex peripherals.

## Security assumptions

The appliance is a single-user physical device, but user-provided media is
untrusted input. Emulator processes must remain unprivileged; configuration is
root-owned; state is not world-readable or writable; asset acquisition never
implicitly grants execution or distribution rights. Network services, sudo
policy, removable-media mounting, sandboxing, and update trust are deferred and
must be explicitly designed before exposure. Provisioning is unattended-capable
but does not embed credentials or secrets in this repository.
