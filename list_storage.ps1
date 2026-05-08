$shell = New-Object -ComObject Shell.Application
$computer = $shell.NameSpace(17) # This PC
$phone = $computer.Items() | Where-Object { $_.Name -match "Kevin" -and $_.Name -match "S24" }

if (-not $phone) {
    Write-Error "Phone not found"
    exit
}

$phoneFolder = $phone.GetFolder
$storage = $phoneFolder.Items() | Where-Object { $_.Name -match "내장" -or $_.Name -match "Internal" }

if (-not $storage) {
    Write-Error "Storage not found"
    exit
}

Write-Output "Accessing Storage: $($storage.Name)"
$storageFolder = $storage.GetFolder
foreach ($item in $storageFolder.Items()) {
    Write-Output "Folder/File: $($item.Name)"
}
