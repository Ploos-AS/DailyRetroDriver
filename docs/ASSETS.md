# Asset and preservation policy

Proprietary ROMs, firmware, operating systems, disk images, and commercial
software are never committed to this repository or downloaded by provisioning.
Users supply assets they are legally entitled to use. This includes concepts
such as Amiga Kickstart and system volumes, Atari TOS, optional JiffyDOS, and
software media; naming a work does not provide or authorize it.

The manifest records a stable logical ID, relative path, SHA-256 digest,
required/optional status, associated profiles, classification, provenance, and
an optional license reference. SHA-256 establishes file identity and detects
corruption. It does **not** establish copyright ownership, a license, or
distribution permission. Provenance records should describe how the local user
obtained or created the asset without exposing secrets.

Supported source classifications are:

* `user_supplied`: provided locally under the user's responsibility;
* `freeware`: published for no-cost use under stated terms;
* `open_source`: covered by an identified open-source license;
* `redistributable`: permission to redistribute has been verified and recorded.

Classification alone is not proof. Preserve a license reference or provenance
note and review the actual terms. Open alternatives such as EmuTOS may be
supported as optional assets without forcing them over a user's lawful original
firmware. `assets/manifest.example.yml` contains placeholder hashes only; local
manifests and asset payloads are ignored by Git.
