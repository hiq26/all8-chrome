"""Provide a direct ZIP asset on the GitHub Latest release."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import zipfile


def gh(*args):
    return subprocess.check_output(["gh", *args], text=True)


repo = os.environ["GH_REPO"]
# GitHub's Latest endpoint is authoritative; never choose the highest prerelease version.
release = json.loads(gh("api", f"repos/{repo}/releases/latest"))
if release["prerelease"] or release["draft"] or not re.fullmatch(r"v\d+\.\d+\.\d+", release["tag_name"]):
    raise SystemExit("Latest must be a published non-prerelease version")
version = release["tag_name"][1:]
asset_name = f"all8-{version}.zip"
asset = next((a for a in release["assets"] if a["name"] == asset_name), None)
if not asset or asset["state"] != "uploaded":
    raise SystemExit(f"Missing complete production asset: {asset_name}")
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    gh("release", "download", release["tag_name"], "--repo", repo, "--pattern", asset_name, "--dir", directory)
    path = root / asset_name
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if asset.get("digest") and asset["digest"] != f"sha256:{digest}":
        raise SystemExit("Release asset checksum mismatch")
    with zipfile.ZipFile(path) as archive:
        manifest = json.loads(archive.read("manifest.json"))
        if manifest["version"] != version or "staging" in manifest["name"].lower():
            raise SystemExit("Production manifest/version verification failed")
    alias = root / "all8-latest.zip"
    path.rename(alias)
    checksum = root / "SHA256SUMS.txt"
    checksum.write_text(f"{digest}  {alias.name}\n")
    # Assets do not trigger release edited events. Do not change release status or Latest selection.
    gh("release", "upload", release["tag_name"], str(alias), str(checksum), "--clobber", "--repo", repo)
    print(f"Published Latest download: {version}, sha256:{digest}")
