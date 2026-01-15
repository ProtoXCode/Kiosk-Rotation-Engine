document.addEventListener("DOMContentLoaded", () => {
  let playlist = [];
  let playlistVersion = null;
  let index = 0;

  // Token used to invalidate old timers/callbacks
  let advanceToken = 0;

  const img = document.getElementById("image");
  const frame = document.getElementById("frame");
  const video = document.getElementById("video");

  /* ---------------- playlist ---------------- */

  async function loadPlaylist() {
    const res = await fetch("/playlist");
    const data = await res.json();

    if (!data.items || data.items.length === 0) {
      console.warn("Playlist empty");
      playlist = [];
      return;
    }

    if (playlistVersion !== data.version) {
      playlist = data.items;
      playlistVersion = data.version;
      index = 0;
    }
  }

  /* ---------------- helpers ---------------- */

  function hideAll() {
    img.style.display = "none";
    frame.style.display = "none";
    video.style.display = "none";

    img.src = "";

    video.pause();
    video.removeAttribute("src");
    video.load();

    video.onended = null;
    video.onerror = null;
  }

  function advance(expectedToken) {
    if (expectedToken !== advanceToken) return;

    index++;

    // At wrap-around, refresh playlist once
    if (index >= playlist.length) {
      loadPlaylist().then(() => {
        index = 0;
        showNext();
      });
      return;
    }

    showNext();
  }

  /* ---------------- core player ---------------- */

  function showNext() {
    if (playlist.length === 0) return;

    advanceToken++;
    const token = advanceToken;

    const item = playlist[index];
    hideAll();

    /* IMAGE */
    if (item.kind === "image") {
      img.style.display = "block";
      img.onerror = () => advance(token);

      img.src = item.src;

      setTimeout(() => advance(token), item.duration * 1000);
      return;
    }

    /* IFRAME (HTML + PDF) */
    if (item.kind === "iframe") {
      frame.style.display = "block";

      // Clear old handlers so they don't stack
      frame.onload = null;
      frame.onerror = null;

      frame.onerror = () => advance(token);

      frame.onload = () => {
        // Start timing ONLY after iframe actually loads
        setTimeout(() => advance(token), item.duration * 1000);
      };

      // Set src last (after handlers) so we don't miss events
      frame.src = item.src;
      return;
    }

    /* VIDEO */
    if (item.kind === "video") {
      video.style.display = "block";
      video.muted = item.meta?.muted ?? true;

      video.onended = () => advance(token);
      video.onerror = () => advance(token);

      video.src = item.src;
      video.play().catch(() => advance(token));
      return;
    }

    // Unknown type → skip safely
    advance(token);
  }

  /* ---------------- BOOTSTRAP ---------------- */

  loadPlaylist().then(() => {
    if (playlist.length > 0) showNext();
  });
});
