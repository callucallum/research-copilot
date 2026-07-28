Add-Type -AssemblyName System.Windows.Forms

$folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
$folderBrowser.Description = "Select project folder"

$result = $folderBrowser.ShowDialog()

if ($result -ne "OK") {
    exit
}

$projectPath = $folderBrowser.SelectedPath

Write-Host "Selected project:"
Write-Host $projectPath

$root = Split-Path $PSScriptRoot -Parent

& "$root\scripts\start.cmd" $projectPath