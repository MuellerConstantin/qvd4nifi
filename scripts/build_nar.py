"""
Build a NiFi NAR file from the current project.
"""

import datetime
import shutil
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import tomllib

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
BUILD = ROOT / "build"
PACKAGE_DIR = ROOT / "qvd4nifi"
PYPROJECT = ROOT / "pyproject.toml"

def read_project_metadata():
    """
    Read the project name and version from pyproject.toml.
    """
    with open(PYPROJECT, "rb") as f:
        data = tomllib.load(f)

    poetry = data["tool"]["poetry"]

    name = poetry["name"]
    version = poetry["version"]

    return name, version

def create_manifest(name, version):
    """
    Create the MANIFEST.MF file for the NAR.
    """
    manifest_dir = BUILD / "META-INF"
    manifest_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    content = "\n".join(
        [
            "Manifest-Version: 1.0",
            "Created-By: qvd4nifi-nar-builder",
            f"Build-Timestamp: {timestamp}",
            f"Nar-Id: {name}-nar",
            f"Nar-Group: {name}",
            f"Nar-Version: {version}",
            "",
        ]
    )

    (manifest_dir / "MANIFEST.MF").write_text(content)

def install_dependencies():
    """
    Install the project dependencies into the NAR-INF/bundled-dependencies directory.
    """
    target = BUILD / "NAR-INF" / "bundled-dependencies"
    target.mkdir(parents=True, exist_ok=True)

    requirements_file = BUILD / "requirements.txt"

    subprocess.check_call(
        [
            "poetry",
            "export",
            "-f",
            "requirements.txt",
            "--without-hashes",
            "-o",
            str(requirements_file),
        ]
    )

    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-r",
            str(requirements_file),
            "--upgrade",
            "--target",
            str(target),
        ]
    )

def copy_package():
    """
    Copy the project package into the NAR.
    """
    target = BUILD / "qvd4nifi"
    shutil.copytree(PACKAGE_DIR, target)

def build_nar(name, version):
    """
    Create the NAR file by zipping the contents of the build directory.
    """
    DIST.mkdir(exist_ok=True)

    nar_file = DIST / f"{name}-{version}.nar"

    with ZipFile(nar_file, "w", ZIP_DEFLATED) as z:
        for path in BUILD.rglob("*"):
            if path.is_file():
                z.write(path, path.relative_to(BUILD))

    print("Created", nar_file)

def clean():
    """
    Clean the build directory.
    """
    if BUILD.exists():
        shutil.rmtree(BUILD)

def main():
    """
    Main function to build the NAR.
    """
    clean()

    name, version = read_project_metadata()

    create_manifest(name, version)
    install_dependencies()
    copy_package()
    build_nar(name, version)

    clean()

if __name__ == "__main__":
    main()
