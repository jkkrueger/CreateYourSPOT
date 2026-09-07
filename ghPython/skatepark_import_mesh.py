# skatepark_import_mesh.py — GhPython / Rhino 8 Script-Komponente
# =============================================================================
# Liest die EXAKTE 3D-Geometrie aus dem JSON der Besucherversion (Feld "mesh"
# je Element) — für Objekte, die nicht parametrisch erstellt, sondern direkt
# in Rhino gezeichnet wurden. Das JSON bleibt gleichzeitig kompatibel zu
# skatepark_import_v2.py (parametrischer Rebuild über types/dims).
#
# ── INPUTS (im GH-Editor anlegen) ────────────────────────────────────────────
#   json_path │ str  │ Item │ Pfad zur .json aus der Besucherversion
#   bake      │ bool │ Item │ True = direkt ins aktive Rhino-Dokument baken
#                            (Layer inkl. Hierarchie + Farbe werden angelegt)
#   clear     │ bool │ Item │ True = vor dem Baken alle Objekte auf den
#                            Ziel-Layern löschen (optional, Standard False)
#
# ── OUTPUTS (im GH-Editor exakt so benennen) ─────────────────────────────────
#   meshes  │ list[Mesh] │ exakte Geometrie je Element (Rhino-Welt, cm)
#   breps   │ list[Brep] │ Mesh→Brep-Konvertierung — für bestehende
#                          Brep-basierte Bake-Nodes (skatepark_bake_grouped)
#   layers  │ list[str]  │ Layerpfad je Element (parallel zu meshes)
#   names   │ list[str]  │ Objektname je Element (parallel zu meshes)
#   log     │ str        │ Statusmeldung — unbedingt als Output anlegen!
#
# ── KOORDINATEN ──────────────────────────────────────────────────────────────
#   Die Vertices im JSON sind bereits fertige RHINO-Weltkoordinaten (Z-up, cm):
#   Rotation und Position sind von der Web-App eingerechnet, die Achsen-
#   konvertierung (rhino = web.x, -web.z, web.y) ebenfalls. Hier wird NICHTS
#   mehr transformiert — nur Mesh aufbauen.
# =============================================================================

import json
import Rhino
import Rhino.Geometry as rg

meshes = []
breps  = []
layers = []
names  = []
log    = ""
_errors = []

# ── JSON einlesen (IronPython-2-kompatibel: kein encoding-Parameter) ─────────
data = None
try:
    with open(json_path, 'r') as f:
        data = json.load(f)
except Exception as e:
    log = "FEHLER beim Oeffnen/Parsen: {}".format(e)

def _build_mesh(md):
    """mesh-Dict {vertices:[x,y,z,...], faces:[a,b,c,...]} -> rg.Mesh oder None."""
    verts = md.get('vertices') or []
    faces = md.get('faces') or []
    if len(verts) < 9 or len(faces) < 3:
        return None
    m = rg.Mesh()
    for i in range(0, len(verts) - 2, 3):
        m.Vertices.Add(float(verts[i]), float(verts[i + 1]), float(verts[i + 2]))
    vc = m.Vertices.Count
    for i in range(0, len(faces) - 2, 3):
        a, b, c = int(faces[i]), int(faces[i + 1]), int(faces[i + 2])
        if a < vc and b < vc and c < vc:
            m.Faces.AddFace(a, b, c)
    if m.Faces.Count == 0:
        return None
    m.Normals.ComputeNormals()
    m.Compact()
    return m

def _hex_color(hx):
    """'#rrggbb' -> (r, g, b) oder None."""
    try:
        hx = (hx or '').lstrip('#')
        return (int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16))
    except Exception:
        return None

# ── Elemente verarbeiten ─────────────────────────────────────────────────────
if data is not None:
    els = data.get('elements', [])
    for i, el in enumerate(els):
        try:
            md = el.get('mesh')
            if not md:
                _errors.append("Element {} ohne mesh-Feld (altes JSON?)".format(i))
                continue
            m = _build_mesh(md)
            if m is None:
                _errors.append("Element {}: Mesh nicht baubar".format(i))
                continue
            meshes.append(m)
            layers.append(str(el.get('layer', 'Import')))
            names.append(str(el.get('typeName', el.get('id', 'Objekt_{}'.format(i)))))
            # Brep-Konvertierung fuer Brep-basierte Bake-Nodes (kann bei sehr
            # grossen Meshes dauern — nur nutzen, wenn gebraucht)
            try:
                b = rg.Brep.CreateFromMesh(m, True)
                breps.append(b)
            except Exception:
                breps.append(None)
        except Exception as ex:
            _errors.append("Element {}: {}".format(i, ex))

    # ── Optional: direkt baken (Layer inkl. Hierarchie + Farbe) ──────────────
    if bake and meshes:
        doc = Rhino.RhinoDoc.ActiveDoc
        try:
            from System.Drawing import Color
        except Exception:
            Color = None

        def _ensure_layer_path(full_path, rgb):
            """Layerpfad 'A::B::C' anlegen (falls noetig), Index des Blatts zurueckgeben."""
            parts = [p.strip() for p in full_path.split('::') if p.strip()]
            if not parts:
                parts = ['Import']
            path_so_far = ''
            idx = -1
            for k, part in enumerate(parts):
                path_so_far = part if not path_so_far else path_so_far + '::' + part
                idx = doc.Layers.FindByFullPath(path_so_far, -1)
                if idx < 0:
                    lyr = Rhino.DocObjects.Layer()
                    lyr.Name = part
                    if k > 0:
                        parent_idx = doc.Layers.FindByFullPath(
                            '::'.join(parts[:k]), -1)
                        if parent_idx >= 0:
                            lyr.ParentLayerId = doc.Layers[parent_idx].Id
                    if Color is not None:
                        if k == len(parts) - 1 and rgb:
                            lyr.Color = Color.FromArgb(rgb[0], rgb[1], rgb[2])
                        else:
                            lyr.Color = Color.FromArgb(128, 130, 135)
                    idx = doc.Layers.Add(lyr)
            return idx

        # Layer-Indizes vorbereiten (+ optional leeren)
        layer_idx = {}
        for i, lp in enumerate(layers):
            if lp in layer_idx:
                continue
            rgb = _hex_color(els[i].get('color') if i < len(els) else None)
            layer_idx[lp] = _ensure_layer_path(lp, rgb)

        if clear:
            removed = 0
            for lp, li in layer_idx.items():
                if li < 0:
                    continue
                lyr = doc.Layers[li]
                for o in doc.Objects.FindByLayer(lyr) or []:
                    doc.Objects.Delete(o, True)
                    removed += 1
            _errors.append("{} alte Objekte geloescht".format(removed)) if removed else None

        baked = 0
        for i, m in enumerate(meshes):
            attr = Rhino.DocObjects.ObjectAttributes()
            li = layer_idx.get(layers[i], -1)
            if li >= 0:
                attr.LayerIndex = li
            attr.Name = names[i]
            gid = doc.Objects.AddMesh(m, attr)
            if gid != gid.Empty:
                baked += 1
        doc.Views.Redraw()
        log = "GEBAKT: {}/{} Meshes auf {} Layer".format(baked, len(meshes), len(layer_idx))
    else:
        src = data.get('source', '?')
        log = "OK | {} Meshes aus '{}' | bake=False (nur GH-Geometrie)".format(len(meshes), src)

if _errors:
    log += " | HINWEISE: " + " | ".join(_errors[:6])
