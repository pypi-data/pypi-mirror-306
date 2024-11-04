import os
from pathlib import Path
import platform
import shutil

import __main__
LOCAL_ASSET_DIR = os.path.join(os.path.dirname(__main__.__file__), ".aoe_assets/")

AOE_INSTALL_DIR = "AOE_INSTALL_NOT_FOUND"
AOE_COMMON_DIR = "AOE_INSTALL_NOT_FOUND"

if platform.system() == 'Windows':
    try:
        import winreg
        import vdf

        steam_key_x64 = r"SOFTWARE\Wow6432Node\Valve\Steam\NSIS"
        steam_key_x86 = r"SOFTWARE\Valve\Steam\NSIS"
        registry_handler = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        try:
            steam_key_handler = winreg.OpenKey(registry_handler, steam_key_x64)
        except OSError:
            steam_key_handler = winreg.OpenKey(registry_handler, steam_key_x86)

        steam_install_dir, _ = winreg.QueryValueEx(steam_key_handler, "Path")

        aoe_steam_appid = "221380"

        def check_for_aoe_steamappid(libraryfolder):
            for filename in os.listdir(str(Path(libraryfolder).joinpath("steamapps"))):
                if filename.endswith('.acf'):
                    with open(str(Path(libraryfolder).joinpath("steamapps").joinpath(filename)), 'r') as file:
                        steamapp = vdf.load(file)
                        if steamapp['AppState']['appid'] == aoe_steam_appid:
                            global AOE_INSTALL_DIR
                            AOE_INSTALL_DIR = str(Path(libraryfolder).joinpath("steamapps").joinpath("common").joinpath(steamapp['AppState']['installdir']))

        with open(str(Path(steam_install_dir).joinpath("steamapps").joinpath("libraryfolders.vdf")), 'r') as file:
            libraryfolders = vdf.load(file)
            for libraryfolder in libraryfolders['libraryfolders'].values():
                if type(libraryfolder) == dict:
                    check_for_aoe_steamappid(libraryfolder['path'])

        AOE_COMMON_DIR = AOE_INSTALL_DIR + "/resources/_common/"
    
    except:
        pass  # Was not able to find a suitable Age of Empires installation

def cache_aoe_file(filename):
    if gaia.is_packaged_simulation():
        return 
    
    if not os.path.exists(LOCAL_ASSET_DIR):
        os.makedirs(LOCAL_ASSET_DIR)

    try:
        if not os.path.exists(LOCAL_ASSET_DIR + Path(filename).name):
            shutil.copy2(filename, LOCAL_ASSET_DIR)
    except:
        pass

from .aoe_loader import *
from .aoe_moving_impostor import *
from .aoe_terrain import *