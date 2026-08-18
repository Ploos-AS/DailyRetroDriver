# Architecture

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
├── state/{amiga,atari,commodore}/
├── media/{amiga,atari,commodore}/
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
manifest. Backups must cover all three mutable areas and their manifests.

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

An appliance profile declares its family and emulator boundary, virtual machine
parameters, display and input policy, asset references, mutable-state location,
and required/preferred hardware capabilities. Resolution will follow this order:

1. detect a host and produce its capability set;
2. load and validate a selected appliance profile;
3. reject missing `hardware_requirements.all` capabilities;
4. resolve logical assets through the local manifest and verify checksums;
5. render emulator-specific configuration into a session workspace;
6. start the emulator under supervision.

M0 implements document validation and hardware resolution only. Emulator
adapters will own translation from the generic profile contract into Amiberry,
Hatari, or VICE configuration; generic code will not manipulate emulator flags.

## Expected boot and session flow

After host initialization, a future dedicated graphical session will start a
small appliance manager. It will validate configuration and assets, present
eligible profiles, launch exactly one fullscreen emulator, collect logs, and
return to the selector on a clean exit or crash. A session supervisor will
enforce process ownership and recovery. Linux administration remains available
on a separate console or explicitly enabled administrative path.

No launcher, graphical session, supervisor, or emulator is implemented in M0.

## Security assumptions

The appliance is a single-user physical device, but user-provided media is
untrusted input. Emulator processes must remain unprivileged; configuration is
root-owned; state is not world-readable or writable; asset acquisition never
implicitly grants execution or distribution rights. Network services, sudo
policy, removable-media mounting, sandboxing, and update trust are deferred and
must be explicitly designed before exposure. Provisioning is unattended-capable
but does not embed credentials or secrets in this repository.
