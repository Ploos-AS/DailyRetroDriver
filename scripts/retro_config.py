"""Configuration loading and validation shared by M0 tools."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

SOURCE_CLASSES = {"user_supplied", "freeware", "open_source", "redistributable"}
CAPABILITIES = {"high_performance_emulation", "nvme", "usb3_storage"}
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class ConfigError(ValueError):
    """A configuration file violates an M0 contract."""


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ConfigError(f"{path}: cannot read YAML: {exc}") from exc
    if not isinstance(value, dict):
        raise ConfigError(f"{path}: document root must be a mapping")
    if value.get("schema_version") != 1:
        raise ConfigError(f"{path}: schema_version must be 1")
    return value


def _require_id(value: Any, location: str) -> None:
    if not isinstance(value, str) or not ID_PATTERN.fullmatch(value):
        raise ConfigError(f"{location}: expected a lowercase kebab-case ID")


def validate_hardware(path: Path) -> dict[str, Any]:
    data = load_yaml(path)
    hardware = data.get("hardware")
    capabilities = data.get("capabilities")
    if not isinstance(hardware, dict) or not isinstance(capabilities, dict):
        raise ConfigError(f"{path}: hardware and capabilities must be mappings")
    _require_id(hardware.get("id"), f"{path}: hardware.id")
    if hardware["id"] != path.stem:
        raise ConfigError(f"{path}: hardware.id must match filename")
    for key in CAPABILITIES:
        if not isinstance(capabilities.get(key), bool):
            raise ConfigError(f"{path}: capabilities.{key} must be boolean")
    matches = hardware.get("model_match", {}).get("contains", [])
    if not isinstance(matches, list) or not matches or not all(isinstance(x, str) for x in matches):
        raise ConfigError(f"{path}: hardware.model_match.contains must contain strings")
    return data


def validate_registry(path: Path) -> dict[str, Any]:
    data = load_yaml(path)
    families = data.get("families")
    if not isinstance(families, list) or not families:
        raise ConfigError(f"{path}: families must be a non-empty list")
    seen: set[str] = set()
    menu_orders: set[int] = set()
    for family in families:
        if not isinstance(family, dict):
            raise ConfigError(f"{path}: each family must be a mapping")
        family_id = family.get("id")
        _require_id(family_id, f"{path}: family.id")
        if family_id in seen:
            raise ConfigError(f"{path}: duplicate family ID {family_id}")
        seen.add(family_id)
        for key in ("name", "canonical_profile", "planned_emulator"):
            if not isinstance(family.get(key), str) or not family[key]:
                raise ConfigError(f"{path}: family {family_id} requires {key}")
        if not isinstance(family.get("menu_order"), int) or family["menu_order"] < 0:
            raise ConfigError(f"{path}: family {family_id} has invalid menu_order")
        if family["menu_order"] in menu_orders:
            raise ConfigError(f"{path}: duplicate menu_order {family['menu_order']}")
        menu_orders.add(family["menu_order"])
        if family.get("status") not in {"enabled", "experimental", "disabled"}:
            raise ConfigError(f"{path}: family {family_id} has invalid status")
    return data


def load_family_registry(root: Path) -> dict[str, Any]:
    """Load the declarative family registry for consumers such as the launcher."""
    return validate_registry(root / "families" / "registry.yml")


def validate_profile(path: Path, family_ids: set[str] | None = None) -> dict[str, Any]:
    data = load_yaml(path)
    profile = data.get("profile")
    if not isinstance(profile, dict):
        raise ConfigError(f"{path}: profile must be a mapping")
    profile_id = profile.get("id")
    _require_id(profile_id, f"{path}: profile.id")
    if family_ids is not None and profile.get("family") not in family_ids:
        raise ConfigError(f"{path}: unknown appliance family")
    if path.parent.name != profile["family"]:
        raise ConfigError(f"{path}: profile directory must match family")
    for key in ("machine", "display", "input", "state", "hardware_requirements"):
        if not isinstance(data.get(key), dict):
            raise ConfigError(f"{path}: {key} must be a mapping")
    if data["display"].get("fullscreen") is not True:
        raise ConfigError(f"{path}: M0 example profiles must default to fullscreen")
    state_dir = data["state"].get("directory", "")
    expected_prefix = f"state/{profile['family']}/"
    if not isinstance(state_dir, str) or not state_dir.startswith(expected_prefix):
        raise ConfigError(f"{path}: mutable state must be below {expected_prefix}")
    for asset in data.get("assets", []):
        if not isinstance(asset, dict) or asset.get("source") not in SOURCE_CLASSES:
            raise ConfigError(f"{path}: profile asset has invalid source classification")
    required = data["hardware_requirements"].get("all", [])
    if not isinstance(required, list) or not set(required).issubset(CAPABILITIES):
        raise ConfigError(f"{path}: unknown required hardware capability")
    return data


def validate_manifest(path: Path, profile_ids: set[str]) -> dict[str, Any]:
    data = load_yaml(path)
    assets = data.get("assets")
    if not isinstance(assets, list):
        raise ConfigError(f"{path}: assets must be a list")
    seen: set[str] = set()
    for asset in assets:
        if not isinstance(asset, dict):
            raise ConfigError(f"{path}: each asset must be a mapping")
        asset_id = asset.get("id")
        _require_id(asset_id, f"{path}: asset.id")
        if asset_id in seen:
            raise ConfigError(f"{path}: duplicate asset ID {asset_id}")
        seen.add(asset_id)
        digest = asset.get("sha256")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ConfigError(f"{path}: {asset_id} has invalid SHA-256")
        source = asset.get("source", {})
        if source.get("classification") not in SOURCE_CLASSES:
            raise ConfigError(f"{path}: {asset_id} has invalid source classification")
        if asset.get("requirement") not in {"required", "optional"}:
            raise ConfigError(f"{path}: {asset_id} has invalid requirement")
        unknown = set(asset.get("profiles", [])) - profile_ids
        if unknown:
            raise ConfigError(f"{path}: {asset_id} references unknown profiles: {sorted(unknown)}")
    return data


def discover_and_validate(root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    registry = load_family_registry(root)
    families = registry["families"]
    family_ids = {item["id"] for item in families}
    hardware = [validate_hardware(path) for path in sorted((root / "hardware").glob("*.yml"))]
    profiles = [validate_profile(path, family_ids) for path in sorted((root / "profiles").glob("*/*.yml"))]
    if not hardware or not profiles:
        raise ConfigError("configuration requires hardware and appliance profiles")
    profile_ids = {item["profile"]["id"] for item in profiles}
    if len(profile_ids) != len(profiles):
        raise ConfigError("configuration contains duplicate profile IDs")
    for family in families:
        if family["canonical_profile"] not in profile_ids:
            raise ConfigError(f"family {family['id']} references unknown canonical profile {family['canonical_profile']}")
        canonical = next(item for item in profiles if item["profile"]["id"] == family["canonical_profile"])
        if canonical["profile"]["family"] != family["id"]:
            raise ConfigError(f"family {family['id']} canonical profile belongs to another family")
        if canonical["profile"].get("emulator") != family["planned_emulator"]:
            raise ConfigError(f"family {family['id']} planned emulator disagrees with canonical profile")
    validate_manifest(root / "assets" / "manifest.example.yml", profile_ids)
    return hardware, profiles


def resolve_hardware(model: str, hardware: list[dict[str, Any]]) -> dict[str, Any] | None:
    matches = [item for item in hardware if any(token in model for token in item["hardware"]["model_match"]["contains"])]
    if len(matches) > 1:
        matches.sort(key=lambda item: max(map(len, item["hardware"]["model_match"]["contains"])), reverse=True)
    return matches[0] if matches else None


def resolve_canonical_profiles(registry: dict[str, Any], profiles: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Return canonical profiles keyed by family ID, without family allow-lists."""
    by_id = {item["profile"]["id"]: item for item in profiles}
    return {
        family["id"]: by_id[family["canonical_profile"]]
        for family in registry["families"]
    }
