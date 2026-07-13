#!/usr/bin/env python3
"""
unzip_all.py

Recursively extracts all ZIP files found in an input folder into an output
folder, with protection against zip-slip path traversal, proper error
handling, and per-archive extraction folders to avoid filename collisions.
"""

import argparse
import logging
import os
import sys
import zipfile
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


def is_within_directory(directory: Path, target: Path) -> bool:
    """Check that `target` resolves to a path inside `directory` (zip-slip guard)."""
    try:
        directory = directory.resolve()
        target = target.resolve()
        return directory in target.parents or directory == target
    except OSError:
        return False


def safe_extract(zip_ref: zipfile.ZipFile, dest: Path) -> None:
    """Extract a zip file, refusing any member that would escape `dest`."""
    for member in zip_ref.infolist():
        member_path = dest / member.filename
        if not is_within_directory(dest, member_path):
            raise ValueError(
                f"Blocked potentially unsafe path in archive: {member.filename}"
            )
    zip_ref.extractall(dest)


def unzip_all(
    input_folder: str,
    output_folder: str,
    recursive: bool = False,
    per_archive_subfolder: bool = True,
) -> tuple[int, int]:
    """
    Extract all .zip files from `input_folder` into `output_folder`.

    Returns (success_count, failure_count).
    """
    input_path = Path(input_folder).expanduser()
    output_path = Path(output_folder).expanduser()

    if not input_path.is_dir():
        raise NotADirectoryError(f"Input folder does not exist: {input_path}")

    output_path.mkdir(parents=True, exist_ok=True)

    pattern = "**/*.zip" if recursive else "*.zip"
    zip_files = sorted(
        p for p in input_path.glob(pattern) if p.suffix.lower() == ".zip"
    )

    if not zip_files:
        log.warning("No ZIP files found in %s", input_path)
        return 0, 0

    success = 0
    failure = 0

    for zip_path in zip_files:
        # Give each archive its own subfolder (named after the zip) to avoid
        # different archives silently overwriting each other's files.
        if per_archive_subfolder:
            dest = output_path / zip_path.stem
        else:
            dest = output_path
        dest.mkdir(parents=True, exist_ok=True)

        log.info("Extracting: %s -> %s", zip_path, dest)

        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                bad_file = zip_ref.testzip()
                if bad_file is not None:
                    raise zipfile.BadZipFile(f"Corrupt member: {bad_file}")
                safe_extract(zip_ref, dest)
            success += 1
        except zipfile.BadZipFile:
            log.error("Not a valid zip file, skipping: %s", zip_path)
            failure += 1
        except ValueError as e:
            log.error("Skipped %s: %s", zip_path, e)
            failure += 1
        except OSError as e:
            log.error("OS error while extracting %s: %s", zip_path, e)
            failure += 1

    log.info("Done. %d succeeded, %d failed.", success, failure)
    return success, failure


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract all ZIP files in a folder.")
    parser.add_argument("input_folder", nargs="?", help="Folder containing ZIP files")
    parser.add_argument("output_folder", nargs="?", help="Folder to extract into")
    parser.add_argument(
        "-r", "--recursive", action="store_true",
        help="Also search subfolders of the input folder for ZIP files",
    )
    parser.add_argument(
        "--flat", action="store_true",
        help="Extract all archives directly into the output folder "
             "instead of one subfolder per archive",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    input_folder = args.input_folder or input(
        "Enter the path to the folder containing ZIP files: "
    ).strip()
    output_folder = args.output_folder or input(
        "Enter the path for the output folder: "
    ).strip()

    try:
        success, failure = unzip_all(
            input_folder,
            output_folder,
            recursive=args.recursive,
            per_archive_subfolder=not args.flat,
        )
    except NotADirectoryError as e:
        log.error(str(e))
        return 1

    return 0 if failure == 0 else 2


if __name__ == "__main__":
    sys.exit(main())