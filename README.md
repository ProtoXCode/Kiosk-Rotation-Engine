# 🖥️ Kiosk Rotation Engine

A lightweight, self‑hosted digital signage engine for kiosk displays.

Drop files in a folder. Screens update automatically. No cloud. No accounts.
No nonsense.

---

## ✨ Features

* 📂 Folder‑based rotation (images, videos, HTML)
* 🔄 Live updates — viewers refresh automatically
* 🧠 Playlist versioning (safe, flicker‑free updates)
* 🖥️ Fullscreen kiosk player (browser‑based)
* 🛡️ Fault‑tolerant (missing files won’t crash playback)
* ⚙️ Simple YAML configuration
* 🐧 Works on Linux, Windows, Raspberry Pi

---

## 🚀 Quick Start

```bash
git clone https://github.com/ProtoXCode/Kiosk-Rotation-Engine.git
cd kiosk-rotation-engine
pip install -r requirements.txt
python run.py
```

Open in a browser:

```
http://<host>:8080
```

(Use fullscreen / kiosk mode for production screens.)

---

## 📁 Adding Content

Put files into the **rotation directory** (default: `rotation/`).

Supported formats:

* Images: `.jpg`, `.png`, `.jpeg`
* HEIC / HEIF: `.heic`, `.heif` (auto‑converted to JPEG)
* Video: `.mp4`, `.webm`
* HTML: `.html` (rendered via iframe)
* URL: `'.url` (rendered via iframe, target site must allow to be built in)

Changes are picked up automatically — no reload, no restart.

---

## ⚙️ Configuration (`config.yaml`)

Example:

```yaml
rotation:
  media_directory: /srv/kiosk/rotation
  default_duration: 10
  image_duration: 10
  playlist_scan: 60
  video_mute: true
```

* **media_directory** – Folder watched for content
* **default_duration** – Fallback duration (seconds)
* **image_duration** – Image display time
* **playlist_scan** – Backend rescan interval (seconds)
* **video_mute** – Start videos muted

---

## 🧠 How It Works (Short Version)

* Backend scans the rotation folder on a fixed interval
* Builds a versioned playlist
* Viewers fetch the playlist and play it sequentially
* Updates are applied cleanly on the next loop

No polling storms. No race conditions. No broken screens.

---

## ⚠️ Design Notes

* No authentication (intended for trusted networks)
* No admin UI — filesystem is the source of truth
* Not designed for public internet exposure

---

## 📜 License

MIT License

Use it, break it, improve it — just don’t put it behind a paywall 😎
