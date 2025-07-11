import PyInstaller.__main__
import shutil
import os

# Aufräumen vorheriger Builds
for folder in ['build', 'dist', '__pycache__']:
    if os.path.exists(folder):
        shutil.rmtree(folder)

# PyInstaller Optionen ohne --icon
opts = [
    'main.py',
    '--name=SmartTaskTool_by_Sevenof9',
    '--onefile',
    #'--console',
    '--noconsole',
    '--windowed',
    '--clean',
    '--log-level=WARN',
    '--add-data=gui.py;.',  # gui.py in dist/ kopieren
    '--add-data=tray.py;.',  # tray.py in dist/ kopieren
    '--add-data=hardware.py;.',  # hardware.py in dist/ kopieren
    '--add-data=restart_helper.py;.',  # restart_helper.py in dist/ kopieren
    '--add-data=DePixelSchmal.otf;.',
]

# Hidden-Imports
hidden_imports = [
    'win32com',
    'win32com.client',
    'pythoncom',
    'pystray._win32',
    'pystray._base',
    'wmi',
    'pynvml',
    'pystray',
    'PIL.Image',
    'PIL.ImageDraw',
    'PIL.ImageFont',
    'pythoncom',
    'wx',
    'difflib',
    'psutil'
]

for hidden in hidden_imports:
    opts.append(f'--hidden-import={hidden}')

PyInstaller.__main__.run(opts)
