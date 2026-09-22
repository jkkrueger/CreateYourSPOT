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

1. Der **Katalog** wird automatisch aus den beweglichen Rampen gebaut — eine
   Karte je Rampe, eingeordnet nach Ähnlichkeit zu den gepinnten Objekten
   (siehe *Kategorien* weiter unten).
2. Alles Feste wird **einheitlich grau**.
3. Jede Kategorie bekommt eine **eigene Signalfarbe**, die einzelnen Rampen
   darin abgestufte Helligkeiten davon.

Der Besucher hat dann nur noch: **Katalog** (Bestandsliste der Halle),
**Verschieben / Drehen / Entfernen** der farbigen Rampen und den **JSON-Export**.
Feste Elemente lassen sich weder bewegen noch löschen. Über `← Betreibermodus`
geht es zurück; die Layerfarben kehren dabei zurück.

> **Der Besucher legt keine neuen Rampen an.** Er arbeitet ausschließlich mit
> dem vorhandenen Bestand der Halle — das Stempeln von Kopien gibt es nur im
> Betreibermodus (Panel *📚 Katalog*).

### Der Katalog als Bestandsliste

Der Katalog führt **jede einzelne bewegliche Rampe** der Halle mit einer eigenen
Karte — nicht nur einen Vertreter je Typ. Benannt wird nach Kategorie plus
laufendem Index, also `QTRS 1`, `QTRS 2`, `BNKS 1` … Damit ist jedes Stück
einzeln ansprechbar. Ein Klick auf die Karte markiert genau diese Rampe in der
Halle und wählt sie aus (der Gumball steht sofort daran).

Entfernt der Besucher eine Rampe, wandert sie in den Papierkorb, bleibt aber
Teil des Bestands: **ihre Karte bleibt stehen** und lässt sich zurücklegen.

| Element der Karte | Bedeutung |
|---|---|
| „in der Halle" | steht gerade im Entwurf |
| „herausgenommen" / „liegt im Papierkorb" | wurde entfernt |
| **↩ Zurücklegen** | holt genau diese Rampe an ihre alte Stelle zurück |
| ausgegraute Karte | steht gerade nicht in der Halle |

Zwei Filter greifen zusammen:

- **Zustand:** Alle · In der Halle · Entfernt
- **Typ:** Chips mit Farbpunkt und Anzahl je Kategorie — beliebig viele
  gleichzeitig wählbar. Keiner gewählt = alle Typen.

> An `spotSkatehalle_IST.3dm` geprüft (Szenario „Mobile Ramps beweglich"):
> 20 bewegliche Rampen ergeben **20 Karten**, filterbar nach 4 Typen
> (BNKS 6, Flats/Ebenen 12, QTRS 1, Walls 1). Vorher waren es 4 Karten für
> 20 Rampen.

### Ansichtsfenster folgen dem Katalog

Ist ein Drawer offen, rücken die 3D-Ansichten nach rechts, sodass sich Katalog
und Ansichtsfenster **nicht überlappen** — beim Ziehen am Breiten-Anfasser
laufen sie live mit, beim Schließen nehmen sie die Fläche wieder ein. Technisch
verschiebt eine CSS-Variable `--stage-left` die drei deckungsgleichen Ebenen
(`#viewport`, `#paneOverlay`, `#measureLabels`) gemeinsam; `paneRect()` rechnet
dadurch automatisch mit der kleineren Fläche. Am Handy bleibt es beim Overlay —
dort wäre für die 3D-Ansicht sonst kein Platz.

### Tutorial

Beim Wechsel in den Besuchermodus fragt die App: *Tutorial anschauen?* Sagt der
Besucher ja, führt eine Karte am unteren Rand durch **sechs Schritte**, die er
jeweils selbst ausführen muss — der nächste Schritt schaltet erst frei, wenn die
Aktion wirklich passiert ist:

1. Ansicht drehen
2. Grau vs. farbig verstehen (Lesen, weiter per Klick)
3. Eine **namentlich genannte Rampe suchen und auswählen** — der Typ mit den
   meisten Exemplaren wird automatisch als Suchziel gewählt
4. Diese Rampe verschieben
5. Über den Katalog eine Rampe nachlegen
6. Abschluss mit Hinweis auf Speichern und Rückgängig

Jederzeit neu startbar über *☰ Menü → Hilfe → 🎓 Tutorial starten*, abbrechbar
über das ✕ der Karte.

Zu jedem Schritt zeigt ein **animiertes Icon** die passende Geste — am PC mit
Maus (gedrückte Taste hervorgehoben), am Touchgerät mit Finger. Die Grafiken sind
Inline-SVG mit CSS-Keyframes, also ohne Bilddateien; bei *prefers-reduced-motion*
stehen sie automatisch still. Ist ein Schritt gelöst, wechselt das Icon auf einen
Haken.

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

### Kategorien: Einordnung nach Ähnlichkeit

Beim Wechsel in den Besuchermodus vergleicht die App jede **bewegliche** Rampe mit
den **gepinnten** und ordnet sie der Kategorie (= Layer) der ähnlichsten festen
Objekte zu. Verfahren: **k-Nearest-Neighbour (k=3)** auf z-standardisierten
Merkmalen — logarithmierte Maße, Steilheit H/L, Breitenverhältnis B/L und ein
flächengewichtetes **Neigungshistogramm** der Flächennormalen (waagerecht →
senkrecht). Das Histogramm ist nötig, weil eine Bounding-Box eine gekrümmte
Quarterpipe nicht von einer schrägen Bank trennen kann. Liegt nichts näher als
2,5 Standardabweichungen, landet die Rampe in „Sonstige".

Warum k-NN und nicht k-Means: die Kategorien sind durch das Pinnen bereits
vorgegeben — es ist ein Zuordnungs-, kein Clusterproblem. k-NN ist dafür
deterministisch, ohne Training und nachvollziehbar dokumentierbar.

> ⚠️ **Gemessene Genauigkeit:** In einer Leave-one-out-Kreuzvalidierung auf
> `spotSkatehalle_IST.3dm` trifft die Zuordnung die Layer-Wahrheit in **rund 62 %**
> der Fälle (Bounding-Box allein: 54 %). Rails werden fast immer erkannt (89–94 %),
> Walls kaum (20–29 %). Die Einordnung ist damit eine **Vorsortierung, keine
> sichere Klassifikation** — die Verwechslungen passieren überwiegend zwischen
> ohnehin ähnlichen Familien (BNKS ↔ QTRS ↔ Flats). Wer eine exakte Gruppierung
> braucht, korrigiert sie über *Meine Layer*.
>
> Grund für die Grenze: die Objekte der Datei tragen **keine Namen**, es gibt also
> außer Layer und Geometrie keine Information. Sprechende Objektnamen in Rhino
> (z. B. „quarterpipe_03") würden die Zuordnung deutlich sicherer machen.

Ohne gepinnte Rampen gibt es keine Vergleichsbasis — dann gruppiert die App wie
zuvor nach exakt gleicher Form und weist in der Statuszeile darauf hin.

### Meine Layer (Besuchermodus)

Über *☰ Menü → Meine Layer* legt der Besucher eigene Gruppen an: Name eingeben,
**+**, dann eine Rampe auswählen und den Layer antippen. Erneutes Antippen nimmt
sie wieder heraus, das ✕ löscht den Layer (die Rampen bleiben erhalten). Jede
Rampe gehört zu höchstens einem Besucher-Layer; die Rhino-Layer bleiben davon
unberührt, damit Kategorie und Einfärbung erhalten bleiben.

Beim **JSON-Export** fragt die App, welche dieser Layer mitsollen — jede Gruppe
mit Objektzahl zum Anhaken, plus „Ohne Layer". Im JSON steht der gewählte Layer
je Element unter `visitorLayer`.

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
