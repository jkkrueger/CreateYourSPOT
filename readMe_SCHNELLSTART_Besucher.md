# Skatepark-Planer (Besucherversion) — Schnellstart

Browser-Anwendung zum Anschauen und Arrangieren eines fertigen Skateparks:
eine vorbereitete Rhino-Datei (`.3dm`) laden, Rampen verschieben/drehen,
Ergebnis exportieren. Keine Installation nötig. Immer den **kompletten Ordner**
verwenden (`index.html` allein funktioniert nicht — `vendor/` wird gebraucht).

## Starten

- **Empfohlen (komplett offline):** Doppelklick auf `Start_Offline.bat`.
  Der Server startet, der Browser öffnet sich automatisch.
  Beenden: Konsolenfenster schließen. *(Python muss installiert sein.)*
- **Schnell:** `index.html` doppelklicken. Funktioniert sofort; für das
  **Laden von `.3dm`-Dateien wird dabei Internet benötigt**.

## ⚠️ Wichtig: welche `.3dm` lädt die App?

Die App zeigt eine `.3dm` nur, wenn deren Objekte **Netze (Meshes)** enthalten.
Frisch in Grasshopper gebakte Geometrie hat oft noch keine:

> Nach dem Baken in Rhino einmal in eine **gerenderte / schattierte Ansicht**
> wechseln (das erzeugt die Render-Meshes) und die **`.3dm` speichern**.

Erst dann kann die Web-App (rhino3dm) die Rampen laden und anzeigen — sonst
erscheinen sie **leer bzw. unsichtbar**. So fließt das Ergebnis aus der
Pipeline wieder sauber in die Besucher-App zurück.

## Stimmt die Größe nicht?

Nach dem Laden steht die reale Parkgröße in der Statusleiste. Wirkt alles zu
groß/klein, im Panel **Datei** unter „Einheit der Datei" die richtige Einheit
wählen (Automatisch, Millimeter, Zentimeter, Meter oder Zoll) — die Szene wird
sofort umgerechnet.

## Der Kreislauf in Kürze

Grasshopper (Import → Build → Bake) → Rhino →
**gerenderte Ansicht + `.3dm` speichern** → Besucher-App lädt die `.3dm`.
