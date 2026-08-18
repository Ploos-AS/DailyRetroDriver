# Roadmap

## M0 — foundation (complete)

Version schemas for hardware, profiles, and asset manifests; detect supported
Raspberry Pi hardware; bootstrap DietPi/Debian with an idempotent Ansible
foundation; create the secure runtime layout; and provide local validation and
`retro-doctor`. Acceptance: all M0 documents validate, Ansible syntax passes,
the playbook is safe to run twice without unintended changes, and no emulator or
proprietary asset is required.

## M0.1 — multi-platform architecture expansion (current)

Generalize family discovery and validation through a declarative registry;
provide canonical profiles for Amiga, Atari 16/32-bit, Commodore 8-bit, Atari
8-bit, ZX Spectrum, and MSX; derive runtime family directories and diagnostic
output from that registry; and document experimental candidates. Acceptance:
all six families resolve canonical profiles, a temporary registry extension
works without Python changes, duplicate/unknown IDs fail cleanly, and no
emulator or firmware is installed or committed.

## M1 — reproducible host foundation

Provision pinned graphics, audio, and input dependencies; define the dedicated
local session and console/admin boundary; qualify display and controller paths
on every supported board. Acceptance: a clean DietPi image reaches a repeatable
hardware-accelerated test session with working audio and input, and a second
provisioning run is clean.

## M2 — appliance manager

Implement the fullscreen selector, profile/capability eligibility, asset
preflight, session supervision, structured logs, clean exit, and crash return.
Acceptance: sample non-emulator sessions launch fullscreen and return reliably;
failure is visible and recoverable without exposing a desktop.

## M3 — emulator integrations

Emulator integrations are deliberately split into family submilestones. Each
must provide a pinned installation, profile translation, asset preflight,
isolated mutable state, fullscreen behavior, logging, and recovery acceptance.

### M3.1 — Amiga / Amiberry

Build and pin Amiberry, render A1200 configuration, validate user-supplied
Kickstart/system assets, and isolate mutable state. Acceptance: a qualified
A1200 session starts, runs, saves state in the canonical tree, and returns to
the selector; no proprietary content ships with the project.

### M3.2 — Atari 16/32-bit / Hatari

Install and pin Hatari, render the STE profile, support user TOS or an explicitly
licensed open alternative, and qualify input/display behavior. Acceptance: the
STE session meets the same start, state, logging, and recovery contract.

### M3.3 — Commodore / VICE

Install and pin VICE, render the C64 profile, map keyboard/joystick input, and
validate optional firmware/media. Acceptance: the C64 session meets the common
session contract and does not require unredistributable assets in source.

### M3.4 — Atari 8-bit / Atari800

Render the 800XL profile and qualify firmware/input behavior across the Atari
8-bit machine variants planned below. Acceptance: a legal firmware asset can be
validated and the 800XL session meets the common session contract.

### M3.5 — ZX Spectrum / Fuse

Render the 128K profile and qualify keyboard, display, and optional machine ROM
handling. Acceptance: the 128K session meets the common session contract.

### M3.6 — MSX / openMSX

Render the generic MSX2 profile without assuming one proprietary vendor machine,
then qualify firmware and input handling. Acceptance: an eligible MSX2 session
meets the common session contract.

## Future machine targets

The registry can accept additional profiles under the existing families:

* Amiga: A500, A600, A1200, and A3000/A4000 where useful.
* Atari 16/32-bit: ST, STE, TT, and Falcon.
* Commodore: C64, C128, VIC-20, Plus/4, and PET.
* Atari 8-bit: Atari 400/800, 600XL/800XL, 65XE/130XE, and optionally 5200.
* ZX Spectrum: 48K, 128K, +2, and +3.
* MSX: MSX1, MSX2, MSX2+, and Turbo R where support and assets permit.

Potential experimental families are Commander X16 (planned `x16emu`), BBC
Micro / Master, Apple II, and Acorn Archimedes. Emulator selection for these
must consider ARM64 support, maintenance, accuracy, fullscreen suitability,
CLI/configurability, input, latency, licensing, and reproducible installation;
MAME is not selected by default merely because it supports a platform.

## M6 — resilience and qualification

Implement manifest-aware backup/restore, host and appliance qualification,
transactional updates, and rollback. Acceptance: documented loss scenarios are
restorable on supported hardware, update failure rolls back, and qualification
reports are retained.

## M7 — installation and recovery

Polish unattended installation, first-boot asset onboarding, recovery media,
operator documentation, and release artifacts. Acceptance: a user can install
from a documented DietPi baseline, recover a failed device, and reproduce a
released appliance without hidden manual steps.

Future milestones are planned and are not implemented or complete.
