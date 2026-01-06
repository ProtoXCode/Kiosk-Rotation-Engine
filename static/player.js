let playlist = [];
let index = 0;

async function loadPlaylist() {
  const res = await fetch("/playlist");
  playlist = await res.json();
}

function showNext() {
  if (playlist.length === 0) return;

  const item = playlist[index];
  const img = document.getElementById("image");

  img.src = item.src;

  setTimeout(() => {
    index = (index + 1) % playlist.length;
    showNext();
  }, item.duration * 1000);
}

loadPlaylist().then(showNext);
