# Techinf Zeitverwaltung

---

## Grundidee

Unsere Idee war es, ein kleines und kompaktes System zu entwickeln, um die Arbeitszeit in Coworking-Spaces oder im Homeoffice zu erfassen.

## Getting Started

### Firmware

Es werden folgende Pakete im Projekt verwendet, die im Nachhinein installiert werden müssen:

- MFRC522
- ArduinoJson

Es müssen ein Verzeichnis namens `.env` erstellt werden. Danach müssen zwei Dateien erstellt werden.

**api.h**

```h
#define API_ADDRESS "Server Adresse"
#define API_KEY "API Passwort"
```

**credentials.h**

```h
#define SSID "SSID"
#define PASSWORD "Passwort"
```

Danach kann `firmware.ino` auf dem ESP 8266 geflasht werden.

### Server

Es gibt zwei Möglichkeiten den Server laufen zulassen. Einmal per Terminal oder via einen Docker Container.

#### Nutzung via Terminal (MacOS/Linux)

**1**: In den Server Ordner wechseln

```bash
cd ./server
```

**2**: Alle Module installieren die gebraucht werden

```bash
pip install -r requirements.txt
```

**3**: Die Datenbank initialisieren

```bash
python main.py -i
```

(**4**: Die Demo Daten hinzufügen)

```bash
python main.py -add
```

**5**: Server starten

```bash
python main.py -a 0.0.0.0 -p [port]
```

#### Nutzung via Docker (MacOS/Linux)

**1**: In den Server Ordner wechseln

```bash
cd ./server
```

**2**: Docker image erstellen

```bash
docker build -t [image_name] .
```

**3**: Image ID kopieren

```bash
docker images
```

**4**: Docker Container via ID starten

```bash
 docker run -d -p 80:80 --name [container_name] [image_id]
```
