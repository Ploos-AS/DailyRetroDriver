#!/usr/bin/env python3
"""Host qualification evidence collection for Daily Retro Driver M1.1.

The collector is deliberately non-destructive. It observes host state only and
returns structured evidence that can be archived with a physical qualification
run.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import glob
import json
import platform
import subprocess
from typing import Iterable


@dataclass(frozen=True)
class Check:
    id: str
    status: str
    detail: str


def read_text(path: Path) -> str:
    try:
        return path.read_bytes().rstrip(b"\0").decode("utf-8", errors="replace").strip()
    except OSError:
        return ""


def parse_os_release(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in read_text(path).splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            values[key] = value.strip().strip('"')
    return values


def matching_paths(patterns: Iterable[str]) -> list[str]:
    found: set[str] = set()
    for pattern in patterns:
        found.update(glob.glob(pattern))
    return sorted(found)


def command_output(argv: list[str]) -> str:
    try:
        completed = subprocess.run(
            argv,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return completed.stdout.strip()


def collect(*, model_file: Path = Path("/proc/device-tree/model"), os_release_file: Path = Path("/etc/os-release"), architecture: str | None = None) -> dict[str, object]:
    model = read_text(model_file)
    release = parse_os_release(os_release_file)
    arch = (architecture or platform.machine()).lower()
    os_family = {release.get("ID", ""), *release.get("ID_LIKE", "").split()}

    drm_nodes = matching_paths(("/dev/dri/card*", "/dev/dri/renderD*"))
    drm_connectors = matching_paths(("/sys/class/drm/card*-HDMI-*", "/sys/class/drm/card*-DP-*"))
    input_nodes = matching_paths(("/dev/input/event*",))
    audio_nodes = matching_paths(("/dev/snd/controlC*", "/dev/snd/pcm*"))

    checks = [
        Check("os.debian_family", "PASS" if os_family & {"debian", "dietpi"} else "FAIL", release.get("PRETTY_NAME", "unknown")),
        Check("arch.arm64", "PASS" if arch in {"aarch64", "arm64"} else "FAIL", arch or "unknown"),
        Check("hardware.pi400", "PASS" if "Raspberry Pi 400" in model else "FAIL", model or "model unavailable"),
        Check("graphics.drm", "PASS" if drm_nodes else "FAIL", ", ".join(drm_nodes) or "no DRM device nodes"),
        Check("graphics.connector", "PASS" if drm_connectors else "WARN", ", ".join(drm_connectors) or "no display connector observed"),
        Check("input.evdev", "PASS" if input_nodes else "FAIL", f"{len(input_nodes)} event node(s)"),
        Check("audio.alsa", "PASS" if audio_nodes else "WARN", f"{len(audio_nodes)} ALSA node(s)"),
    ]

    required_ids = {"os.debian_family", "arch.arm64", "hardware.pi400", "graphics.drm", "input.evdev"}
    qualified = all(check.status == "PASS" for check in checks if check.id in required_ids)

    return {
        "schema_version": 1,
        "milestone": "M1.1",
        "project": "Daily Retro Driver",
        "qualification_target": "raspberry-pi-400",
        "result": "PASS" if qualified else "FAIL",
        "host": {
            "model": model or "unknown",
            "architecture": arch,
            "kernel": platform.release(),
            "os": release.get("PRETTY_NAME", "unknown"),
            "dietpi_version": read_text(Path("/boot/dietpi/.version")) or "not-detected",
        },
        "graphics": {
            "drm_nodes": drm_nodes,
            "connectors": drm_connectors,
            "modetest_summary": command_output(["modetest", "-c"]),
        },
        "input": {"event_nodes": input_nodes},
        "audio": {
            "device_nodes": audio_nodes,
            "aplay_cards": command_output(["aplay", "-l"]),
        },
        "session": {
            "logind": command_output(["loginctl", "show-seat", "seat0", "-p", "CanGraphical"]),
        },
        "checks": [asdict(check) for check in checks],
        "notes": [
            "Evidence collection is non-destructive.",
            "A PASS is host-baseline evidence only; emulator qualification remains deferred to M3.x.",
            "Display timing, latency, audio playback quality and key mapping require later interactive qualification.",
        ],
    }


def dumps(report: dict[str, object]) -> str:
    return json.dumps(report, indent=2, sort_keys=True) + "\n"
