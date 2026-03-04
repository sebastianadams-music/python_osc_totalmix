# TotalMix OSC Mouse Bridge

A background macOS service that maps your mouse wheel to the RME TotalMix Master Fader using OSC.

## How to use:
- **Ctrl + Scroll**: Adjust Master Volume.
- **Ctrl + Middle Click**: Reset Volume to c. -20dB (change this to whatever value you want).
- **Bi-directional Sync**: If you move the fader in TotalMix, the script stays updated.

## Installation:

1. **Clone/Move project** to your preferred location (e.g., `/Volumes/seb/Projects/...`).
2. **Create Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
3. **Configure TotalMix**:

Open TotalMix FX > Options > Settings > OSC.

Enable Controller 1 for OSC

In Port: 7001, Out Port: 7002, Remote IP: 127.0.0.1. (this is your own machine's internal address)

Install Launch Agent:

Open com.user.python.osc.totalmix.plist.

Update the paths to match your .venv and main.py.

Move the file to ~/Library/LaunchAgents/.

Load it:

Bash
launchctl load ~/Library/LaunchAgents/com.user.python.osc.totalmix.plist
Permissions:

Go to System Settings > Privacy & Security > Accessibility.

Add your .venv/bin/python3 executable to the allowed list. (It will appear just as "python3" I think)

Check logs if things aren't working:

tail -f /tmp/totalmix_osc.err (Errors)

tail -f /tmp/totalmix_osc.out (Activity)
