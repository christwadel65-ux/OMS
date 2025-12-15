[Setup]
AppId={{A5B3C4D5-E6F7-8A9B-0C1D-2E3F4A5B6C7D}}
AppName=Outil de Maintenance Systeme
AppVersion=1.0.1
AppPublisher=OMS Project
DefaultDirName={autopf}\OutilMaintenance
DefaultGroupName=Outil de Maintenance Systeme
OutputDir=..\installer
OutputBaseFilename=OutilMaintenance_Setup_v1.0.1
SetupIconFile=..\assets\icon.ico
WizardStyle=modern
LicenseFile=..\docs\LICENSE.txt
Compression=lzma2/max
SolidCompression=yes
PrivilegesRequired=admin
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: english; MessagesFile: compiler:Default.isl
Name: french; MessagesFile: compiler:Languages\French.isl

[Tasks]
Name: desktopicon; Description: Create desktop shortcut
Name: quicklaunch; Description: Create Quick Launch shortcut

[Files]
Source: ..\dist\OutilMaintenance\*; DestDir: {app}; Flags: ignoreversion recursesubdirs
Source: ..\docs\README.txt; DestDir: {app}; Flags: ignoreversion
Source: ..\docs\LICENSE.txt; DestDir: {app}; Flags: ignoreversion

[Icons]
Name: {group}\Outil de Maintenance; Filename: {app}\OutilMaintenance.exe
Name: {group}\Uninstall; Filename: {uninstallexe}
Name: {autodesktop}\Outil de Maintenance; Filename: {app}\OutilMaintenance.exe; Tasks: desktopicon

[Run]
Filename: {app}\OutilMaintenance.exe; Description: Launch Outil de Maintenance; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: dirifempty; Name: {app}

[Registry]
Root: HKLM; Subkey: Software\OutilMaintenance; ValueType: string; ValueName: InstallPath; ValueData: {app}
Root: HKLM; Subkey: Software\OutilMaintenance; ValueType: string; ValueName: Version; ValueData: 1.0.1
