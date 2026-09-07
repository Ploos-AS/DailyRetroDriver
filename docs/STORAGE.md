# Storage policy

Daily Retro Driver separates the replaceable host OS, auditable assets, and
mutable state. `/etc/daily-retro-driver` can be reconstructed from versioned
configuration. `/srv/daily-retro-driver/assets`, `media`, and `state` cannot be
assumed reproducible and require backups; manifests and reports should be backed
up with them. Backups should be stored on a different device, with restore tests
and filesystem-level consistency handled in M6.

Hardware policy is capability-driven:

* Raspberry Pi 400 has no built-in NVMe. A reliable USB 3 SSD is the recommended
  persistent target; an SD card may host DietPi but should not be the sole copy
  of mutable data.
* Raspberry Pi 500 has Pi 5-class performance, but policy must not assume
  integrated NVMe. Prefer a USB 3 SSD unless detection finds a separately
  supported persistent target.
* Raspberry Pi 500+ should use integrated NVMe for the canonical runtime tree
  when present and healthy, with USB 3 SSD as a fallback.

M0 creates the canonical tree on the root filesystem and records policy only.
It does not partition, format, mount, migrate, or erase storage. Later storage
work must identify devices by stable IDs, require explicit migration decisions,
preserve recoverability, and remain safe to repeat.
