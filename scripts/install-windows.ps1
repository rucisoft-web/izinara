# Pasang dan jalankan Izinara di Windows 11 dengan Docker Desktop.
# Pemakaian (PowerShell):
#   powershell -ExecutionPolicy Bypass -File install-windows.ps1            # dengan data demo
#   powershell -ExecutionPolicy Bypass -File install-windows.ps1 -NoDemo    # tanpa data demo
param(
    [string]$Dir = "$HOME\izinara",
    [string]$Branch = "claude/project-thread-pf8s62",
    [string]$Database = "izinara",
    [switch]$NoDemo
)
$ErrorActionPreference = "Stop"

function Test-Command($name) { [bool](Get-Command $name -ErrorAction SilentlyContinue) }

# 1. Git dan Docker Desktop
$missing = @()
if (-not (Test-Command git)) { $missing += "Git.Git" }
if (-not (Test-Command docker)) { $missing += "Docker.DockerDesktop" }
if ($missing.Count -gt 0) {
    Write-Host "Memasang $($missing -join ', ') lewat winget..." -ForegroundColor Cyan
    foreach ($id in $missing) {
        winget install --id $id -e --accept-source-agreements --accept-package-agreements
    }
    Write-Host ""
    Write-Host "Selesai memasang. Restart Windows bila diminta, buka Docker Desktop sampai statusnya 'Engine running'," -ForegroundColor Yellow
    Write-Host "lalu jalankan skrip ini lagi di jendela PowerShell baru." -ForegroundColor Yellow
    exit 0
}

# 2. Tunggu Docker Desktop siap
Write-Host "Memeriksa Docker Desktop..." -ForegroundColor Cyan
$ready = $false
for ($i = 0; $i -lt 60; $i++) {
    cmd /c "docker info >nul 2>&1"
    if ($LASTEXITCODE -eq 0) { $ready = $true; break }
    if ($i -eq 0) {
        $exe = "$env:ProgramFiles\Docker\Docker\Docker Desktop.exe"
        if (Test-Path $exe) { Start-Process $exe }
        Write-Host "Menunggu Docker Desktop menyala (maks. 5 menit)..."
    }
    Start-Sleep -Seconds 5
}
if (-not $ready) { throw "Docker Desktop belum berjalan. Buka Docker Desktop lalu jalankan skrip ini lagi." }

# 3. Ambil kode Izinara
if (Test-Path "$Dir\.git") {
    Write-Host "Memperbarui kode di $Dir..." -ForegroundColor Cyan
    git -C $Dir pull --ff-only
} else {
    Write-Host "Mengunduh Izinara ke $Dir..." -ForegroundColor Cyan
    git clone -b $Branch https://github.com/rucisoft-web/izinara.git $Dir
}
Set-Location $Dir

# 4. Buat database dan pasang modul (hanya pertama kali)
$marker = Join-Path $Dir ".izinara-$Database-terpasang"
if (-not (Test-Path $marker)) {
    $modules = if ($NoDemo) { "izinara,izinara_theme" } else { "izinara,izinara_demo,izinara_theme" }
    Write-Host "Membuat database '$Database' dan memasang $modules (beberapa menit)..." -ForegroundColor Cyan
    docker compose run --rm odoo odoo `
        --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/izinara `
        -d $Database -i $modules --without-demo=all --stop-after-init
    if ($LASTEXITCODE -ne 0) { throw "Pemasangan modul gagal. Lihat pesan di atas." }
    New-Item -ItemType File -Path $marker | Out-Null
}

# 5. Jalankan Odoo
Write-Host "Menjalankan Izinara..." -ForegroundColor Cyan
docker compose up -d
if ($LASTEXITCODE -ne 0) { throw "docker compose up gagal." }

for ($i = 0; $i -lt 60; $i++) {
    try {
        Invoke-WebRequest -Uri "http://localhost:8069/web/login" -UseBasicParsing -TimeoutSec 5 | Out-Null
        break
    } catch { Start-Sleep -Seconds 3 }
}
Start-Process "http://localhost:8069"

Write-Host ""
Write-Host "Izinara berjalan di http://localhost:8069" -ForegroundColor Green
Write-Host "  Login admin : admin / admin (segera ganti kata sandinya)"
if (-not $NoDemo) { Write-Host "  Akun demo   : budi.purchasing, rina.ml, hasan.halal, dewi.izin, andi.impor, sari.manajer (kata sandi: izinara)" }
Write-Host "  Berhenti    : cd $Dir; docker compose down"
Write-Host "  Jalan lagi  : cd $Dir; docker compose up -d"
