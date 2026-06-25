"""Google Drive mirror via platform connectors/googledrive (Node)."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from scripts.connectors import SyncResult

_CONNECTOR_DIR = Path(__file__).resolve().parents[2] / "connectors" / "googledrive"
_CLI = _CONNECTOR_DIR / "dist" / "cli.js"


def sync_googledrive_mirror(project_root: Path, source_config: dict) -> SyncResult:
    gd = source_config.get("googledrive") or {}
    folder_id = gd.get("folder_id") or os.environ.get("GOOGLE_DRIVE_FOLDER_ID")
    if not folder_id:
        raise ValueError("source.googledrive.folder_id or GOOGLE_DRIVE_FOLDER_ID is required")

    local_mirror = source_config.get("local_mirror", "build/corpus/drive")
    output_dir = (project_root / local_mirror).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if not _CLI.is_file():
        raise FileNotFoundError(
            f"Drive connector not built: {_CLI}. "
            "Run: cd connectors/googledrive && npm install && npm run build"
        )

    cmd = [
        "node",
        str(_CLI),
        "mirror",
        "--folder-id",
        str(folder_id),
        "--output-dir",
        str(output_dir),
    ]
    batch_size = gd.get("batch_size")
    if batch_size:
        cmd.extend(["--batch-size", str(batch_size)])

    env = os.environ.copy()
    proc = subprocess.run(cmd, cwd=_CONNECTOR_DIR, env=env, capture_output=True, text=True)
    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip() or "unknown error"
        raise RuntimeError(f"googledrive mirror failed: {detail}")

    summary = {}
    if proc.stdout.strip():
        try:
            summary = json.loads(proc.stdout)
        except json.JSONDecodeError:
            summary = {}

    manifest = output_dir / "mirror-manifest.json"
    return SyncResult(
        adapter="googledrive",
        local_mirror=output_dir,
        mirrored_count=int(summary.get("mirroredCount", 0)),
        failed_count=int(summary.get("failedCount", 0)),
        manifest_path=manifest if manifest.is_file() else None,
    )
