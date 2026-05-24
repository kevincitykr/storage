Set WshShell = CreateObject("WScript.Shell")
strStartup = WshShell.SpecialFolders("Startup")
Set oShellLink = WshShell.CreateShortcut(strStartup & "\START_SYNC_KB.lnk")
oShellLink.TargetPath = "E:\desktop_kevincity\999. knowledge Base\START_SYNC_KB.bat"
oShellLink.WorkingDirectory = "E:\desktop_kevincity\999. knowledge Base"
oShellLink.WindowStyle = 1
oShellLink.Save
