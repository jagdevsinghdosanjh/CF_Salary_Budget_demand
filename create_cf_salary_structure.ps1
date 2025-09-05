# create_cf_salary_structure.ps1

# Define subfolders relative to current directory
$folders = @(
    "data",
    "modules",
    "assets",
    "templates"
)

# Create folders
foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder | Out-Null
        Write-Host "📁 Created folder: $folder"
    } else {
        Write-Host "⚠️ Folder already exists: $folder"
    }
}

# Define placeholder files and their initial content
$files = @{
    "app.py" = "# Streamlit entry point"
    "modules\salary_calculator.py" = "# Salary calculation logic"
    "modules\data_loader.py" = "# Excel data loading logic"
    "modules\utils.py" = "# Utility functions"
    "assets\styles.css" = "/* Custom styles */"
    "templates\index.html" = "<!-- Optional HTML template -->"
    "README.md" = "# CF Salary Budget Demand Project"
}

# Create files
foreach ($path in $files.Keys) {
    if (-not (Test-Path $path)) {
        New-Item -ItemType File -Path $path -Force | Out-Null
        Set-Content -Path $path -Value $files[$path]
        Write-Host "📝 Created file: $path"
    } else {
        Write-Host "⚠️ File already exists: $path"
    }
}

Write-Host "`n✅ Project structure initialized!"
