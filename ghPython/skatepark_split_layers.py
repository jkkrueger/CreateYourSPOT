# skatepark_split_layers.py — GhPython / Rhino 8 Script-Komponente
# =============================================================================
# Teilt eine flache Brep-Liste anhand der parallelen Layer-Liste in einen
# DataTree auf: ein Branch pro Layer. Danach kann in Grasshopper pro
# Layer-Gruppe weitergearbeitet werden.
#
# Der Tree wird über ghpythonlib.treehelpers erzeugt — das funktioniert
# identisch im alten GhPython (IronPython 2) UND im neuen Rhino-8-Script-
# Editor (Python 3). Direktes DataTree[object]() macht dort Probleme
# (orange Leitung / leerer Output).
#
# ── INPUTS (im GH-Editor exakt so benennen!) ─────────────────────────────────
#   breps  │ List Access │ Type hint: No Type Hint (nimmt Breps UND Meshes)
#   layers │ List Access │ Type hint: str │ Layername je Brep (parallel!)
#
#   → z. B. direkt die Ausgänge geometry/layers der Build-Node oder
#     meshes/layers bzw. breps/layers der skatepark_import_mesh-Node.
#
# ── OUTPUTS (im GH-Editor anlegen) ───────────────────────────────────────────
#   geo_tree      │ DataTree │ Branch {0;0} = alle Breps des 1. Layers usw.
#                             (Reihenfolge = erstes Auftreten, stabil)
#   unique_layers │ list[str]│ Layername je Branch, index-gleich zu geo_tree
#   counts        │ list[int]│ Anzahl Geometrien je Branch (Kontrolle)
#   log           │ str      │ Statusmeldung
#
# ── WEITERARBEITEN MIT EINZELNEN LAYERN ──────────────────────────────────────
#   a) Explode Tree ("Bang!") an geo_tree → ein Ausgang pro Branch.
#   b) Gezielt einen Layer holen:
#        Member Index  (Set = unique_layers, Member = "QTRS")  → Index i
#        Tree Branch   (Tree = geo_tree, Path = {0;i})         → Brep-Liste
#   c) geo_tree direkt weiterleiten — GH-Komponenten arbeiten automatisch
#      branch-weise, jede Operation läuft getrennt pro Layer.
# =============================================================================

import ghpythonlib.treehelpers as th

unique_layers = []
counts = []
log = ""

_b = list(breps) if breps else []
_l = [str(x) for x in layers] if layers else []

if not _b:
    log = "Keine Breps am Eingang."
elif len(_b) != len(_l):
    n = min(len(_b), len(_l))
    log = "WARNUNG: {} Breps, aber {} Layer — nur die ersten {} Paare verwendet. ".format(
        len(_b), len(_l), n)
    _b, _l = _b[:n], _l[:n]

# Verschachtelte Listen: eine innere Liste pro Layer
nested = []
for brep, lay in zip(_b, _l):
    if brep is None:
        continue
    if lay not in unique_layers:
        unique_layers.append(lay)
        nested.append([])
    nested[unique_layers.index(lay)].append(brep)

geo_tree = th.list_to_tree(nested) if nested else None
counts = [len(lst) for lst in nested]

log += "OK | {} Geometrien in {} Layer-Branches: {}".format(
    sum(counts), len(unique_layers),
    ", ".join("{}({})".format(l, c) for l, c in zip(unique_layers, counts)))
