# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['login.py'],
    pathex=[],
    binaries=[('C:\\Program Files\\MySQL\\MySQL Server 8.0\\lib\\libmysql.dll', '.')],
    datas=[('Bg1.png', '.'), ('sunglasses.ico', '.'), ('C:\\Users\\TUFF\\AppData\\Roaming\\Python\\Python312\\site-packages\\tkcalendar', 'tkcalendar')],
    hiddenimports=['tkcalendar', 'PIL.Image', 'PIL.ImageTk', 'PIL._imaging', 'matplotlib.backends.backend_tkagg', 'matplotlib.pyplot', 'matplotlib.dates', 'mplcursors', 'dateutil.relativedelta', 'mysql.connector', 'mysql'],
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
    [],
    exclude_binaries=True,
    name='login',
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
    icon=['sunglasses.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='login',
)
