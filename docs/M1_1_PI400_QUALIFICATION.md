# M1.1 — Raspberry Pi 400 host baseline

M1.1 makes the Raspberry Pi 400 the first physical Daily Retro Driver reference
host. It does not qualify an emulator and it does not install a launcher.

## Status

Repository implementation: **IMPLEMENTED**.

Physical Raspberry Pi 400 qualification: **NOT PERFORMED**.

The milestone is not complete until evidence from a real Pi 400 has been
captured and reviewed.

## Canonical DRD identity

Qualification must use the renamed Daily Retro Driver identity:

- product: `Daily Retro Driver` (`DRD`)
- repository: `Ploos-AS/DailyRetroDriver`
- runtime root: `/srv/daily-retro-driver`
- configuration root: `/etc/daily-retro-driver`
- service account/group: `drd:drd`
- administration group: `drd-admin`
- doctor command: `scripts/drd-doctor`
- qualification command: `scripts/drd-qualify-host`

Evidence produced under the former `RetroDailyDriver` / `retro-daily-driver`
identity is not accepted as the canonical M1.1 physical qualification record.

## Target

- Raspberry Pi 400
- 64-bit ARM (`aarch64`/`arm64`)
- DietPi or a compatible Debian-family installation
- DRM/KMS graphics path
- Linux evdev input path
- ALSA-visible audio where provided by the selected display/audio path

M1.1 observes these interfaces without installing an emulator or changing the
host graphics/audio configuration.

## Qualification run

Provision the host first using the normal playbook. Run provisioning a second
time and retain the Ansible recap; M1 acceptance ultimately requires that the
second run is clean.

Then, from a checkout of this repository on the Pi 400:

```bash
make check
sudo ./scripts/drd-doctor --repo-root .
sudo python3 scripts/drd-qualify-host \
  --output /srv/daily-retro-driver/reports/m1.1-pi400.json
```

Review the JSON evidence rather than relying only on the process exit status.
The required M1.1 baseline checks are Debian/DietPi family, ARM64 architecture,
Pi 400 model identity, a DRM device and evdev input. Display connector and ALSA
observations are retained as evidence but may require interactive follow-up.

## Manual observations

Record alongside the JSON report:

1. monitor/TV model, connection and requested display mode;
2. whether the console is visually stable with no unexpected blanking or mode
   churn;
3. whether the integrated Pi 400 keyboard is usable and special keys are
   visible to Linux;
4. selected audio output and a successful audible playback test;
5. the second Ansible provisioning recap (`changed=0` is the target);
6. any warnings from `drd-doctor` or the qualification report.

Do not mark display timing, latency, audio quality, keyboard mapping, fullscreen
session behavior or any emulator as qualified from this baseline alone. Those
require later interactive M1/M3 evidence.

## Acceptance

M1.1 can be marked complete when a real Pi 400 run has:

- produced a `result: PASS` M1.1 JSON report;
- resolved the existing `raspberry-pi-400` hardware profile;
- completed `make check`;
- completed a second provisioning run without unintended changes;
- recorded the manual display/input/audio observations above;
- found no blocker that invalidates the Pi 400 as the first DRD reference host.

Until then the repository supports the qualification procedure, but the
physical target remains unqualified.
