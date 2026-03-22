# AppSiteBlocker

A Windows console app that blocks websites and kills forbidden processes.

## What it does

- Blocks sites by editing `C:\Windows\System32\drivers\etc\hosts`
- Kills processes whose names match keywords in the config
- Minimizes to the system tray
- Logs all activity to `appsiteblocker.log`

## Requirements

- Windows 10 / 11
- Python 3.10+
- Administrator privileges (needed to edit the hosts file)

## Install

```
pip install -r requirements.txt
```

## Run

```
python main.py
```

Run as Administrator — otherwise site blocking will fail.

## Config

Edit `config.json`:

```json
{
    "blocked_sites": [
        "example.com"
    ],
    "blocked_apps": [
        "notepad"
    ]
}
```

- `blocked_sites` — domains to redirect to `127.0.0.1`. `www.` is added automatically.
- `blocked_apps` — process name keywords to kill (case-insensitive).

Press **3** in the menu to reload config without restarting.

## Menu

```
1  enable protection
2  disable protection
3  reload config
4  minimize to tray
5  exit
```

## License

MIT
