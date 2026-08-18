# Roadmap

## M0 — foundation (current)

Version schemas for hardware, profiles, and asset manifests; detect supported
Raspberry Pi hardware; bootstrap DietPi/Debian with an idempotent Ansible
foundation; create the secure runtime layout; and provide local validation and
`retro-doctor`. Acceptance: all M0 documents validate, Ansible syntax passes,
the playbook is safe to run twice without unintended changes, and no emulator or
proprietary asset is required.

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

## M3 — Amiga / Amiberry

Build and pin Amiberry, render A1200 configuration, validate user-supplied
Kickstart/system assets, and isolate mutable state. Acceptance: a qualified
A1200 session starts, runs, saves state in the canonical tree, and returns to
the selector; no proprietary content ships with the project.

## M4 — Atari / Hatari

Install and pin Hatari, render the STE profile, support user TOS or an explicitly
licensed open alternative, and qualify input/display behavior. Acceptance: the
STE session meets the same start, state, logging, and recovery contract.

## M5 — Commodore / VICE

Install and pin VICE, render the C64 profile, map keyboard/joystick input, and
validate optional firmware/media. Acceptance: the C64 session meets the common
session contract and does not require unredistributable assets in source.

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
