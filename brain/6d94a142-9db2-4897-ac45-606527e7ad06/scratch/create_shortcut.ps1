$WshShell = New-Object -ComObject WScript.Shell
$ShortcutPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\Syncthing.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "C:\Users\ksohw\AppData\Local\Programs\Syncthing\syncthing.exe"
$Shortcut.Arguments = "serve --no-console --no-browser"
$Shortcut.WorkingDirectory = "C:\Users\ksohw\AppData\Local\Programs\Syncthing"
$Shortcut.Save()
Write-Host "Shortcut created at $ShortcutPath"
