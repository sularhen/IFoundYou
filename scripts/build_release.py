from __future__ import annotations

import shutil
import subprocess
import tarfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
STAGING = DIST / "release-staging"
VERSION = "2.0.1"


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_common_files(destination: Path) -> None:
    (destination / "src").mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        ROOT / "src",
        destination / "src",
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", "*.egg-info"),
    )
    shutil.copy2(ROOT / "README.md", destination / "README.md")
    shutil.copy2(ROOT / "LICENSE", destination / "LICENSE")
    shutil.copy2(ROOT / "pyproject.toml", destination / "pyproject.toml")
    for unwanted in destination.rglob("__pycache__"):
        shutil.rmtree(unwanted, ignore_errors=True)
    for unwanted in destination.rglob("*.egg-info"):
        if unwanted.is_dir():
            shutil.rmtree(unwanted, ignore_errors=True)


def build_python_distributions() -> None:
    run(["python", "-m", "pip", "install", "--upgrade", "build"])
    run(["python", "-m", "build"])


def package_windows() -> Path:
    win_root = STAGING / f"ifoundyou-windows-{VERSION}"
    reset_dir(win_root)
    copy_common_files(win_root)
    shutil.copy2(ROOT / "whereareyou.ps1", win_root / "whereareyou.ps1")
    shutil.copy2(ROOT / "ifoundyou.cmd", win_root / "ifoundyou.cmd")
    shutil.copy2(ROOT / "release" / "install-windows.ps1", win_root / "install.ps1")

    archive = DIST / f"ifoundyou-windows-{VERSION}.zip"
    if archive.exists():
        archive.unlink()

    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file_path in win_root.rglob("*"):
            if file_path.is_file():
                zf.write(file_path, file_path.relative_to(STAGING))
    return archive


def package_linux() -> Path:
    linux_root = STAGING / f"ifoundyou-linux-{VERSION}"
    reset_dir(linux_root)
    copy_common_files(linux_root)
    shutil.copy2(ROOT / "ifoundyou", linux_root / "ifoundyou")
    shutil.copy2(ROOT / "whereareyou.sh", linux_root / "whereareyou.sh")
    shutil.copy2(ROOT / "release" / "install-linux.sh", linux_root / "install.sh")

    archive = DIST / f"ifoundyou-linux-{VERSION}.tar.gz"
    if archive.exists():
        archive.unlink()

    with tarfile.open(archive, "w:gz") as tar:
        tar.add(linux_root, arcname=linux_root.name)
    return archive


def main() -> None:
    DIST.mkdir(exist_ok=True)
    reset_dir(STAGING)
    build_python_distributions()
    windows_archive = package_windows()
    linux_archive = package_linux()
    print(f"Built release artifacts:\n- {windows_archive}\n- {linux_archive}")


if __name__ == "__main__":
    main()
