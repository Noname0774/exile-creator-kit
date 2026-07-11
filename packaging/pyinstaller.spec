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
datas += optional_binary(PROJECT_DIR / "VERSION", ".")
datas += optional_binary(PROJECT_DIR / "LICENSE", ".")
datas += optional_data_tree(PROJECT_DIR / "assets" / "branding", "assets/branding")
datas += optional_data_tree(PROJECT_DIR / "assets" / "icons", "assets/icons")
datas += optional_data_tree(PROJECT_DIR / "LICENSES", "LICENSES")

hiddenimports = []
hiddenimports += collect_submodules("tkinter")
hiddenimports += collect_submodules("tkinterdnd2")
hiddenimports += [
    "PIL",
    "PIL.Image",
    "PIL.ImageTk",
    "core.export",
    "core.export.generic_exporter",
    "core.export.history",
    "core.export.preflight",
    "core.export.presets",
    "core.export.profile",
    "core.export.queue",
    "core.export.x_exporter",
    "core.export.youtube_exporter",
    "core.media",
    "core.media.ffprobe_adapter",
    "core.media.ffprobe_parser",
    "core.media.info",
    "core.media.inspector",
    "core.media.media_summary",
    "core.media.smart_bitrate",
    "core.settings",
    "core.settings.defaults",
    "core.settings.model",
    "core.settings.repository",
    "core.settings.service",
    "core.settings.validator",
    "core.storage.path_resolver",
    "core.system",
    "core.system.diagnostics",
    "core.system.encoder_selector",
    "core.system.environment",
    "core.system.gpu_detector",
    "gui.about_window",
    "gui.components.export_card",
    "gui.components.header",
    "gui.components.media_card",
    "gui.components.recent_exports_card",
    "gui.components.status_card",
    "gui.components.theme",
    "gui.settings_window",
    "tkinterdnd2",
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
