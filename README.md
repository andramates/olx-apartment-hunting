# OLX Apartment Hunting

Aplicație backend pentru monitorizarea anunțurilor OLX pe baza unor filtre salvate și trimiterea de notificări email când apar anunțuri noi.

## Ce face aplicația

Aplicația permite:
- creare utilizatori
- creare filtre OLX per utilizator
- rulare manuală a unui filtru
- extragerea anunțurilor din OLX
- detectarea anunțurilor noi
- salvarea anunțurilor și a match-urilor în PostgreSQL
- generarea notificărilor
- trimiterea notificărilor pe email
- gruparea mai multor notificări ale aceluiași user într-un singur email

## Stack tehnologic

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Playwright
- SMTP pentru email

## Arhitectură

Proiectul folosește o arhitectură stratificată:

- `presentation` pentru API și request/response schemas
- `application` pentru services și ports
- `domain` pentru entități
- `infrastructure` pentru DB, scraping, email și config

## Structura proiectului

```text
src/
  main.py
  presentation/
    api/
      dependencies.py
      routers/
      schemas/
  application/
    services/
    ports/
  domain/
    entities/
  infrastructure/
    config/
    db/
      models/
      repositories/
    scraping/
    notifications/
migrations/
```

## Funcționalități implementate
### Users
- creare user
- listare useri
- afișare user după id
### Filters
- creare filtru OLX
- listare filtre pentru un user
- activare filtru
- dezactivare filtru
- rulare manuală a unui filtru
### Listings
- scraping OLX folosind Playwright
- salvare anunțuri noi în baza de date
- legare între filtre și anunțuri prin filter_matches
### Notifications
- creare notificări pending pentru anunțurile noi
- trimitere notificări pe email
- grupare notificări per user într-un singur email
- marcarea notificărilor ca sent sau failed
## Baza de date

### Tabele principale:

- users
- search_filters
- listings
- filter_matches
- notifications
alembic_version

### Relații
- un user poate avea mai multe filtre
- un filtru poate match-ui mai multe anunțuri
- un anunț poate fi asociat mai multor filtre
- notificările sunt generate pentru user + filtru + listing

## Instalare
### 1. Clonează proiectul
``` 
git clone <repo-url>
cd olx-apartment-hunting
```
### 2. Creează și activează virtualenv
```
python3.12 -m venv .venv
source .venv/bin/activate
```
### 3. Instalează dependențele
```
pip install fastapi uvicorn sqlalchemy "psycopg[binary]" alembic pydantic-settings python-dotenv playwright apscheduler requests beautifulsoup4 email-validator
playwright install
```
### 4. Creează baza de date PostgreSQL

Exemplu:
```sql
CREATE DATABASE olx_apartment_hunting;
```
### 5. Configurează variabilele de mediu

Creează un fișier .env în root-ul proiectului:
```
APP_NAME=OLX Apartment Hunting
APP_ENV=dev
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/olx_apartment_hunting

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM=your_email@gmail.com
```
### 6. Rulează migrațiile
```
alembic upgrade head
```
## Rulare aplicație
```
uvicorn src.main:app --reload
```

Documentația Swagger va fi disponibilă la:
```
http://127.0.0.1:8000/docs
```

### Endpoint-uri principale
#### Health
```
GET /health
```
#### Users
```
POST /users
GET /users
GET /users/{user_id}
```
#### Filters
```
POST /filters
PATCH /filters/{filter_id}/activate
PATCH /filters/{filter_id}/deactivate
POST /filters/{filter_id}/run
GET /users/{user_id}/filters
```
#### Notifications
```
POST /notifications/dispatch
```
### Exemplu de flow
#### 1. Creezi un user
```json
{
  "name": "Andra",
  "email": "andra@example.com"
}
```
#### 2. Creezi un filtru OLX (pune URL-ul de pe OLX)
```json
{
  "user_id": 1,
  "name": "2 camere Cluj",
  "olx_url": "https://www.olx.ro/...", 
  "check_interval_minutes": 5
}
```
#### 3. Rulezi filtrul
```
POST /filters/{filter_id}/run
```
Aplicația:

- deschide pagina OLX
- extrage anunțurile
- salvează anunțurile noi
- creează filter_matches
- creează notificări pending
#### 4. Trimiți notificările
```
POST /notifications/dispatch
```
Aplicația:

- grupează notificările pending per user
- construiește un singur email pentru fiecare user
- trimite emailul
- marchează notificările ca sent

### Cum funcționează deduplicarea

Deduplicarea se face pe două niveluri:

#### 1. În listings

external_id este unic, deci același anunț nu este salvat de două ori global.

#### 2. În filter_matches

perechea (filter_id, listing_id) este unică, deci același anunț nu este notificat de două ori pentru același filtru.

## Email notifications

Aplicația folosește SMTP pentru trimiterea emailurilor.

Pentru Gmail:

- trebuie activată 2-Step Verification
- trebuie generat un App Password
- App Password-ul se pune în .env la SMTP_PASSWORD

Notificările sunt grupate per user, astfel încât dacă există mai multe anunțuri noi, userul primește un singur email.

## Probleme întâlnite
### SMTPAuthenticationError 535

Înseamnă că Gmail nu acceptă autentificarea.

Verifică:

- SMTP_USER corect
- SMTP_FROM corect
- SMTP_PASSWORD să fie App Password, nu parola normală
- restart al aplicației după schimbarea .env

#### Alembic nu vede configul

Asigură-te că:

- alembic.ini este valid
- migrations/env.py importă Base
- target_metadata = Base.metadata
- .env a ajuns în Git

#### Asigură-te că ai în .gitignore:

.env, 
.venv/,
__pycache__/,
*.pyc,
.idea/

## Îmbunătățiri posibile:

- job periodic cu APScheduler
- retry pentru notificări failed
- endpoint-uri de update/delete pentru filtre
- autentificare și autorizare
- UI web
- parsare mai bună a prețului și locației
- 
## Status proiect

Acesta este un MVP funcțional care demonstrează fluxul complet:

- user
- filtru
- scraping
- detectare anunțuri noi
- generare notificări
- trimitere email (gmail)