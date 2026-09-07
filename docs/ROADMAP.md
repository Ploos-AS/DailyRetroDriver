# Roadmap

## M0 — foundation (complete)

Version schemas for hardware, profiles, and asset manifests; supported
Raspberry Pi hardware detection; DietPi/Debian bootstrap; secure runtime
layout; and local validation/doctor tooling. Acceptance: documents validate,
Ansible syntax passes, and no emulator or proprietary asset is required.

## M0.1 — generic multi-platform architecture (complete)

Declarative family registry, six initial classic families, generic discovery,
canonical profiles, derived runtime directories, and extension tests.

## M0.2 — modern-retro and microcomputer experience architecture (complete)

Formalize the computer-not-console experience contract, persistent personality
state, peripheral philosophy, classic/modern-retro classification, emulator
qualification states, and registry-driven catalog. Add canonical profiles for
BBC, Apple II, Archimedes, Commander X16, MEGA65, Agon, Neo6502, Foenix F256,
Colour Maximite 2, X65, plus Spectrum Next under Spectrum. Acceptance: all
registry families resolve canonical profiles; unresolved/candidate states are
validated without implying qualification; doctor output is registry-driven; and
no emulator, ROM, launcher, or frontend is installed.

## M0.3 — authentic experience and capability policy (complete)

Make authenticity-first behavior, native environment boot targets, host
invisibility, display/input/audio/storage/communications requirements,
authentic-versus-enhanced fidelity, capability recommendations, runtime
assessment statuses, and user override semantics explicit. Acceptance: required
and recommended capabilities validate separately; `not_recommended` remains
startable with acknowledgement; performance cannot create `blocked`; emulator
qualification remains distinct from host/profile assessment; and no benchmark,
emulator, launcher, or frontend is implemented.

## M1 — reproducible host foundation

Provision pinned graphics, audio, and input dependencies; define the dedicated
local session and console/admin boundary; and qualify display/controller paths on
Pi 400, Pi 500, and Pi 500+. A second provisioning run must be clean.

### M1.1 — Raspberry Pi 400 host baseline (implementation complete; physical qualification pending)

Make Pi 400 the first physical reference host. Provide a non-destructive,
machine-readable qualification harness for DietPi/Debian identity, ARM64,
hardware identity, DRM/KMS visibility, evdev input, ALSA evidence, and session
prerequisites. Acceptance requires a real Pi 400 evidence run, `make check`, a
clean second provisioning run, and recorded display/input/audio observations.
No emulator is qualified by M1.1.

### M1.2 — reproducible graphics/audio/input dependencies

Pin and provision the host packages and configuration selected from M1.1
evidence, preserving the console/admin boundary and avoiding a general-purpose
desktop environment.

### M1.3 — dedicated local appliance session

Establish and qualify the local graphical session boundary needed by M2, with
host UI hidden during appliance use and an explicit administration/recovery
path.

### M1.4 — Pi 500 / Pi 500+ host qualification

Repeat the host qualification contract on the remaining official keyboard
computer targets without weakening Pi 400 support.

## M2 — appliance/session manager

Implement the registry-driven fullscreen personality selector, profile/capability
eligibility, asset preflight, session supervision, structured logs, clean exit,
and crash return. It must present computer personalities, not a game carousel.

## M3 — classic computer integrations

Each submilestone requires pinned installation, profile translation, asset
preflight, isolated mutable state, fullscreen behavior, logging, and recovery.

### M3.1 — Amiga / Amiberry

### M3.2 — Atari 16/32-bit / Hatari

### M3.3 — Commodore / VICE

### M3.4 — Atari 8-bit / Atari800

### M3.5 — ZX Spectrum / Fuse

### M3.6 — MSX / openMSX

### M3.7 — BBC Micro / Master

Evaluate a suitable emulator only after authoritative Linux/ARM64 and
appliance-suitability research; support Model B and Master profiles.

### M3.8 — Apple II

Evaluate a suitable emulator with persistent disk workflows and Apple IIe
profile support.

### M3.9 — Acorn Archimedes

Evaluate a suitable emulator and RISC OS configuration for the A3000 profile.

## M4 — modern-retro integrations

### M4.1 — Commander X16

High-priority evaluation and integration of the X16 computer personality using
the `x16emu` candidate.

### M4.2 — MEGA65

Evaluate Xemu and persistent MEGA65 computer workflows.

### M4.3 — Agon

Select an emulator only after authoritative project evidence.

### M4.4 — Neo6502

Select an emulator only after ARM64 Linux evidence exists.

### M4.5 — Foenix F256

Evaluate a reproducible ARM64-capable emulator and F256 profile.

### M4.6 — Spectrum Next

Integrate Spectrum Next as a profile under the existing Spectrum family.

### M4.7 — Colour Maximite 2

Evaluate a suitable emulator and persistent BASIC/development workflow.

### M4.8 — X65

Evaluate the less mature X65 ecosystem without inventing emulator qualification.

## M5 — persistence and peripheral integration

Implement persistent computer disks/media, optional snapshots, keyboard/mouse/
joystick policies, USB import, networking, serial, audio, and carefully scoped
peripheral/GPIO experimentation.

## M6 — resilience, qualification, and updates

Implement manifest-aware backup/restore, host and appliance qualification,
transactional updates, and rollback. Qualification records must include
emulator version, hardware, architecture, DietPi version, graphics backend, and
result.

## M7 — installation and recovery

Polish unattended installation, first-boot asset onboarding, recovery media,
operator documentation, and release artifacts. Future milestones are planned
and are not implemented or complete.

## Future machine targets

Expected later profiles include Amiga A500/A600/A3000/A4000; Atari ST/STE/TT/
Falcon; Commodore C128/VIC-20/Plus/4/PET; Atari 8-bit 400/800, 600XL/800XL,
65XE/130XE and optional 5200; Spectrum 48K/+2/+3; and MSX1/MSX2+/Turbo R.

Emulator selection must consider Linux/ARM64 support, maintenance, accuracy,
keyboard-computer suitability, fullscreen/CLI behavior, persistence, audio,
input, licensing, and reproducible installation. MAME is not selected merely
because it supports a platform.
