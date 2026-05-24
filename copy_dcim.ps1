# S24+ DCIM Copy Script - ASCII safe version
# Avoids Korean characters in script file to prevent encoding issues

param(
    [string]$DestBase
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Continue"

if (-not $DestBase) {
    Write-Host "ERROR: Please provide -DestBase parameter"
    exit 1
}

Write-Host "Destination base: $DestBase"

$shell = New-Object -ComObject Shell.Application
$computer = $shell.NameSpace(17)

# Find phone
$phone = $computer.Items() | Where-Object { $_.Name -like "*S24*" }
if (-not $phone) { Write-Host "ERROR: S24+ not found"; exit 1 }
Write-Host "Phone: $($phone.Name)"

# Internal storage = first item
$storage = $phone.GetFolder.Items().Item(0)
Write-Host "Storage: $($storage.Name)"

# Find DCIM
$dcim = $null
$sItems = $storage.GetFolder.Items()
for ($i = 0; $i -lt $sItems.Count; $i++) {
    if ($sItems.Item($i).Name -eq "DCIM") {
        $dcim = $sItems.Item($i)
        break
    }
}
if (-not $dcim) { Write-Host "ERROR: DCIM not found"; exit 1 }

# Prepare destination
$destDCIM = "$DestBase\DCIM"
Write-Host "destDCIM = [$destDCIM]"
if (-not (Test-Path $destDCIM)) {
    New-Item -ItemType Directory -Path $destDCIM -Force | Out-Null
    Write-Host "Created: $destDCIM"
}

$totalFiles = 0
$errorFiles = 0

function Copy-MTPFolder {
    param(
        [Parameter(Mandatory=$true)]$SrcItem,
        [Parameter(Mandatory=$true)][string]$DestPath
    )
    
    $folder = $SrcItem.GetFolder
    $items = $folder.Items()
    $count = $items.Count
    
    Write-Host ">> Scanning '$($SrcItem.Name)' ($count items) -> $DestPath"
    
    for ($i = 0; $i -lt $count; $i++) {
        $item = $items.Item($i)
        
        if ($item.IsFolder) {
            $subDest = "$DestPath\$($item.Name)"
            if (-not (Test-Path $subDest)) {
                New-Item -ItemType Directory -Path $subDest -Force | Out-Null
            }
            Copy-MTPFolder -SrcItem $item -DestPath $subDest
        } else {
            $script:totalFiles++
            try {
                $destFolderObj = $shell.NameSpace($DestPath)
                if ($destFolderObj) {
                    $destFolderObj.CopyHere($item, 0x10 -bor 0x400)
                    if ($script:totalFiles % 20 -eq 0) {
                        Write-Host "  ... $($script:totalFiles) files copied so far"
                    }
                } else {
                    Write-Host "  [ERR] shell.NameSpace failed for: $DestPath"
                    $script:errorFiles++
                }
            } catch {
                Write-Host "  [ERR] $($item.Name): $_"
                $script:errorFiles++
            }
        }
    }
}

Write-Host ""
Write-Host "========================================="
Write-Host "Starting DCIM copy..."
Write-Host "========================================="
$sw = [System.Diagnostics.Stopwatch]::StartNew()

Copy-MTPFolder -SrcItem $dcim -DestPath $destDCIM

$sw.Stop()
Write-Host ""
Write-Host "========================================="
Write-Host "Done!"
Write-Host "Total files: $totalFiles"
Write-Host "Errors: $errorFiles"
Write-Host "Time: $($sw.Elapsed.ToString('hh\:mm\:ss'))"
Write-Host "========================================="
