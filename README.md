# Pistol — Printer Installer

> A one-click macOS utility that silently installs, configures, and presets an entire print fleet for end users.

---

## What It Does

Pistol automates the full printer deployment workflow on macOS:

1. **Installs all driver packages** (`.pkg`) using AppleScript with elevated privileges — including the YSoft SafeQ client for pull-print authentication.
2. **Creates and registers printers** via `lpadmin`, applying model-specific PPDs and IP addresses.
3. **Copies print presets** directly into the user's macOS preferences, so every printer is ready with the correct paper, tray, and finishing defaults out of the box.

---

## Printers Deployed

| Queue Name | Model | Notes |
|---|---|---|
| **Fiery** | Ricoh Pro C7200S (E-35A PS) | Finisher + Perfect Binder configured |
| **Color** | Ricoh IM C3000 | 1-cassette tray option |
| **Unique** | Ricoh MP C4504 | Default settings |
| **Black** | Toshiba e-STUDIO 4528A | Drawer stack configured |

All printers are connected over the local network and registered under a shared print server location.

---

## Architecture

```
Pistol/
├── main.py                  # Entry point — auth gate + Tkinter UI
├── Data/
│   └── Data.py              # Package paths & printer config table
├── Scripts/
│   ├── Installer/
│   │   └── tk_installer.py  # AppleScript-based .pkg runner with live log output
│   ├── Printers/
│   │   └── Create_printer_with_settings.py  # lpadmin wrapper
│   └── Presets/
│       └── Copy_Prst.py     # Copies .plist presets to ~/Library/Preferences
├── pkgs/
│   ├── Black/               # Toshiba driver package
│   ├── Color/               # Ricoh Color driver package
│   ├── Fiery/               # Fiery driver package
│   ├── Uniqe/               # Ricoh Unique driver package
│   ├── Ysoft/               # YSoft SafeQ client package
│   └── Presets/             # Apple print preset plists
└── Tools/
    └── tools.py             # Path resolution utilities
```

---

## How It Works

### 1. Authentication
The app opens with a password prompt. Only authorized technicians can proceed — everyone else gets a silent exit.

### 2. Package Installation
All `.pkg` files are passed through the same install loop via `osascript`, which triggers macOS's native admin privilege dialog. This includes the YSoft SafeQ client (first in the queue), followed by each printer driver. All packages run in a single authenticated session. Output is streamed live into the UI text log.

### 4. Printer Creation
After drivers are installed, the app calls `lpadmin` for each printer with:
- A display name and queue name
- The printer's IP address
- The correct PPD file path
- Model-specific hardware options (finishers, trays, drawers)

### 5. Preset Deployment
Pre-built `.plist` files (Apple's native print preset format) are copied into `~/Library/Preferences`, making custom paper sizes, quality settings, and tray selections immediately available in every app's print dialog.

---

## Setup — Adding Your Files

The `pkgs/` folders are intentionally empty in this repo. Before building or running, place your files as follows:

**Driver packages** — file names must match exactly as listed below:

```
pkgs/Black/        → Black.pkg
pkgs/Color/        → color.pkg
pkgs/Fiery/        → fiery.pkg
pkgs/Uniqe/        → unique.pkg
pkgs/Ysoft/        → Ysoft.pkg
```

> **Note:** File names are case-sensitive and must match exactly. If a file is missing or misnamed, the installer will skip it silently.

> **SafeQ users:** If your organization uses [YSoft SafeQ](https://www.ysoft.com) as a print management platform, place the **SafeQ Client installer** (`.pkg`) in `pkgs/Ysoft/`. This is the pull-print client that authenticates users at the printer via badge or PIN. Without it, secure print release will not function. Obtain the installer from your SafeQ administrator or the YSoft portal.

**Print presets** — drop your `.plist` files into:

```
pkgs/Presets/      → com.apple.print.custompresets.*.plist
                   → com.apple.print.add.plist
```

These are Apple's native print preset format — export them from `~/Library/Preferences` on a configured machine.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| UI | Tkinter |
| Installer execution | AppleScript via `osascript` |
| Printer management | CUPS / `lpadmin` |
| Distribution | PyInstaller (standalone `.app`) |
| Platform | macOS — Apple Silicon & Intel |

---

## Requirements

- macOS Sonoma or later
- Network access to the printer subnet
- Administrator credentials (prompted at install time)

---

*Built by [OREN Ohayon](https://github.com/ThetaAim)*