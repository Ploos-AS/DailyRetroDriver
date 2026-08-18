from pathlib import Path
import shutil
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from retro_config import (  # noqa: E402
    ConfigError,
    discover_and_validate,
    load_family_registry,
    resolve_canonical_profiles,
    resolve_hardware,
)


class ConfigurationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.hardware, cls.profiles = discover_and_validate(ROOT)
        cls.registry = load_family_registry(ROOT)

    def test_expected_hardware_profiles_exist(self) -> None:
        self.assertEqual(
            {item["hardware"]["id"] for item in self.hardware},
            {"raspberry-pi-400", "raspberry-pi-500", "raspberry-pi-500-plus"},
        )

    def test_expected_appliance_profiles_exist(self) -> None:
        self.assertEqual(
            {item["profile"]["id"] for item in self.profiles},
            {"amiga-a1200", "atari-ste", "commodore-c64", "atari8-800xl", "spectrum-128k", "msx-msx2"},
        )

    def test_all_first_class_families_have_canonical_profiles(self) -> None:
        self.assertEqual(
            {item["id"] for item in self.registry["families"]},
            {"amiga", "atari", "commodore", "atari8", "spectrum", "msx"},
        )
        canonical = resolve_canonical_profiles(self.registry, self.profiles)
        self.assertEqual(set(canonical), {item["id"] for item in self.registry["families"]})

    def test_new_family_can_be_added_without_python_changes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copy_root = Path(directory) / "repo"
            shutil.copytree(ROOT, copy_root)
            registry_path = copy_root / "families" / "registry.yml"
            registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
            registry["families"].append({
                "id": "test-family",
                "name": "Test Family",
                "canonical_profile": "test-machine",
                "planned_emulator": "test-emulator",
                "menu_order": 999,
                "status": "experimental",
            })
            registry_path.write_text(yaml.safe_dump(registry, sort_keys=False), encoding="utf-8")
            (copy_root / "profiles" / "test-family").mkdir()
            (copy_root / "profiles" / "test-family" / "test-machine.yml").write_text(
                """---\nschema_version: 1\nprofile:\n  id: test-machine\n  family: test-family\n  title: Test Machine\n  emulator: test-emulator\n  maturity: experimental\nmachine:\n  model: test\ndisplay:\n  fullscreen: true\ninput:\n  keyboard: host\nassets: []\nstate:\n  directory: state/test-family/test-machine\n  mutable: []\nhardware_requirements:\n  all: []\n  preferred: []\n""",
                encoding="utf-8",
            )
            _, profiles = discover_and_validate(copy_root)
            self.assertIn("test-machine", {item["profile"]["id"] for item in profiles})

    def test_unknown_family_reference_fails_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copy_root = Path(directory) / "repo"
            shutil.copytree(ROOT, copy_root)
            profile_path = copy_root / "profiles" / "msx" / "msx-msx2.yml"
            content = profile_path.read_text(encoding="utf-8").replace("family: msx", "family: unknown")
            profile_path.write_text(content, encoding="utf-8")
            with self.assertRaisesRegex(ConfigError, "unknown appliance family"):
                discover_and_validate(copy_root)

    def test_duplicate_family_ids_fail_validation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copy_root = Path(directory) / "repo"
            shutil.copytree(ROOT, copy_root)
            registry_path = copy_root / "families" / "registry.yml"
            registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
            registry["families"].append(dict(registry["families"][0]))
            registry_path.write_text(yaml.safe_dump(registry, sort_keys=False), encoding="utf-8")
            with self.assertRaisesRegex(ConfigError, "duplicate family ID"):
                discover_and_validate(copy_root)

    def test_duplicate_profile_ids_fail_validation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copy_root = Path(directory) / "repo"
            shutil.copytree(ROOT, copy_root)
            duplicate = copy_root / "profiles" / "msx" / "duplicate.yml"
            original = (copy_root / "profiles" / "msx" / "msx-msx2.yml").read_text(encoding="utf-8")
            duplicate.write_text(original, encoding="utf-8")
            with self.assertRaisesRegex(ConfigError, "duplicate profile IDs"):
                discover_and_validate(copy_root)

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
