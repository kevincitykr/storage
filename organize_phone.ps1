param(
    [string]$DestinationRoot = "E:\20260502 S24 백업",
    [datetime]$ThresholdDate = "2026-01-01",
    [switch]$DryRun
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$shell = New-Object -ComObject Shell.Application
$computer = $shell.NameSpace(17) # This PC

# Find Phone
$phone = $computer.Items() | Where-Object { $_.Name -like "*S24*" }
if (-not $phone) {
    Write-Error "Phone 'S24+' not found in This PC"
    return
}

# Find Internal Storage
$items = $phone.GetFolder.Items()
$storage = $null
for ($i=0; $i -lt $items.Count; $i++) {
    $item = $items.Item($i)
    $subItems = $item.GetFolder.Items()
    $hasMedia = $false
    for ($j=0; $j -lt $subItems.Count; $j++) {
        if ($subItems.Item($j).Name -match "DCIM|Pictures|Download") {
            $hasMedia = $true
            break
        }
    }
    if ($hasMedia) {
        $storage = $item
        break
    }
}

if (-not $storage) {
    $storage = $items.Item(0)
}

Write-Host "============================================="
Write-Host "S24+ Phone Storage Organizer"
Write-Host "============================================="
Write-Host "Using Storage: $($storage.Name)"
Write-Host "Destination: $DestinationRoot"
Write-Host "Threshold Date: $ThresholdDate"
Write-Host "Mode: $(if ($DryRun) {'DRY RUN'} else {'LIVE COPY'})"
Write-Host "============================================="

$targetBase = $DestinationRoot

if (-not (Test-Path $targetBase)) {
    New-Item -ItemType Directory -Path $targetBase -Force | Out-Null
    Write-Host "Created destination directory: $targetBase"
}

$fileCount = 0
$errorCount = 0
$skipCount = 0
$startTime = Get-Date

# Log file for tracking
$logFile = Join-Path $targetBase "_copy_log_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"

function Write-Log($message) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] $message"
    Add-Content -Path $logFile -Value $logEntry -Encoding UTF8
    Write-Host $logEntry
}

function Process-Folder($folderItem, $relativeDir) {
    $folder = $folderItem.GetFolder
    $items = $folder.Items()
    
    for ($i=0; $i -lt $items.Count; $i++) {
        $item = $items.Item($i)
        
        if ($item.IsFolder) {
            # Skip system/app folders
            if ($item.Name -eq "Android") {
                Write-Log "SKIP FOLDER: Android (system folder)"
                continue
            }
            
            $newRelativeDir = if ($relativeDir -eq ".") { $item.Name } else { Join-Path $relativeDir $item.Name }
            Process-Folder $item $newRelativeDir
        } else {
            # It's a file - check modification date
            $modDate = $folder.GetDetailsOf($item, 3) # Date Modified
            try {
                $dt = [datetime]::Parse($modDate)
            } catch {
                $script:skipCount++
                continue
            }
            
            if ($dt -lt $ThresholdDate) {
                $script:fileCount++
                $destDir = if ($relativeDir -eq ".") { $targetBase } else { Join-Path $targetBase $relativeDir }
                $destPath = Join-Path $destDir $item.Name
                
                if ($DryRun) {
                    Write-Log "[DRY] ($($script:fileCount)) $($item.Name) | Modified: $($dt.ToString('yyyy-MM-dd')) | -> $destDir"
                } else {
                    # Check if already copied
                    if (Test-Path $destPath) {
                        Write-Log "[SKIP] ($($script:fileCount)) $($item.Name) already exists at destination"
                        continue
                    }
                    
                    try {
                        # Create destination directory
                        if (-not (Test-Path $destDir)) {
                            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
                        }
                        
                        # Copy using Shell (works with MTP)
                        $destFolder = $shell.NameSpace($destDir)
                        if ($destFolder) {
                            # Flags: 16 = Yes to All, 1024 = No error UI, 4 = No progress dialog
                            $destFolder.CopyHere($item, 16 -bor 1024 -bor 4)
                            
                            # Brief wait for MTP transfer to complete
                            Start-Sleep -Milliseconds 500
                            
                            # Verify
                            if (Test-Path $destPath) {
                                Write-Log "[OK] ($($script:fileCount)) $($item.Name) | $($dt.ToString('yyyy-MM-dd')) | -> $destDir"
                            } else {
                                # Retry with longer wait (MTP can be slow for large files)
                                Start-Sleep -Seconds 2
                                if (Test-Path $destPath) {
                                    Write-Log "[OK-RETRY] ($($script:fileCount)) $($item.Name)"
                                } else {
                                    Write-Log "[FAIL] ($($script:fileCount)) $($item.Name) - copy verification failed"
                                    $script:errorCount++
                                }
                            }
                        } else {
                            Write-Log "[ERROR] ($($script:fileCount)) Cannot access destination folder: $destDir"
                            $script:errorCount++
                        }
                    } catch {
                        Write-Log "[ERROR] ($($script:fileCount)) $($item.Name): $($_.Exception.Message)"
                        $script:errorCount++
                    }
                }
            }
        }
    }
}

Write-Log "Starting file scan and copy..."
Process-Folder $storage "."

$elapsed = (Get-Date) - $startTime
Write-Host ""
Write-Host "============================================="
Write-Host "COMPLETE"
Write-Host "============================================="
Write-Host "Total files processed: $fileCount"
Write-Host "Errors: $errorCount"
Write-Host "Skipped (no date): $skipCount"
Write-Host "Elapsed time: $($elapsed.ToString('hh\:mm\:ss'))"
Write-Host "Log saved: $logFile"
Write-Host "============================================="
Write-Log "DONE - Total: $fileCount, Errors: $errorCount, Skipped: $skipCount, Time: $($elapsed.ToString('hh\:mm\:ss'))"
