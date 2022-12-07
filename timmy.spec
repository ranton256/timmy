# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['timmy.py'],
             pathex=['C:\\Users\\ranto\\pyinstall_test'],
             binaries=[],
             datas=[
                ('images', 'images'),
                ('sounds', 'sounds'),
                ('music', 'music'),
                ('fonts', 'fonts'),
                ('text_utils.py', '.'),
                ('high_scores.py', '.'),
                ('levels.py', '.'),
                ('timmy1.py', '.'),
                ('README.txt', '.')
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='timmy',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
