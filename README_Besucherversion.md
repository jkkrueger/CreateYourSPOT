# Skatepark-Planer · Besucherversion

Browser-Anwendung zum Arrangieren eines Skatepark-Layouts aus einer
Rhino-Datei (`.3dm`) — ohne Installation, ohne CAD-Kenntnisse.
Ausführliche Bedienung: `Tutorial_Skatepark_Planer.txt`.

---

## Online-Version

**https://jkkrueger.github.io/skatehalle/**

Läuft direkt im Browser — auch am Handy, ohne Installation und ohne lokalen
Server. Die hinterlegte Skatehalle wird beim Öffnen automatisch geladen.

> Erster Aufruf lädt rund 5 MB (rhino3dm, three.js, die `.3dm`). Im WLAN
> unkritisch, über Mobilfunk kurz spürbar.

---

## Die hinterlegte Halle (Auto-Load)

Beim Start lädt die App automatisch die Datei, die in `samples/index.json` mit
`"default": true` markiert ist — in Betreiber- **und** Besuchermodus. Niemand
muss also erst eine Datei auswählen.

**Eine andere Halle hinterlegen:**

1. Die `.3dm` nach `samples/` kopieren (mit Render-Meshes, siehe Abschnitt unten).
2. In `samples/index.json` eintragen und `"default": true` dorthin verschieben:

```json
[
  { "file": "meineHalle.3dm", "name": "Halle 2026", "default": true },
  { "file": "spotSkatehalle_IST.3dm", "name": "Skatehalle – IST-Zustand" }
]
```

Alle Einträge erscheinen zusätzlich im Panel *📁 Datei* unter **Hinterlegte
Dateien** und lassen sich dort per Klick umschalten. Ohne `"default"` wird der
erste Eintrag geladen.

> Auto-Load braucht HTTP(S) — per Doppelklick (`file://`) blockiert der Browser
> das Nachladen. Dann über die Online-Version oder einen lokalen Server starten.

---

## Starten

### Variante A — Doppelklick (schnell, braucht Internet)

`index.html` doppelklicken.

Der Browser öffnet die Seite über `file://`. Three.js und der GLTF-Exporter
werden dabei lokal aus `vendor/` geladen, **rhino3dm jedoch aus dem Internet**.
Grund: rhino3dm besteht aus einer WebAssembly-Datei (`rhino3dm.wasm`), die per
`fetch()` nachgeladen wird — und das ist auf `file://`-Seiten aus
Sicherheitsgründen von jedem Browser blockiert.

→ Ohne Internetverbindung funktioniert in dieser Variante der **.3dm-Import
nicht**. Die Statuszeile weist beim Start darauf hin.

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

**B3 — Batch-Datei**

Doppelklick auf `Start_Offline.bat` (einfachste Variante, funktioniert aber
nicht auf allen Systemen zuverlässig).

> Voraussetzung für alle drei Wege: Python ist installiert
> (`python --version` in PowerShell prüfen).
> Alternativ tut es jeder andere lokale Webserver, z. B. die VS-Code-Erweiterung
> „Live Server".

---

## ⚠️ Wichtig: `.3dm` mit Render-Meshes speichern

Die App zeigt eine `.3dm` nur, wenn deren Objekte **Netze (Meshes)** enthalten.
Frisch in Grasshopper gebakte Geometrie hat oft noch keine — dann erscheinen
die Rampen beim Laden **leer bzw. unsichtbar** (die App meldet
„⚠ n Flächen ohne Render-Mesh" und rekonstruiert sie nur notdürftig).

**So geht der Kreislauf sauber auf:** nach dem Baken in Rhino einmal in eine
**gerenderte / schattierte Ansicht** wechseln (das erzeugt die Render-Meshes)
und die **`.3dm` speichern**. Erst dann fließt das Ergebnis aus der Pipeline
wieder verlustfrei in die Besucher-App zurück.

> **Kreislauf:** Grasshopper (Import → Build → Bake) → Rhino →
> **gerenderte Ansicht + `.3dm` speichern** → Besucher-App lädt die `.3dm`.

---

## Zwei Modi: Betreiber und Besucher

Die App kennt zwei Rollen und schaltet zwischen ihnen um — **eine** `index.html`
für beides.

**Betreibermodus** (Start) — die volle Werkzeugpalette. Hier wird die Halle
vorbereitet: `.3dm` laden, Layer ordnen, messen, und vor allem **pinnen**.

> 📌 **Der Pin ist der Schalter.** Alles, was der Betreiber pinnt (Objekt-Pin in
> der Szene-Liste oder Layer-Pin für einen ganzen Layer), gilt als *fest
> verbaut*. Alles Ungepinnte gilt als *beweglich* — das ist genau das, womit
> der Besucher später spielen darf.

**Besuchermodus** — über `👥 Besucher` unten in der Icon-Leiste. Beim Wechsel
passiert dreierlei:

1. Der **Katalog** wird automatisch aus den beweglichen Rampen gebaut.
   Baugleiche Rampen (gleiche Maße, gleiches Netz) werden zu **einem** Eintrag
   zusammengefasst — fünf identische Quarterpipes ergeben eine Katalogkarte
   mit dem Vermerk „5× in der Halle“.
2. Alles Feste wird **einheitlich grau**.
3. Jeder bewegliche Rampen*typ* bekommt eine **eigene Signalfarbe**; Kopien
   erben die Farbe ihrer Vorlage.

Der Besucher hat dann nur noch: **Katalog** (Rampen nachlegen per Klick in die
Fläche), **Verschieben / Drehen / Entfernen** der farbigen Rampen und den
**JSON-Export**. Feste Elemente lassen sich weder bewegen noch löschen. Über
`← Betreibermodus` geht es zurück; die Layerfarben kehren dabei zurück.

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
