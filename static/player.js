document.addEventListener("DOMContentLoaded", () => {
  let playlist = [];
  let index = 0;

  const img = document.getElementById("image");
  const frame = document.getElementById("frame");
  const video = document.getElementById("video");

  async function loadPlaylist() {
    const res = await fetch("/playlist");
    playlist = await res.json();
    console.log("Playlist:", playlist);
  }

  function hideAll() {
    img.style.display = "none";
    frame.style.display = "none";
    video.style.display = "none";

    img.src = "";
    frame.src = "";
    video.pause();
    video.src = "";
  }

  function next() {
    index = (index + 1) % playlist.length;
    showNext();
  }

  function showNext() {
    if (playlist.length === 0) return;

    const item = playlist[index];
    hideAll();

    if (item.kind === "image") {
      img.src = item.src;
      img.style.display = "block";

      setTimeout(next, item.duration * 1000);
    }

    if (item.kind === "iframe") {
      frame.src = item.src;
      frame.style.display = "block";

      setTimeout(next, item.duration * 1000);
    }

    if (item.kind === "video") {
      video.src = item.src;
      video.muted = item.meta?.muted ?? true;
      video.autoplay = true;
      video.onended = next;

      video.style.display = "block";
      video.play();
    }
  }

  loadPlaylist().then(showNext);
});
