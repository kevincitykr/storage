[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$shell = New-Object -ComObject Shell.Application
$computer = $shell.NameSpace(17) # This PC
$phone = $computer.Items() | Where-Object { $_.Name -like "*S24*" }

if (-not $phone) {
    Write-Error "Phone not found"
    exit
}

$phoneFolder = $phone.GetFolder
# Find storage that contains '저장' but not '듀얼'
$storage = $phoneFolder.Items() | Where-Object { $_.Name -match "저장" -and $_.Name -notmatch "듀얼" }

if (-not $storage) {
    Write-Error "Storage not found"
    exit
}

Write-Output "Selected Storage: $($storage.Name)"
$storageFolder = $storage.GetFolder
foreach ($item in $storageFolder.Items()) {
    Write-Output "Item: $($item.Name)"
}
