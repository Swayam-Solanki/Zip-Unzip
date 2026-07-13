import subprocess
import sys
import os

def convert_avi_to_mp4(input_path, output_path=None):
    """
    Convert an AVI file to MP4 using ffmpeg.
    
    Args:
        input_path (str): Path to the input .avi file
        output_path (str): Path for the output .mp4 file (optional)
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + ".mp4"

    command = [
        "ffmpeg",
        "-i", input_path,      # input file
        "-c:v", "libx264",     # video codec
        "-c:a", "aac",         # audio codec
        "-strict", "experimental",
        "-y",                   # overwrite output if it exists
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"✅ Conversion complete: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Conversion failed: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ ffmpeg not found. Install it first (see notes below).")
        sys.exit(1)


if __name__ == "__main__":
    # Example usage
    convert_avi_to_mp4("input.avi", "output.mp4")