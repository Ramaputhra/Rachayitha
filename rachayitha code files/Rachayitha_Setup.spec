# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/Users/Sm!le/Desktop/రచయిత/rachayitha code files/installer_src/setup_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/Sm!le/Desktop/రచయిత/rachayitha code files/dist/Rachayitha.exe', '.'), ('C:/Users/Sm!le/Desktop/రచయిత/rachayitha code files/rachayitha_logo.png', '.'), ('C:/Users/Sm!le/Desktop/రచయిత/rachayitha code files/icon.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Rachayitha_Setup',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:/Users/Sm!le/Desktop/రచయిత/rachayitha code files/icon.ico'],
)
