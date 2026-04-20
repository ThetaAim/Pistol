# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[os.path.abspath('.')],
    binaries=[],
    datas=[
        ('pkgs', 'pkgs'),  # Include the pkgs directory
        ('Scripts/Installer', 'Installer'),  # Include the Installer directory
        ('Scripts/Presets', 'Presets'),  # Include the Presets directory
        ('Scripts/Printers', 'Printers'),  # Include the Printers directory
        ('Data', 'Data'),  # Include the Data directory
        ('Tools', 'Tools'),  # Include the Tools directory
    ],
    hiddenimports=['encodings'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Pistol',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='x86_64',  # ARM: change to 'arm64' and build with: arch -arm64 pyinstaller main.spec --distpath ./Exported/dist_arm
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)

app = BUNDLE(
    coll,
    name='Pistol.app',
    icon='Icons/Icons.icns',
    bundle_identifier='com.yourcompany.main',
)
