# Authentic computer experience

Daily Retro Driver (DRD) prioritizes the experience of using the original or
intended computer environment over operating the Linux host or an emulator
frontend. Once a personality starts, the user should encounter its native
environment as directly as practical. The Raspberry Pi is the host; it should
disappear during normal use.

This is why the official targets remain the keyboard computers Raspberry Pi 400,
Pi 500, and Pi 500+. They are chosen for the physical keyboard-computer illusion,
not because they are generic Raspberry Pi boards. Games are applications inside
the selected computer, alongside native desktop, BASIC, monitor, shell,
programming, communications, and productivity software.

## Authenticity hierarchy

When valid implementation choices conflict, future qualification should prefer:

1. Correct machine behavior
2. Correct input behavior
3. Correct display behavior
4. Correct audio behavior
5. Persistent/native storage semantics
6. Native software workflow
7. Low host visibility
8. Convenience features
9. Maximum benchmark performance

This is guidance, not a substitute for platform-specific historical judgment.
For example, correct PAL timing can matter more than an arbitrary frame-rate
target; correct aspect ratio is preferable to silently stretching to 16:9; and
native Workbench/GEM/BASIC workflows are preferable to a host-side file browser.

## Authentic and enhanced profiles

Profiles express intent through `experience.fidelity`:

```yaml
experience:
  fidelity: authentic
```

`authentic` aims at a historically appropriate CPU class/speed, RAM, chipset
timing, display mode, floppy behavior, and boot flow. `enhanced` represents a
legitimate expanded computer: fast RAM, an accelerator, RTG, hard disk, network
adapter, or larger storage. Enhanced does not mean inauthentic; real owners
expanded these machines too. A future Amiga set might include A1200 stock,
A1200 daily-driver, and A4000/060/RTG as separate profiles.

The registry defaults to authentic and profiles may override it without forcing
identical machine constraints across families.

## Native boot and host invisibility

The intended flow is:

```text
Power on -> Daily Retro Driver selector -> selected computer -> native environment
```

Examples include Workbench or an Amiga boot disk, GEM/TOS, a C64 `READY.`
prompt, Atari BASIC, Spectrum BASIC, MSX BASIC, BBC BASIC/MOS, an Apple II boot
environment, RISC OS, X16 BASIC, MEGA65 native environment, or Agon MOS/BBC
BASIC. Exact targets remain profile-defined and are not automated in M0.3.

Normal operation must avoid Linux panels, notifications, shell windows, host
cursor behavior where inappropriate, blanking dialogs, package messages,
unexpected emulator menus, login prompts, and systemd console output. A future
session must deliberately provide return-to-selector, administration, reboot,
and power-off paths without stealing common original-machine keys.

## Display, input, and audio

Qualification must consider PAL/NTSC, machine refresh, pixel and display aspect
ratio, borders/overscan, integer scaling, optional CRT effects, fullscreen,
latency, tearing, frame pacing, and useful host display mode switching. Stretching
to a modern widescreen is never the silent authenticity default.

Keyboard qualification includes physical and symbolic mapping, special keys,
function keys, modifiers, dead keys, international layouts, joystick mapping,
mouse capture/release, and original button conventions. Emulator controls must
not steal keys used by native software; administrative escape is deliberate and
documented.

Audio qualification includes sample-rate behavior, latency, stable playback,
chipset-specific sound, historically relevant stereo separation, and avoiding
host notifications or mixer artifacts.

## Storage and communications

Persistent state is part of the computer identity. Future adapters should model
floppy, hard disk, cartridge, tape, SD card, filesystem, native partition, or
virtual block-device workflows as the target machine expects. A C64 disk image
should behave like a disk, an Amiga hard disk should persist as Amiga storage,
and X16/MEGA65 storage should resemble their expected workflows. Host import and
export belong in administration and must not replace the machine filesystem.

Where historically plausible and technically supported, future profiles may
expose serial, modem emulation, telnet, Ethernet, TCP/IP stacks, BBS clients,
terminal software, file transfer, and network-mounted or emulated adapters.
Networking is optional by family and profile.

## Capability and assessment policy

These are separate concepts:

```text
Host hardware + emulator qualification + profile requirements/preferences
    = runtime assessment
```

Profiles use `capabilities.required` for correctness prerequisites and
`capabilities.recommended` for performance or experience improvements. A
recommended capability is never treated as required. Existing
`hardware_requirements.all` remains supported for compatibility.

Dynamic assessment statuses are:

| Status | Meaning | Normal start policy |
| --- | --- | --- |
| `qualified` | Tested against the target experience on this host class | Start |
| `unqualified` | Not tested sufficiently; not known broken | Start |
| `not_recommended` | Expected degraded experience, such as latency or frame pacing | Start with acknowledgement |
| `incompatible` | Known technical incompatibility | Do not start normally |
| `blocked` | Concrete missing prerequisite, such as firmware, storage, or binary | Do not start |

Performance alone must never produce `blocked`. `not_recommended` must never
mean forbidden: the future UI must offer **Start anyway** with an acknowledgement.
Reason codes are structured (`performance_below_target`,
`emulator_unqualified`, `required_asset_missing`,
`unsupported_host_architecture`, `graphics_backend_missing`,
`storage_unavailable`, and `configuration_invalid`). M0.3 validates the policy
and start semantics but does not implement a runtime evaluator or benchmark.

Emulator qualification is independent from profile/host assessment. One emulator
may be a candidate or qualified in general while an A4000/060/RTG profile is
`not_recommended` on a Pi 400 and later `qualified` on a Pi 500. No M0.3 result
claims measured hardware performance or emulator qualification.
