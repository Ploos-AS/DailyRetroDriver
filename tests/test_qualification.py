from pathlib import Path
import tempfile
import unittest
from unittest import mock

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from retro_qualification import collect


class QualificationTests(unittest.TestCase):
    def test_pi400_baseline_passes_with_required_devices(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            model = root / "model"
            release = root / "os-release"
            model.write_bytes(b"Raspberry Pi 400 Rev 1.0\0")
            release.write_text('ID=dietpi\nID_LIKE="debian"\nPRETTY_NAME="DietPi"\n', encoding="utf-8")
            path_sets = iter([
                ["/dev/dri/card0", "/dev/dri/renderD128"],
                ["/sys/class/drm/card0-HDMI-A-1"],
                ["/dev/input/event0"],
                ["/dev/snd/controlC0"],
            ])
            with mock.patch("retro_qualification.matching_paths", side_effect=lambda patterns: next(path_sets)), mock.patch("retro_qualification.command_output", return_value=""):
                report = collect(model_file=model, os_release_file=release, architecture="aarch64")
        self.assertEqual(report["result"], "PASS")
        self.assertEqual(report["qualification_target"], "raspberry-pi-400")

    def test_non_pi400_without_devices_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            model = root / "model"
            release = root / "os-release"
            model.write_text("development host", encoding="utf-8")
            release.write_text('ID=ubuntu\nID_LIKE="debian"\nPRETTY_NAME="Ubuntu"\n', encoding="utf-8")
            with mock.patch("retro_qualification.matching_paths", return_value=[]), mock.patch("retro_qualification.command_output", return_value=""):
                report = collect(model_file=model, os_release_file=release, architecture="x86_64")
        self.assertEqual(report["result"], "FAIL")
        statuses = {item["id"]: item["status"] for item in report["checks"]}
        self.assertEqual(statuses["hardware.pi400"], "FAIL")
        self.assertEqual(statuses["graphics.drm"], "FAIL")
        self.assertEqual(statuses["input.evdev"], "FAIL")


if __name__ == "__main__":
    unittest.main()
