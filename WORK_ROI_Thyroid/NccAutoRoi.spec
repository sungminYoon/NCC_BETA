

block_cipher = None

a = Analysis(['main.py'],
             pathex=['C:\\WORK_ROI_Thyroid'],
             binaries=[],
             datas=[('./LAB/resource_ui', 'resource_ui'),
                    ('./LAB/build_lib/PySide6', 'PySide6')],
             hiddenimports=['pydicom.encoders.gdcm', 'pydicom.encoders.pylibjpeg'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

to_rem = ["PySide6.QtPrintSupport", "PySide6.QtSvg"]

for val in to_rem:
    for b in a.binaries:
        nb = b[0]
        if str(nb).endswith(val):
            print("removed  " + b[0])
            a.binaries.remove(b)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='NccAutoRoi',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )

