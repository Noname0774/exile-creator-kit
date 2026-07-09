# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller build configuration for Exile Creator Kit."""

from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

PACKAGING_DIR = Path(SPECPATH)
PROJECT_DIR = PACKAGING_DIR.parent

APP_NAME = "ExileCreatorKit"
ENTRY_POINT = PROJECT_DIR / "gui" / "main_window.py"
VENDOR_FFMPEG_DIR = PROJECT_DIR / "vendor" / "ffmpeg"
ICON_FILE = PROJECT_DIR / "assets" / "icons" / "exile-creator-kit.ico"


def optional_binary(source: Path, destination: str) -> list[tuple[str, str]]:
    """Return a PyInstaller binary entry when the source exists."""
    if source.exists():
        return [(str(source), destination)]

    return []


def optional_data_tree(source: Path, destination: str) -> list[tuple[str, str]]:
    """Return a PyInstaller data entry when the source directory exists."""
    if source.exists():
        return [(str(source), destination)]

    return []


binaries = []
binaries += optional_binary(VENDOR_FFMPEG_DIR / "ffmpeg.exe", ".")
binaries += optional_binary(VENDOR_FFMPEG_DIR / "ffprobe.exe", ".")

datas = []
datas += optional_data_tree(PROJECT_DIR / "assets" / "icons", "assets/icons")
datas += optional_data_tree(PROJECT_DIR / "LICENSES", "LICENSES")
datas += optional_data_tree(PROJECT_DIR / "tools", "tools")

hiddenimports = []
hiddenimports += collect_submodules("tkinter")
hiddenimports += collect_submodules("tkinterdnd2")
hiddenimports += [
    "core.export",
    "core.export.generic_exporter",
    "core.export.history",
    "core.export.profile",
    "core.export.queue",
    "core.export.x_exporter",
    "core.export.youtube_exporter",
    "core.media",
    "core.media.ffprobe_adapter",
    "core.media.ffprobe_parser",
    "core.media.info",
    "core.media.inspector",
    "core.media.smart_bitrate",
    "core.settings",
    "core.settings.defaults",
    "core.settings.model",
    "core.settings.repository",
    "core.settings.service",
    "core.settings.validator",
    "core.storage.path_resolver",
    "gui.about_window",
    "gui.settings_window",
    "tools.export_to_x",
    "tools.export_to_youtube",
]

a = Analysis(
    [str(ENTRY_POINT)],
    pathex=[str(PROJECT_DIR)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "pytest",
        "unittest",
        "pydoc",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(ICON_FILE) if ICON_FILE.exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=APP_NAME,
)
