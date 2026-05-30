const express = require('express');
const path = require('path');
const { ConnectToDatabase, db } = require('./database.cjs');

const app = express();
app.use(express.json());
app.use(express.static('public'));

ConnectToDatabase();

app.post('/api/shorten', (req, res) => {
  const { url } = req.body;

  if (!url) {
    return res.status(400).json({ error: "Hiányzó URL" });
  }

  const shortCode = Math.random().toString(36).slice(2, 8);

  db.run(
    "INSERT INTO urls (short_code, original_url) VALUES (?, ?)",
    [shortCode, url],
    (err) => {
      if (err) {
        console.error("DB hiba:", err);
        return res.status(500).json({ error: "Hiba az adatbázis írásakor" });
      }
      res.json({ shortUrl: `http://localhost:3000/${shortCode}` });
    }
  );
});

app.get('/:code', (req, res) => {
  const { code } = req.params;

  db.get(
    "SELECT original_url FROM urls WHERE short_code = ?",
    [code],
    (err, row) => {
      if (err || !row) {
        return res.status(404).send("Link nem található");
      }
      res.redirect(row.original_url);
    }
  );
});

app.listen(3000, () => console.log('Szerver fut a http://localhost:3000 címen'));