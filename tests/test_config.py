from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from retro_config import discover_and_validate, resolve_hardware  # noqa: E402


class ConfigurationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.hardware, cls.profiles = discover_and_validate(ROOT)

    def test_expected_hardware_profiles_exist(self) -> None:
        self.assertEqual(
            {item["hardware"]["id"] for item in self.hardware},
            {"raspberry-pi-400", "raspberry-pi-500", "raspberry-pi-500-plus"},
        )

    def test_expected_appliance_profiles_exist(self) -> None:
        self.assertEqual(
            {item["profile"]["id"] for item in self.profiles},
            {"amiga-a1200", "atari-ste", "commodore-c64"},
        )

    def test_more_specific_pi_500_plus_alias_wins(self) -> None:
        result = resolve_hardware("Raspberry Pi 500 Plus Rev 1.0", self.hardware)
        self.assertIsNotNone(result)
        self.assertEqual(result["hardware"]["id"], "raspberry-pi-500-plus")

    def test_profiles_keep_state_within_family(self) -> None:
        for item in self.profiles:
            family = item["profile"]["family"]
            self.assertTrue(item["state"]["directory"].startswith(f"state/{family}/"))


if __name__ == "__main__":
    unittest.main()
