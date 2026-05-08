$shell = New-Object -ComObject Shell.Application
$computer = $shell.NameSpace(17) # 17 is the ShellSpecialFolderConstants.ssfDRIVES (This PC)
foreach ($item in $computer.Items()) {
    Write-Output "Name: $($item.Name) - Path: $($item.Path)"
}
