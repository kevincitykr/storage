[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$shell = New-Object -ComObject Shell.Application
$computer = $shell.NameSpace(17) # This PC
$phone = $computer.Items() | Where-Object { $_.Name -like "*S24*" }

if (-not $phone) {
    Write-Error "Phone not found"
    exit
}

$phoneFolder = $phone.GetFolder
$items = $phoneFolder.Items()
foreach ($item in $items) {
    Write-Output "Index: $($items.IndexOf($item)) - Name: $($item.Name)"
}
