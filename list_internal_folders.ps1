[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$shell = New-Object -ComObject Shell.Application
$computer = $shell.NameSpace(17) # This PC
$phone = $computer.Items() | Where-Object { $_.Name -like "*S24*" }
$storage = $phone.GetFolder.Items() | Where-Object { $_.Name -eq "내장 저장공간" }

if (-not $storage) {
    Write-Error "Storage '내장 저장공간' not found"
    exit
}

$storageFolder = $storage.GetFolder
foreach ($item in $storageFolder.Items()) {
    Write-Output "Folder: $($item.Name)"
}
