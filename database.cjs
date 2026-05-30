const sqlite3 = require('sqlite3').verbose();

const db = new sqlite3.Database('./shorturls.db');

function ConnectToDatabase() {
  db.serialize(() => {
    db.run(
      "CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY AUTOINCREMENT, short_code TEXT UNIQUE, original_url TEXT)",
      (err) => {
        if (err) console.error("Tábla létrehozási hiba:", err);
        else console.log("Adatbázis csatlakoztatva és tábla ellenőrizve.");
      }
    );
  });
}

module.exports = { ConnectToDatabase, db };