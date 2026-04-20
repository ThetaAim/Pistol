# Pistol — Printer Installer

> A one-click macOS utility that silently installs, configures, and presets an entire print fleet for end users.

---

## What It Does

Pistol automates the full printer deployment workflow on macOS:

1. **Installs driver packages** (`.pkg`) using AppleScript with elevated privileges — no manual steps for the user.
2. **Creates and registers printers** via `lpadmin`, applying model-specific PPDs and IP addresses.
3. **Copies print presets** directly into the user's macOS preferences, so every printer is ready with the correct paper, tray, and finishing defaults out of the box.
4. **Self-destructs** — the `.app` bundle deletes itself after the user quits, leaving no installer artifacts behind.

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
│   └── Presets/             # Pre-configured Apple print preset plists
└── Tools/
    └── tools.py             # Path resolution utilities
```

---

## How It Works

### 1. Authentication
The app opens with a password prompt. Only authorized technicians can proceed — everyone else gets a silent exit.

### 2. Package Installation
Each driver `.pkg` is passed to `installer` via `osascript`, which triggers macOS's native admin privilege dialog. All packages run in a single authenticated session. Output is streamed live into the UI text log.

### 3. Printer Creation
After drivers are installed, the app calls `lpadmin` for each printer with:
- A display name and queue name
- The printer's IP address
- The correct PPD file path
- Model-specific hardware options (finishers, trays, drawers)

### 4. Preset Deployment
Pre-built `.plist` files (Apple's native print preset format) are copied into `~/Library/Preferences`, making custom paper sizes, quality settings, and tray selections immediately available in every app's print dialog.

### 5. Self-Cleanup
On quit, a background shell command (`sleep 3 && rm -rf`) removes the `.app` bundle — so the installer never lingers on the user's machine.

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