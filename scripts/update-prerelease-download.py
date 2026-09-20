"""Keep a fixed download asset pointing at the highest published prerelease version."""
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
pages = json.loads(gh("api", "--paginate", "--slurp", f"repos/{repo}/releases?per_page=100"))
releases = [release for page in pages for release in page]
candidates = [r for r in releases if r["prerelease"] and not r["draft"] and re.fullmatch(r"v\d+\.\d+\.\d+", r["tag_name"])]
if not candidates:
    raise SystemExit("No published versioned prerelease found; existing download left unchanged.")
release = max(candidates, key=lambda r: tuple(map(int, r["tag_name"][1:].split("."))))
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
    alias = root / "all8-prerelease.zip"
    path.rename(alias)
    checksum = root / "SHA256SUMS.txt"
    checksum.write_text(f"{digest}  {alias.name}\n")
    notes = root / "notes.md"
    notes.write_text(f"최신 선공개 수집기 **{version}** 다운로드입니다.\n\n[버전별 릴리즈]({release['html_url']})\n\n웹의 고정 다운로드 링크를 위한 자동 갱신 채널입니다.\n")
    channel = next((r for r in releases if r["tag_name"] == "latest-prerelease"), None)
    if channel:
        gh("release", "upload", "latest-prerelease", str(alias), str(checksum), "--clobber", "--repo", repo)
        gh("release", "edit", "latest-prerelease", "--repo", repo, "--notes-file", str(notes), "--prerelease", "--latest=false")
    else:
        gh("release", "create", "latest-prerelease", str(alias), str(checksum), "--repo", repo, "--title", "최신 선공개 수집기 다운로드", "--notes-file", str(notes), "--prerelease", "--latest=false")
    print(f"Published download channel: {version}, sha256:{digest}")
