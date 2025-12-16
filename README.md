# 🖥️ Kiosk Rotation Engine (MVP)

> **A dead‑simple, self‑hosted rotation engine for view‑only screens**  
> Built for factory floors, TVs, kiosks, and any display where *scrolling and 
> clicking are illegal*.

This project provides a **fire‑and‑forget kiosk server** that automatically 
discovers content from disk and rotates it fullscreen in a browser.

No accounts. No editors. No cloud. No vendor lock‑in.

Just drop content in a folder and let it play.

---

## 🎯 What this is

This is **not** a full digital signage platform.

It is:
- A **local kiosk server**
- With **filesystem‑driven content discovery**
- Designed for **non‑interactive TVs / monitors**
- Optimized for **industrial / factory environments**

The goal is simple:

> **If it’s a webpage, image, or HTML file — it can be shown on a screen.**

---

## 🧠 Design philosophy (KISS, intentionally)

- The **screen is dumb** (just a browser)
- The **rotation logic is simple**
- The **content owns itself**
- Humans should be able to add content **without touching Python**

This avoids:
- Over‑engineering
- Vendor lock‑in
- UI builders nobody likes
- Becoming “the TV admin guy”

---

## 📁 Core concept: the `rotation/` folder

The kiosk automatically scans a folder and turns its contents into 
fullscreen views.

```
rotation/
├── onsite.url
├── production.url
├── safety.html
├── christmas.html
├── announcement.png
├── map.jpg
├── maintenance/
│   └── index.html
```

Anything placed here becomes part of the rotation.

No restart required (depending on scan interval).

---

## 🧩 Supported content types (MVP)

### 🌐 `.url` files → Web dashboards

A text file containing a single URL:

```
http://onsite.local/onsite
```

Rendered as:
- Fullscreen iframe

Perfect for:
- Dash dashboards
- ERP views
- Grafana
- Internal tools

---

### 📄 `.html` files → Static pages

Dropped directly into `rotation/`.

Rendered as:
- Fullscreen iframe

Supports:
- CSS
- JavaScript
- Animations
- Videos

Ideal for:
- Safety notices
- Announcements
- Event info

---

### 🖼 Images (`.png`, `.jpg`, `.webp`) → Posters

Rendered as:
- Fullscreen, centered image

Ideal for:
- Posters
- Floor maps
- Evacuation plans
- One‑off announcements

---

### 📁 Folders with `index.html`

```
rotation/maintenance/index.html
```

Rendered as:
- Fullscreen mini‑site

Allows multi‑file HTML content with assets.

---

## 🔁 Rotation behavior (MVP)

- Content rotates automatically
- Fixed duration per view (configurable)
- Fullscreen only
- No scrolling
- No user input

The kiosk is **view‑only by design**.

---

## 🖥️ Intended usage

- Factory floor TVs
- Production overview screens
- Safety / evacuation displays
- Office status boards
- Any screen that should *just show things*

The kiosk runs via:
- Browser (Chrome / Edge / Firefox)
- Kiosk / fullscreen mode recommended

---

## 🚧 What this MVP does NOT include (by design)

Not included **yet**:
- UI manager
- Authentication
- User roles
- Screen grouping
- Per‑view schedules
- Remote control

These are **explicitly postponed** to keep the MVP clean.

---

## 🛣️ Planned next steps (post‑MVP)

Once the rotation engine is stable:

### 🧑‍💼 Manager UI (NiceGUI 3.0)
- CRUD for rotation content
- Upload / delete files
- Enable / disable views
- Adjust rotation timing

### 📱 Remote control mode
- Use phone/tablet to temporarily take control
- Select a specific view (e.g. team meeting)
- Return to auto‑rotation

### 🚨 Emergency override
- Force evacuation / safety view
- Pause rotation

All of these builds **on top of the MVP**, not inside it.

---

## 🧠 Why this exists

Most digital signage solutions:
- Are cloud‑locked
- Cost per screen
- Don’t integrate cleanly with ERP systems
- Are painful to maintain long‑term

This project exists to provide:
- A local‑first alternative
- With clean system boundaries
- That scales without turning into a platform monster

---

## 🧑‍💻 Author

Built by **Tom Erik Harnes**  
Focused on practical, industrially grounded software that survives 
real environments.

---

## 🏄‍♂️ Final note

This project is intentionally boring.

Boring means:
- Stable
- Predictable
- Easy to explain
- Hard to replace

That’s exactly what you want on a factory wall.
