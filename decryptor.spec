# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py',
    'db/database.py',
    'db/access_database.py',
    'db/sqlitedatabase.py',
    'crypto/decryptor.py',
    'crypto/keystore.py',
    'cmd_parser/command.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['cryptography', 'pywin32', 'pypiwin32'],
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
    name='decryptor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
