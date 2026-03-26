# 🖥️ Kiosk Rotation Engine

A lightweight, self-hosted digital signage engine for kiosk displays.

Drop files in a folder. Screens update automatically. No cloud. No accounts.
No nonsense.

---

## ✨ Features

* 📂 Folder-based rotation (images, videos, HTML)
* 📥 Network upload support (via shared drop folder)
* 🔄 Live updates — viewers refresh automatically
* 🧠 Playlist versioning (safe, flicker-free updates)
* 🖥️ Fullscreen kiosk player (browser-based)
* 🛡️ Fault-tolerant (invalid files are ignored)
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

## 📁 Content Workflow

This system uses a **two-stage content pipeline**:

```
Upload → Processing → Display
```

### 1. Upload (network share)

Files are dropped into an upload directory (e.g. via SMB/Samba):

```
/srv/uploads
```

This folder can be shared across the network so other machines can easily add content.

---

### 2. Processing (recommended)

A small processing step moves valid files into the live rotation directory:

```
/srv/display
```

Typical responsibilities:

* ✅ Allow only supported file types
* 🚫 Reject invalid or unsupported files
* 📦 Optionally enforce file size limits
* 🔄 Normalize or convert formats if needed

This prevents broken or unsupported files from reaching the display.

---

### 3. Display (app reads here)

The engine reads from the configured media directory:

```yaml
rotation:
  media_directory: /srv/display
```

Only processed, valid content should live here.

---

## 📁 Supported Content

### 🖼️ Images

* `.jpg`, `.jpeg`, `.png`, `.webp`
* `.heic`, `.heif` (auto-converted to JPEG)

### 🎬 Video

* `.mp4`, `.webm`

### 🌐 Web Content

* `.html` (rendered via iframe)
* `.url` (rendered via iframe — target site must allow embedding)

### 📄 Office Documents *(optional)*

* `.ppt`, `.pptx`
* `.doc`, `.docx`
* `.xls`, `.xlsx`
* `.pdf`

> Office files are converted before display (e.g. to images or PDF pages).

> ⚠️ Requires LibreOffice to be installed on the host system for document conversion support.

---

## ⚙️ Configuration (`config.yaml`)

Example:

```yaml
rotation:
  media_directory: /srv/display
  default_duration: 10
  image_duration: 10
  playlist_scan: 60
  video_mute: true
```

* **media_directory** – Folder used for playback (post-processing)
* **default_duration** – Fallback duration (seconds)
* **image_duration** – Image display time
* **playlist_scan** – Backend rescan interval (seconds)
* **video_mute** – Start videos muted

---

## 🧠 How It Works (Short Version)

* Backend scans the media directory on a fixed interval
* Builds a versioned playlist
* Viewers fetch the playlist and play it sequentially
* Updates are applied cleanly on the next loop

No polling storms. No race conditions. No broken screens.

---

## ⚠️ Design Notes

* No authentication (intended for trusted networks)
* Upload directory should **not** be used directly as media source
* Recommended to isolate upload and display directories
* Not designed for public internet exposure

---

## 🧩 Typical Setup

* Debian server running the engine
* Network share (SMB via Samba) mapped to `/srv/uploads`
* Background script or service processes uploads
* Clean media served from `/srv/display`

---

## 📜 License

MIT License

Use it, break it, improve it — just don’t put it behind a paywall 😎
