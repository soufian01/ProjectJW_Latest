// Theme: dark mode with purple accent
(function(){
  const root = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const applyTheme = (t) => {
    if(t === 'dark') {
      root.classList.add('dark');
      localStorage.setItem('theme','dark');
    } else {
      root.classList.remove('dark');
      localStorage.setItem('theme','light');
    }
  };
  const saved = localStorage.getItem('theme') || 'dark';
  applyTheme(saved);
  themeToggle.addEventListener('click', ()=> applyTheme(document.documentElement.classList.contains('dark') ? 'light' : 'dark'));
})();

const videoListEl = document.getElementById('videoList');

async function loadVideos() {
  try {
    const res = await fetch('/api/videos');
    if (!res.ok) throw new Error('Network response was not ok');
    const data = await res.json();
    if (!Array.isArray(data) || data.length === 0) {
      videoListEl.innerHTML = '<p class="text-gray-500">No videos yet.</p>'; return;
    }
    videoListEl.innerHTML = '';
    data.forEach(v => {
      // Create a container for each video with title + player
      // give each container a fixed responsive width so multiple players center evenly
      const container = document.createElement('div');
      container.className = 'w-72 md:w-80 lg:w-96 flex flex-col items-center gap-2 video-card';
      
      const title = document.createElement('p');
      title.className = 'font-medium text-sm text-center';
      title.textContent = v.title || 'Untitled';
      
      const videoEl = document.createElement('video');
      videoEl.src = v.url;
      videoEl.controls = true;
      // make the video fill the container width but keep its aspect ratio and avoid cropping
      videoEl.className = 'rounded-lg w-full';
      videoEl.style.maxHeight = '500px';
      videoEl.style.objectFit = 'contain';
      videoEl.style.width = '100%';
      videoEl.style.height = 'auto';
      // prevent the player from being upscaled beyond its native resolution
      videoEl.addEventListener('loadedmetadata', () => {
        try {
          if (videoEl.videoWidth) {
            // set max-width to the video's natural width (px) so larger containers won't upscale it
            videoEl.style.maxWidth = videoEl.videoWidth + 'px';
          }
        } catch (e) {
          // ignore errors and allow default sizing
          console.warn('Could not set natural maxWidth for video', e);
        }
      });
      
      container.appendChild(title);
      container.appendChild(videoEl);
      videoListEl.appendChild(container);
    });
  } catch (err) {
    console.error(err);
    videoListEl.textContent = 'Failed to load videos.';
  }
}

document.getElementById('contactForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = e.target;
  const fd = new FormData(form);
  const body = { name: fd.get('name'), email: fd.get('email'), message: fd.get('message') };
  const out = document.getElementById('contactStatus');
  const submitBtn = form.querySelector('button[type="submit"]');
  submitBtn.disabled = true;
  try {
    const res = await fetch('/api/contact', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body) });
    if (res.ok) {
      out.textContent = 'Thanks! I will get back to you shortly.'; out.className = 'text-sm mt-2 text-green-600'; form.reset();
    } else {
      const err = await res.json().catch(()=>({})); out.textContent = 'Error: ' + (err.error || 'could not send'); out.className = 'text-sm mt-2 text-red-600';
    }
  } catch (err) { console.error(err); out.textContent = 'Network error'; out.className = 'text-sm mt-2 text-red-600'; }
  finally { submitBtn.disabled = false; }
});

async function showLocation() {
  const btn = document.getElementById('showLocationBtn');
  const container = document.getElementById('mapContainer');
  btn.disabled = true;
  container.innerHTML = 'Loading...';
  try {
    container.innerHTML = `<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d80429.06496168647!2d6.78540945053099!3d50.953155244112985!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47bf2572d0d7e601%3A0xac339addcd4e3c68!2sXTRAFIT%20K%C3%B6ln-Ehrenfeld!5e0!3m2!1sen!2sde!4v1761516792559!5m2!1sen!2sde" width="100%" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>`;
  } catch (err) {
    container.textContent = 'Unable to load location.';
    console.error(err);
  } finally {
    btn.disabled = false;
  }
}

document.getElementById('showLocationBtn').addEventListener('click', showLocation);

loadVideos();
