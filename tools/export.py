"""Unified export launcher."""

import subprocess
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python tools/export.py <media-file>")
        return 1

    media_path = sys.argv[1]
    media_name = Path(media_path).name
    tools_dir = Path(__file__).resolve().parent

    print("====================================")
    print("Exile Creator Kit")
    print()
    print("Video:")
    print(media_name)
    print()
    print("What would you like to do?")
    print()
    print("1. 📤 Export for X")
    print("   Optimized for X posting (512 MB)")
    print()
    print("2. 📺 Export for YouTube")
    print("   High quality export")
    print()
    print("0. Exit")
    print("====================================")

    choice = input("> ").strip()

    if choice == "1":
        script_path = tools_dir / "export_to_x.py"
        print("Preparing X export...")
    elif choice == "2":
        script_path = tools_dir / "export_to_youtube.py"
        print("Preparing YouTube export...")
    elif choice == "0":
        print("Canceled.")
        return 0
    else:
        print("Invalid selection.")
        return 1

    result = subprocess.run([sys.executable, str(script_path), media_path])
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
