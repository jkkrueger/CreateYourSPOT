# Skatepark-Planer · Besucherversion

Browser-Anwendung zum Arrangieren eines Skatepark-Layouts aus einer
Rhino-Datei (`.3dm`) — ohne Installation, ohne CAD-Kenntnisse.
Ausführliche Bedienung: `Tutorial_Skatepark_Planer.txt`.

---

## Online-Version

**https://jkkrueger.github.io/skatehalle/**

Läuft direkt im Browser — auch am Handy, ohne Installation und ohne lokalen
Server. Die hinterlegte Skatehalle wird beim Öffnen automatisch geladen.

> Erster Aufruf lädt rund 5 MB (rhino3dm, three.js, die `.3dm`).

---

## Die hinterlegte Halle (Auto-Load)

Beim Start lädt die App automatisch die Datei, die in `samples/index.json` mit
`"default": true` markiert ist.


## Starten

### Variante A — Doppelklick (schnell, braucht Internet)

`index.html` doppelklicken.

Der Browser öffnet die Seite über `file://`. Three.js und der GLTF-Exporter
werden dabei lokal aus `vendor/` geladen, **rhino3dm jedoch aus dem Internet**.

### Variante B — lokaler Server (empfohlen, komplett offline)

Alle Bibliotheken kommen dann aus `vendor/` — es wird **keine
Internetverbindung** benötigt. Drei Wege, alle gleichwertig:

**B1 — von Hand (am zuverlässigsten)**

Im Explorer in diesen Ordner wechseln, in die Adresszeile `powershell` tippen
und Enter drücken. Dann:

```powershell
python -m http.server 8000
```

Anschließend im Browser `http://localhost:8000` öffnen.
Beenden mit `Strg+C` oder Fenster schließen.

**B2 — PowerShell-Skript**

Rechtsklick auf `Start_Offline.ps1` → **„Mit PowerShell ausführen"**.
Sucht Python automatisch, weicht bei belegtem Port aus und öffnet den Browser
selbst. Blockiert Windows die Ausführung von Skripten, stattdessen in
PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\Start_Offline.ps1
```


> Voraussetzung für erfolgreichen Start: Python ist installiert
> (`python --version` in PowerShell prüfen).
> Alternativ tut es jeder andere lokale Webserver, z. B. die VS-Code-Erweiterung
> „Live Server".

---

## ⚠️ Wichtig: `.3dm` mit Render-Meshes speichern

Die App zeigt eine `.3dm` nur, wenn deren Objekte **Netze (Meshes)** enthalten.

**So geht der Kreislauf sauber auf:** nach dem zeichnen in Rhino einmal in eine
**gerenderte / schattierte Ansicht** wechseln (das erzeugt die Render-Meshes)
und die **`.3dm` speichern**. Erst dann fließt das Ergebnis aus der Pipeline
wieder verlustfrei in die Besucher-App zurück.


## Zwei Modi: Betreiber und Besucher

Die App kennt zwei Rollen und schaltet zwischen ihnen um — **eine** `index.html`
für beides.

**Betreibermodus** (Start) — die volle Werkzeugpalette. Hier wird die Halle
vorbereitet: `.3dm` laden, Layer ordnen, messen, und vor allem **pinnen**.

> 📌 **Der Pin ist der Schalter.** Gepinnt = *fest verbaut*, ungepinnt =
> *beweglich*. Alles Ungepinnte ist genau das, womit der Besucher spielen darf.
>
> **Voreinstellung: alles gepinnt.** Beim Laden einer `.3dm` gilt zunächst die
> gesamte Halle als fest. Der Betreiber gibt gezielt frei, was beweglich sein
> soll, indem er in der Szene-Liste den 📌 der jeweiligen Rampen (oder eines
> ganzen Layers) löst. Das ist die sichere Richtung — sonst wäre versehentlich
> die komplette Halle verschiebbar.

**Besuchermodus** — über `👥 Besucher` unten in der Icon-Leiste. Beim Wechsel
passiert dreierlei:

1. Der **Katalog** wird automatisch aus den beweglichen Rampen gebaut.
2. Alles Feste wird **einheitlich grau**.
3. Jede Kategorie bekommt eine **eigene Signalfarbe**, die einzelnen Rampen
   darin abgestufte Helligkeiten davon.

Der Besucher hat dann nur noch: **Katalog** (Bestandsliste der Halle),
**Verschieben / Drehen / Entfernen** der farbigen Rampen und den **JSON-Export**.
Feste Elemente lassen sich weder bewegen noch löschen. Über `← Betreibermodus`
geht es zurück; die Layerfarben kehren dabei zurück.

> **Der Besucher legt keine neuen Rampen an.** Er arbeitet ausschließlich mit
> dem vorhandenen Bestand der Halle.

**Kategorie per Drag & Drop ändern:** Eine Karte auf einen Typ-Chip ziehen
ordnet die Rampe dieser Kategorie zu und übernimmt deren Farbe. Diese
Zuweisung schlägt die automatische Einordnung dauerhaft.


### Bedienhilfen

- **Drawer-Breite:** Menü- und Katalog-Fenster haben am rechten Rand einen
  Anfasser — mit gedrückter Maustaste horizontal ziehen. Die Breite wird pro
  Browser gemerkt, Doppelklick auf den Anfasser setzt sie zurück. Das
  Katalog-Raster passt die Spaltenzahl automatisch an.
- **Rampen finden:** Ein Klick auf das Bild einer Katalogkarte lässt **alle
  Exemplare dieses Typs** in den Ansichten weiß aufleuchten (pulsierend) und
  wählt das erste davon aus — der Gumball (Pfeile + Drehring) steht also sofort
  am Objekt. Nochmal klicken hebt die Markierung auf.
- **Verdeckte Körper auswählen** (beide Modi): Bleibt die Maus eine Sekunde auf
  einer Rampe stehen, erscheint das Info-Fenster. Liegen dort mehrere Körper
  übereinander, zeigt es „Körper 1 von 3“ — mit **Tab** schaltet man durch sie
  hindurch (Shift+Tab rückwärts), der gerade gemeinte leuchtet cyan. Ein Klick
  übernimmt genau diesen, nicht den vordersten.


### Meine Layer (Besuchermodus)

Über *☰ Menü → Meine Layer* legt der Besucher eigene Gruppen an: Name eingeben,
**+**, dann eine Rampe auswählen und den Layer antippen. Erneutes Antippen nimmt
sie wieder heraus, das ✕ löscht den Layer (die Rampen bleiben erhalten). Jede
Rampe gehört zu höchstens einem Besucher-Layer; die Rhino-Layer bleiben davon
unberührt, damit Kategorie und Einfärbung erhalten bleiben.

### Export nach Layern

Beim **JSON-Export** fragt die App, welche Gruppen mitsollen — jede mit
Objektzahl zum Anhaken, dazu ein „Alle / keine"-Schalter. Jede Rampe gehört zu
**genau einer** Gruppe, damit die Auswahl eindeutig bleibt:

1. der selbst angelegte Besucher-Layer, falls gesetzt
2. sonst die Katalog-Kategorie (`QTRS`, `BNKS` … — per Drag & Drop änderbar)
3. sonst der Layer aus der Rhino-Datei (das betrifft die festen Elemente)

Im JSON steht der Besucher-Layer je Element zusätzlich unter `visitorLayer`.

### Farbgebung

| Was | Farbe |
|---|---|
| Fest verbaut | einheitlich grau |
| Rampentyp | eine Grundfarbe je Typ |
| Einzelne Rampe eines Typs | gestaffelte Helligkeit derselben Grundfarbe |
| Ausgewählt | kräftiges **Magenta** — bewusst außerhalb der Rampen-Palette |
| Unter dem Cursor (Tab-Durchschaltung) | **Cyan** |
| Im Katalog markiert | weiß pulsierend |

---

## Ordnerinhalt

| Datei / Ordner | Bedeutung |
|---|---|
| `index.html` | Die komplette Anwendung (Oberfläche, 3D-Ansicht, Import/Export) |
| `vendor/` | Bibliotheken: three.js, rhino3dm (+ `.wasm`), GLTFExporter — **nicht löschen** |
| `.nojekyll` | Schaltet die Jekyll-Verarbeitung von GitHub Pages ab — **nicht löschen** |
| `Start_Offline.ps1` / `.bat` | Startet den lokalen Server und öffnet den Browser |
| `Tutorial_Skatepark_Planer.txt` | Anwender-Tutorial |
| `skatepark_import_mesh.py` | GhPython-Node: exakte Geometrie aus dem JSON nach Rhino |
| `skatepark_split_layers.py` | GhPython-Node: Breps nach Layern in einen DataTree aufteilen |
| `jsonImport_Besucherversion.gh` | Grasshopper-Definition für den JSON-Import |
| `json/`, `ghOutput/` | Beispiel-/Austauschdateien |
| `samples/` | Hinterlegte `.3dm`-Dateien + `index.json`. Der Eintrag mit `"default": true` wird beim Start automatisch geladen (siehe oben). |

Die Anwendung ist als Ganzes weiterzugeben: **immer den kompletten Ordner
kopieren**, die `index.html` allein funktioniert nicht.

---

## Bekannte Meldungen

| Meldung | Ursache / Lösung |
|---|---|
| „Three.js nicht geladen“ | `vendor/` fehlt oder ist unvollständig. Kompletten Ordner verwenden. |
| „rhino3dm nicht initialisiert“ | Per Doppelklick geöffnet **und** keine Internetverbindung → über einen lokalen Server starten (siehe Variante B). |
| „⚠ n Flächen ohne Render-Mesh“ | Die `.3dm` enthält Flächen ohne gespeichertes Mesh. Die App rekonstruiert sie automatisch; sauberste Lösung: Datei in Rhino **schattiert/gerendert anzeigen und neu speichern** (siehe Abschnitt oben). |
| Objekte zu groß / zu klein | Im Panel *Datei* die Einheit umstellen (Automatisch, mm, cm, m oder Zoll). |

---

## Export-Formate

| Format | Ziel | Hinweis |
|---|---|---|
| **JSON** | Grasshopper | Parametrische Daten **und** exakte Geometrie. Import über `skatepark_import_v2.py` (parametrisch) oder `skatepark_import_mesh.py` (Meshes). |
| **GLB** | Blender | Datei → Importieren → glTF 2.0. Layer werden zu Collections, Maßstab in Metern. |
| **.3dm** | Rhino | Direkt zu öffnen; Layer, Farben und Lage bleiben erhalten. |

Es werden immer nur **sichtbare** Objekte exportiert.
