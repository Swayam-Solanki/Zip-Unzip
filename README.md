# Zip Unzip & Media Tools 🗜️🎬

A collection of lightweight, robust Python utility scripts for secure bulk ZIP archive extraction and media file conversion.

---

## Features

### 1. Safe Bulk ZIP Extractor ([zip_unzip.py](file:///c:/Users/Swayam%20B%20Solanki/Documents/PROJECTS/Zip%20Unzip/zip_unzip.py))
Extracts multiple `.zip` files in a given directory with advanced safeguards and customizable options:
- **Zip-Slip Protection:** Built-in path traversal security prevents files from extracting outside the destination directory.
- **Bulk Extraction:** Extract all ZIPs in a target directory at once.
- **Recursive Mode:** Option to recursively search subdirectories for ZIP files (`-r` or `--recursive`).
- **Archive Isolation:** By default, creates a dedicated subfolder for each ZIP archive to prevent filename collisions and overwrite issues. Supports a `--flat` flag to disable this.
- **Corrupt File Validation:** Pre-validates ZIP file integrity before extraction.
- **Interactive or CLI Mode:** Runs with command-line arguments or prompts you for paths if run interactively.

### 2. AVI to MP4 Converter ([avi_to_mp4.py](file:///c:/Users/Swayam%20B%20Solanki/Documents/PROJECTS/Zip%20Unzip/avi_to_mp4.py))
Converts `.avi` video files to modern `.mp4` format:
- **H.264 & AAC Encoding:** Encodes video to H.264 (`libx264`) and audio to AAC (`aac`) for high compatibility.
- **Simple Execution:** Run as a standalone script or integrate into other Python pipelines.

---

## Installation & Setup

### Prerequisites
- **Python 3.x**
- **FFmpeg** (required for [avi_to_mp4.py](file:///c:/Users/Swayam%20B%20Solanki/Documents/PROJECTS/Zip%20Unzip/avi_to_mp4.py))
  - **Windows:** Download from [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or install via [Chocolatey](https://chocolatey.org/): `choco install ffmpeg` or [Scoop](https://scoop.sh/): `scoop install ffmpeg`.
  - **macOS:** Install via Homebrew: `brew install ffmpeg`
  - **Linux:** Install via apt: `sudo apt install ffmpeg`

### Cloning the Repository
```bash
git clone https://github.com/Swayam-Solanki/Zip-Unzip.git
cd Zip-Unzip
```

---

## Usage Guide

### 1. ZIP Extractor (`zip_unzip.py`)

#### Command Line Arguments
```bash
python zip_unzip.py [input_folder] [output_folder] [options]
```

| Parameter / Flag | Description |
| :--- | :--- |
| `input_folder` | *(Optional)* Path to directory containing ZIP files. |
| `output_folder` | *(Optional)* Destination folder for extracted contents. |
| `-r`, `--recursive` | Recursively search subdirectories of `input_folder` for ZIP files. |
| `--flat` | Extract all files directly into `output_folder` instead of creating subfolders named after each archive. |

#### Examples

**Basic CLI Usage:**
```bash
python zip_unzip.py ./archives ./extracted
```

**Recursive Extraction with Flat Structure:**
```bash
python zip_unzip.py ./archives ./extracted -r --flat
```

**Interactive Mode:**
If you run the script without arguments, it will prompt you for the input and output folders:
```bash
python zip_unzip.py
```

---

### 2. AVI to MP4 Converter (`avi_to_mp4.py`)

To convert an AVI video file, modify the example script or import the function into your project:

#### Inline Usage (Edit script or import):
```python
from avi_to_mp4 import convert_avi_to_mp4

# Converts 'input.avi' to 'output.mp4' in the current folder
convert_avi_to_mp4("input.avi", "output.mp4")
```

#### Run Directly:
```bash
python avi_to_mp4.py
```

---

## Safety Features

### Zip-Slip Guard
Zip-Slip is a critical directory traversal vulnerability that allows attackers to write arbitrary files outside the extraction directory. [zip_unzip.py](file:///c:/Users/Swayam%20B%20Solanki/Documents/PROJECTS/Zip%20Unzip/zip_unzip.py) protects against this by verifying that each extracted member's target path resolves strictly inside the destination folder.

```python
def is_within_directory(directory: Path, target: Path) -> bool:
    try:
        directory = directory.resolve()
        target = target.resolve()
        return directory in target.parents or directory == target
    except OSError:
        return False
```

If a member attempts to escape the directory, extraction is blocked, the file is skipped, and an error is logged.

---

## License
This project is open-source. Feel free to modify and adapt it for your own scripts and workflows!
