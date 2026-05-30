document.addEventListener('DOMContentLoaded', () => {

  document.getElementById('btn-qr').addEventListener('click', () => {
    const inputUrl = document.getElementById('url-input').value.trim();

    if (!inputUrl) {
      alert("Kérlek, írj be egy URL-t!");
      return;
    }

    const qrImg = document.getElementById('qr-img');
    const placeholder = document.getElementById('qr-placeholder');

    qrImg.style.display = 'none';
    placeholder.style.display = 'block';

    qrImg.onload = () => {
      qrImg.style.display = 'block';
      placeholder.style.display = 'none';
    };
    qrImg.onerror = () => {
      alert("Nem sikerült a QR kódot legenerálni.");
    };

    qrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=${encodeURIComponent(inputUrl)}`;
    document.getElementById('result-qr').classList.add('visible');
  });


  document.getElementById('btn-shorten').addEventListener('click', async () => {
    const inputUrl = document.getElementById('url-input').value.trim();

    if (!inputUrl) {
      alert("Kérlek, írj be egy URL-t!");
      return;
    }

    const btn = document.getElementById('btn-shorten');
    btn.disabled = true;
    btn.textContent = 'Rövidítés...';

    try {
      const response = await fetch('/api/shorten', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: inputUrl })
      });

      const data = await response.json();

      if (!response.ok) {
        alert(data.error || "Hiba történt.");
        return;
      }

      const anchor = document.getElementById('result-link-anchor');
      anchor.href = data.shortUrl;
      anchor.textContent = data.shortUrl;

      document.getElementById('result-short').classList.add('visible');

    } catch (err) {
      alert("Nem sikerült kapcsolódni a szerverhez.");
      console.error(err);
    } finally {
      btn.disabled = false;
      btn.innerHTML = '<span class="btn-icon">⚡</span> Rövidítés';
    }
  });

  document.getElementById('copy-btn').addEventListener('click', () => {
    const url = document.getElementById('result-link-anchor').textContent;
    navigator.clipboard.writeText(url).then(() => {
      const btn = document.getElementById('copy-btn');
      btn.textContent = 'Másolva!';
      setTimeout(() => btn.textContent = 'Másolás', 1800);
    });
  });

});
