# -*- mode: python ; coding: utf-8 -*-
# Script PyInstaller pour Outil de Maintenance Système
# Auteur: c.Lecomte
# Version: 2.1

block_cipher = None

a = Analysis(
    ['../src/OutilMaintenance.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../docs/GUIDE_NOUVELLES_FONCTIONS.md', '.'),
        ('../docs/AMELIORATIONS.md', '.'),
        ('../docs/README.txt', '.'),
        ('../docs/LICENSE.txt', '.'),
    ],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'reportlab',
        'reportlab.lib',
        'reportlab.lib.pagesizes',
        'reportlab.platypus',
        'reportlab.lib.styles',
        'reportlab.lib.colors',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'tkinter',
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
    name='OutilMaintenance',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Mode fenêtré (pas de console)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='../assets/icon.ico',  # Icône de l'application
    version='version_info.txt',  # Informations de version
    uac_admin=True,  # Demander les droits admin au lancement
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='OutilMaintenance',
)
