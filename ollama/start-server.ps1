# ============================================================
# start-server.ps1
# Inicia el servidor de Project Zomboid en Docker.
#
# 1. Hace backup de server-files y server-data (si existen)
# 2. Copia la configuracion y saves locales al volumen Docker
# 3. Levanta docker compose
# ============================================================

# --- Configuracion -----------------------------------------------------------
$ProjectDir       = "D:\Docker\ProyectZomboid-DedicatedServer"
$BackupRoot       = "D:\Docker\ProyectZomboid-Backups"

# Rutas locales de Zomboid (fuera de Docker)
$LocalServerCfg   = "C:\Users\Usuario\Zomboid\Server"
$LocalSaveData    = "C:\Users\Usuario\Zomboid\Saves\Multiplayer\servertest"

# Rutas destino dentro del volumen Docker (server-data = /project-zomboid-config)
$DockerServerCfg  = "$ProjectDir\server-data\Server"
$DockerSaveData   = "$ProjectDir\server-data\Saves\Multiplayer\servertest"
# ------------------------------------------------------------------------------

$Timestamp  = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$BackupPath = "$BackupRoot\$Timestamp"

# === PASO 1: Backup ==========================================================
Write-Host ""
Write-Host "=== PASO 1: Copia de seguridad ===" -ForegroundColor Cyan

$backedUp = $false

if (Test-Path "$ProjectDir\server-files") {
    Write-Host "  Respaldando server-files..."
    New-Item -Path "$BackupPath\server-files" -ItemType Directory -Force | Out-Null
    Copy-Item -Path "$ProjectDir\server-files\*" -Destination "$BackupPath\server-files" -Recurse -Force
    $backedUp = $true
}

if (Test-Path "$ProjectDir\server-data") {
    Write-Host "  Respaldando server-data..."
    New-Item -Path "$BackupPath\server-data" -ItemType Directory -Force | Out-Null
    Copy-Item -Path "$ProjectDir\server-data\*" -Destination "$BackupPath\server-data" -Recurse -Force
    $backedUp = $true
}

if ($backedUp) {
    Write-Host "  Backup guardado en: $BackupPath" -ForegroundColor Green
} else {
    Write-Host "  No hay datos previos que respaldar (primer inicio)." -ForegroundColor Yellow
    # Eliminar carpeta de backup vacia si no se uso
    if (Test-Path $BackupPath) { Remove-Item $BackupPath -Force -Recurse }
}

# === PASO 2: Copiar configuracion y saves =====================================
Write-Host ""
Write-Host "=== PASO 2: Copiando configuracion y saves locales ===" -ForegroundColor Cyan

if (Test-Path $LocalServerCfg) {
    Write-Host "  Copiando Server config desde: $LocalServerCfg"
    New-Item -Path $DockerServerCfg -ItemType Directory -Force | Out-Null
    Copy-Item -Path "$LocalServerCfg\*" -Destination $DockerServerCfg -Recurse -Force
    Write-Host "    -> $DockerServerCfg" -ForegroundColor Green
} else {
    Write-Host "  AVISO: No se encontro $LocalServerCfg — se omite." -ForegroundColor Yellow
}

if (Test-Path $LocalSaveData) {
    Write-Host "  Copiando Saves desde: $LocalSaveData"
    New-Item -Path $DockerSaveData -ItemType Directory -Force | Out-Null
    Copy-Item -Path "$LocalSaveData\*" -Destination $DockerSaveData -Recurse -Force
    Write-Host "    -> $DockerSaveData" -ForegroundColor Green
} else {
    Write-Host "  AVISO: No se encontro $LocalSaveData — se omite." -ForegroundColor Yellow
}

# === PASO 3: Iniciar Docker Compose ==========================================
Write-Host ""
Write-Host "=== PASO 3: Iniciando servidor ===" -ForegroundColor Cyan
docker compose -f "$ProjectDir\docker-compose.yml" up -d

Write-Host ""
Write-Host "Servidor iniciado. Usa 'docker compose logs -f' para ver los logs." -ForegroundColor Green
