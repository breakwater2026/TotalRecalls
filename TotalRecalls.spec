# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_submodules

datas = [('app_ui.html', '.')]
# React UI build output (preferred by totalrecalls.desktop.main)
import os
import sys
if os.path.isdir('ui'):
    datas.append(('ui', 'ui'))
icon = 'app.ico' if sys.platform == 'win32' else None

binaries = []
hiddenimports = collect_submodules('totalrecalls')
tmp_ret = collect_all('curl_cffi')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('webview')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('pythonnet')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['numpy', 'PIL', 'pillow', 'pyautogui', 'qtpy',
              'cefpython3', 'objc', 'PyObjCTools', 'AppKit', 'Foundation',
              'WebKit', 'jnius', 'android'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

# Build mode:
#   'onefile' (default) - single self-extracting EXE; used for the direct download.
#   'ondir'             - folder of files; used to build the Microsoft Store MSIX.
# tools/build_exe.py sets this via TR_BUILD_MODE. To build by hand:
#   TR_BUILD_MODE=onefile .venv\Scripts\python.exe -m PyInstaller TotalRecalls.spec
#   TR_BUILD_MODE=onedir  .venv\Scripts\python.exe -m PyInstaller TotalRecalls.spec
MODE = os.environ.get('TR_BUILD_MODE', 'onefile').strip().lower()
if MODE not in ('onefile', 'onedir'):
    raise SystemExit(f"ERROR: TR_BUILD_MODE must be 'onefile' or 'onedir', got {MODE!r}")

if MODE == 'onedir':
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='TotalRecalls',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=icon,
    )
    coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name='TotalRecalls',
    )
else:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        name='TotalRecalls',
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
        icon=icon,
    )
