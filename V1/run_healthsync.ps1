# HealthSync PowerShell Startup Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "HealthSync - Integrated Healthcare Platform" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Installing required packages..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt
    Write-Host "✓ Packages installed successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install packages" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Creating necessary directories..." -ForegroundColor Yellow
$directories = @("uploads", "models", "data", "logs")
foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Host "✓ Created directory: $dir" -ForegroundColor Green
    } else {
        Write-Host "✓ Directory exists: $dir" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Starting HealthSync application..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🌐 Web Interface: http://localhost:5000" -ForegroundColor White
Write-Host "🔬 Medical Imaging: http://localhost:5000/medical-imaging" -ForegroundColor White
Write-Host "🩸 Blood Bank: http://localhost:5000/blood-bank" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the Flask application
try {
    python app.py
} catch {
    Write-Host "❌ Failed to start the application" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
}

Read-Host "Press Enter to exit"
