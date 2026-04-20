import os
from Tools.tools import to_absolute

packages = [
    (to_absolute('../pkgs/Ysoft/Ysoft.pkg'), 'Ysoft'),
    (to_absolute('../pkgs/Fiery/fiery.pkg'), 'Fiery'),
    (to_absolute('../pkgs/Color/color.pkg'), 'Color'),
    (to_absolute('../pkgs/Uniqe/unique.pkg'), 'Unique'),
    (to_absolute('../pkgs/Black/Black.pkg'), 'Black')
]
uninstall_path = [to_absolute('../pkgs/Uninstaller/')]

printer_configs = [
    (
        "Fiery", "172.16.100.100", "ColB",
        "/Library/Printers/PPDs/Contents/Resources/en.lproj/Pro C7200Sseries E-35A PS 1.0", "MainFarm",
        {"EFPaperDeckOpt": "Option2", "EFFinisher": "Finisher7", "EFPerfectBinder": True}
    ),
    (
        "Color", "172.16.100.100", "ColS",
        "/Library/Printers/PPDs/Contents/Resources/RICOH IM C3000", "MainFarm",
        {"OptionTray": "1Cassette"}
    ),
    (
        "Unique", "172.16.100.100", "Tos",
        "/Library/Printers/PPDs/Contents/Resources/RICOH MP C4504", "MainFarm",
        {}
    ),
    (
        "Black", "172.16.100.100", "BWS",
        "/Library/Printers/PPDs/Contents/Resources/TOSHIBA_MonoMFP.gz", "MainFarm",
        {"ModelSelection": "e-STUDIO4528ASeries", "Pedestal": "Drawer1234"}
    )
]
