from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from retro_config import (  # noqa: E402
    ConfigError,
    assessment_can_start,
    discover_and_validate,
    load_family_registry,
    resolve_canonical_profiles,
    resolve_experience,
    resolve_hardware,
    validate_runtime_assessment,
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
        profile_ids = {item["profile"]["id"] for item in self.profiles}
        self.assertTrue({"amiga-a1200", "atari-ste", "commodore-c64", "atari8-800xl", "spectrum-128k", "msx-msx2"}.issubset(profile_ids))
        self.assertTrue({"bbc-master", "apple2-iie", "archimedes-a3000", "x16-default", "mega65-default", "agon-light2", "neo6502-default", "foenix-f256", "cmm2-default", "x65-default"}.issubset(profile_ids))

    def test_all_first_class_families_have_canonical_profiles(self) -> None:
        self.assertEqual(len(self.registry["families"]), 16)
        self.assertEqual(
            {item["classification"] for item in self.registry["families"]},
            {"classic", "modern_retro"},
        )
        canonical = resolve_canonical_profiles(self.registry, self.profiles)
        self.assertEqual(set(canonical), {item["id"] for item in self.registry["families"]})

    def test_core_config_contains_no_family_id_allowlist(self) -> None:
        source = (ROOT / "scripts" / "retro_config.py").read_text(encoding="utf-8")
        for family in self.registry["families"]:
            self.assertNotIn(f'"{family["id"]}"', source)
        self.assertNotIn("Raspberry Pi 400", source)

    def test_experience_defaults_describe_a_microcomputer(self) -> None:
        defaults = self.registry["experience_defaults"]
        self.assertEqual(defaults["type"], "microcomputer")
        self.assertEqual(defaults["boot_target"], "native_environment")
        self.assertTrue(defaults["persistent_state"])
        self.assertFalse(defaults["game_frontend"])
        family = next(item for item in self.registry["families"] if item["id"] == "x16")
        profile = next(item for item in self.profiles if item["profile"]["id"] == "x16-default")
        self.assertEqual(resolve_experience(self.registry, family, profile), defaults)

    def test_authenticity_is_the_default_and_enhanced_is_an_override(self) -> None:
        self.assertEqual(self.registry["experience_defaults"]["fidelity"], "authentic")
        family = next(item for item in self.registry["families"] if item["id"] == "amiga")
        profile = next(item for item in self.profiles if item["profile"]["id"] == "amiga-a1200")
        profile["experience"] = {"fidelity": "enhanced"}
        self.assertEqual(resolve_experience(self.registry, family, profile)["fidelity"], "enhanced")

    def test_required_and_recommended_capabilities_are_distinct(self) -> None:
        x16 = next(item for item in self.profiles if item["profile"]["id"] == "x16-default")
        self.assertEqual(x16["capabilities"]["required"], ["aarch64"])
        self.assertEqual(x16["capabilities"]["recommended"], ["high_performance_emulation"])
        self.assertNotIn("high_performance_emulation", x16["capabilities"]["required"])

    def test_unknown_profile_capability_fails_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copy_root = Path(directory) / "repo"
            shutil.copytree(ROOT, copy_root)
            profile_path = copy_root / "profiles" / "x16" / "x16-default.yml"
            content = profile_path.read_text(encoding="utf-8").replace("[aarch64]", "[not-a-capability]")
            profile_path.write_text(content, encoding="utf-8")
            with self.assertRaisesRegex(ConfigError, "unknown profile capabilities"):
                discover_and_validate(copy_root)

    def test_runtime_assessment_policy_preserves_user_agency(self) -> None:
        self.assertTrue(assessment_can_start({"status": "qualified", "override_allowed": False}))
        self.assertTrue(assessment_can_start({"status": "unqualified", "override_allowed": False}))
        not_recommended = {"status": "not_recommended", "override_allowed": True, "reasons": ["performance_below_target"]}
        self.assertFalse(assessment_can_start(not_recommended))
        self.assertTrue(assessment_can_start(not_recommended, acknowledged=True))
        self.assertFalse(assessment_can_start({"status": "incompatible", "override_allowed": False}))
        self.assertFalse(assessment_can_start({"status": "blocked", "override_allowed": False}))

    def test_performance_alone_cannot_be_blocked(self) -> None:
        with self.assertRaisesRegex(ConfigError, "performance alone cannot produce blocked"):
            validate_runtime_assessment({"status": "blocked", "override_allowed": False, "reasons": ["performance_below_target"]})

    def test_invalid_assessment_status_fails(self) -> None:
        with self.assertRaisesRegex(ConfigError, "invalid status"):
            validate_runtime_assessment({"status": "maybe", "override_allowed": False})

    def test_emulator_qualification_states_are_explicit(self) -> None:
        states = {item["emulator"]["qualification"] for item in self.registry["families"]}
        self.assertIn("candidate", states)
        self.assertIn("unresolved", states)
        self.assertNotIn("qualified", states)

    def test_spectrum_next_is_a_noncanonical_spectrum_profile(self) -> None:
        spectrum_profiles = [item for item in self.profiles if item["profile"]["family"] == "spectrum"]
        self.assertEqual({item["profile"]["id"] for item in spectrum_profiles}, {"spectrum-128k", "spectrum-next"})
        next_profile = next(item for item in spectrum_profiles if item["profile"]["id"] == "spectrum-next")
        self.assertEqual(next_profile["profile"]["classification"], "modern_retro")

    def test_new_family_can_be_added_without_python_changes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copy_root = Path(directory) / "repo"
            shutil.copytree(ROOT, copy_root)
            registry_path = copy_root / "families" / "registry.yml"
            registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
            registry["families"].append({
                "id": "test-family",
                "name": "Test Family",
                "classification": "classic",
                "canonical_profile": "test-machine",
                "emulator": {"id": "test-emulator", "qualification": "candidate"},
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

    def test_duplicate_menu_order_fails_validation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copy_root = Path(directory) / "repo"
            shutil.copytree(ROOT, copy_root)
            registry_path = copy_root / "families" / "registry.yml"
            registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
            registry["families"][1]["menu_order"] = registry["families"][0]["menu_order"]
            registry_path.write_text(yaml.safe_dump(registry, sort_keys=False), encoding="utf-8")
            with self.assertRaisesRegex(ConfigError, "duplicate menu_order"):
                discover_and_validate(copy_root)

    def test_unknown_classification_fails_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copy_root = Path(directory) / "repo"
            shutil.copytree(ROOT, copy_root)
            registry_path = copy_root / "families" / "registry.yml"
            registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
            registry["families"][0]["classification"] = "console"
            registry_path.write_text(yaml.safe_dump(registry, sort_keys=False), encoding="utf-8")
            with self.assertRaisesRegex(ConfigError, "invalid classification"):
                discover_and_validate(copy_root)

    def test_qualified_emulator_requires_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copy_root = Path(directory) / "repo"
            shutil.copytree(ROOT, copy_root)
            registry_path = copy_root / "families" / "registry.yml"
            registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
            registry["families"][0]["emulator"]["qualification"] = "qualified"
            registry_path.write_text(yaml.safe_dump(registry, sort_keys=False), encoding="utf-8")
            with self.assertRaisesRegex(ConfigError, "requires evidence"):
                discover_and_validate(copy_root)

    def test_canonical_profile_mismatch_fails_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copy_root = Path(directory) / "repo"
            shutil.copytree(ROOT, copy_root)
            registry_path = copy_root / "families" / "registry.yml"
            registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
            registry["families"][0]["canonical_profile"] = "atari-ste"
            registry_path.write_text(yaml.safe_dump(registry, sort_keys=False), encoding="utf-8")
            with self.assertRaisesRegex(ConfigError, "belongs to another family"):
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

    def test_retro_doctor_lists_registry_families_without_emulator_checks(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "retro-doctor"), "--repo-root", str(ROOT), "--runtime-root", str(ROOT / "missing-runtime")],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotIn("Traceback", result.stdout + result.stderr)
        self.assertIn("Commander X16", result.stdout)
        self.assertIn("BBC Micro / Master", result.stdout)
        self.assertIn("Emulator checks are intentionally deferred", result.stdout)


if __name__ == "__main__":
    unittest.main()
