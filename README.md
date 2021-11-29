# Požiadavky
- Python3, NodeJS 16, PostgreSQL

# Databáza
Tabuľky sa inicializujú do špecifikovanej databázy automaticky pri prvom spustení backendu.\
V prípade potreby je možné použiť súbor **dump.sql** ktorý obsahuje tabuľky a testovacie dáta z live serveru. Importovať ho do postgresql databázy je možné pomocou:
```
psql database_name < dump.sql
```
prípadne manuálne tento SQL script zavolať vrámci databázy

# Spustenie - Backend
Vytvorenie virtuálneho prostredia
```
cd backend
python3 -m venv venv
```
Inštalácia balíčkov
```
source venv/bin/activate
pip install -r requirements.txt
```
Nastavenie konfiguračných premenných
```py
#backend/config.py
DATABASE_URI = "postgresql://username:password@host:port/db"
SECRET_KEY = "changethis"
```
Nastavenie HTTPS
```py
#backend/run_app.py
from app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(host = "localhost", debug = False, port = 8000, ssl_context=(
        '/cesta/ku/certifikat.pem', 
        '/cesta/ku/certifikat-key.pem'
    ))
```
Spustenie
```
source venv/bin/activate
python run_app.py
```

# Spustenie - Frontend
Inštalácia balíčkov
```
cd frontend
npm install
```
Nastavenie HTTPS
```js
//frontend/nuxt.config.js
import fs from "fs"
import path from "path"

export default {
    server: {
        https: {
            key: fs.readFileSync("/cesta/ku/certifikat-key.pem"),
            cert: fs.readFileSync("/cesta/ku/certifikat.pem")
        },
    },
    ...
    ...
}
```
Preklad a spustenie
```
npm run build
npm run start
```