# ============================================================
#  Skatepark-Planer - Offline-Start (PowerShell)
#
#  STARTEN:
#    Rechtsklick auf diese Datei -> "Mit PowerShell ausfuehren"
#
#  Falls Windows das blockiert ("Ausfuehrung von Skripten ist
#  deaktiviert"), stattdessen PowerShell im Ordner oeffnen und
#  eingeben:
#       powershell -ExecutionPolicy Bypass -File .\Start_Offline.ps1
#
#  Beenden: dieses Fenster schliessen oder Strg+C
# ============================================================

$Port = 8000

# In den Ordner dieses Skripts wechseln
Set-Location -LiteralPath $PSScriptRoot

Write-Host ""
Write-Host "  Skatepark-Planer - lokaler Server" -ForegroundColor Cyan
Write-Host "  Ordner: $PSScriptRoot"
Write-Host ""

# --- Python suchen -------------------------------------------------------
$py = $null
foreach ($cmd in @("python", "py", "python3")) {
    $found = Get-Command $cmd -ErrorAction SilentlyContinue
    if ($found) {
        # Windows-Store-Platzhalter aussortieren (startet nur den Store)
        if ($found.Source -notlike "*WindowsApps*") {
            $py = $found.Source
            break
        }
    }
}

if (-not $py) {
    Write-Host "  FEHLER: Python wurde nicht gefunden." -ForegroundColor Red
    Write-Host ""
    Write-Host "  Moeglichkeiten:"
    Write-Host "    1. Python installieren: https://www.python.org/downloads/"
    Write-Host "       (bei der Installation 'Add Python to PATH' ankreuzen)"
    Write-Host "    2. Oder index.html doppelklicken - dann wird fuer den"
    Write-Host "       .3dm-Import allerdings eine Internetverbindung benoetigt."
    Write-Host ""
    Read-Host "  Mit Enter beenden"
    exit 1
}

# --- Freien Port suchen, falls 8000 belegt ist ---------------------------
while ((Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue)) {
    Write-Host "  Port $Port ist belegt - versuche $($Port + 1)" -ForegroundColor Yellow
    $Port++
}

$url = "http://localhost:$Port/index.html"

Write-Host "  Python:  $py"
Write-Host "  Adresse: $url" -ForegroundColor Green
Write-Host ""
Write-Host "  Browser oeffnet sich gleich automatisch."
Write-Host "  Zum Beenden: dieses Fenster schliessen oder Strg+C"
Write-Host ""

# Browser kurz zeitversetzt oeffnen, damit der Server schon laeuft
Start-Job -ScriptBlock {
    param($u)
    Start-Sleep -Milliseconds 1200
    Start-Process $u
} -ArgumentList $url | Out-Null

# --- Server starten (blockiert, bis das Fenster geschlossen wird) --------
& $py -m http.server $Port

Write-Host ""
Write-Host "  Server beendet." -ForegroundColor Yellow
Read-Host "  Mit Enter schliessen"
