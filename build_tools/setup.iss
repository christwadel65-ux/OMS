[Setup]
; Application identifier (unique GUID)
AppId={{A5B3C4D5-E6F7-8A9B-0C1D-2E3F4A5B6C7D}}

; Application information
AppName=Outil de Maintenance Systeme
AppVersion=2.1.0
AppPublisher=OMS Project
AppPublisherURL=https://github.com/christwadel65-ux/OMS
AppSupportURL=https://github.com/christwadel65-ux/OMS/issues
AppUpdatesURL=https://github.com/christwadel65-ux/OMS/releases

; Installation directories
DefaultDirName={autopf}\OutilMaintenance
DefaultGroupName=Outil de Maintenance Systeme

; Output configuration
OutputDir=..\installer
OutputBaseFilename=OutilMaintenance_Setup_v2.1

; Setup visual configuration
SetupIconFile=..\assets\icon.ico
WizardStyle=modern
LicenseFile=..\docs\LICENSE.txt

; Compression and privileges
Compression=lzma2/max
SolidCompression=yes
PrivilegesRequired=admin
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

; Installation options
AllowNoIcons=yes
AllowUNCPath=no
CreateUninstallRegEntry=yes

[Languages]
Name: english; MessagesFile: compiler:Default.isl
Name: french; MessagesFile: compiler:Languages\French.isl

[Tasks]
Name: desktopicon; Description: Create a &desktop shortcut; GroupDescription: Additional options; Flags: unchecked
Name: quicklaunch; Description: Create a &Quick Launch shortcut; GroupDescription: Additional options; Flags: unchecked
Name: startmenu; Description: Create &Start Menu shortcuts; GroupDescription: Additional options; Flags: checked

[Files]
; Application files
Source: ..\dist\OutilMaintenance\*; DestDir: {app}; Flags: ignoreversion recursesubdirs createallsubdirs

; Documentation files
Source: ..\docs\README.txt; DestDir: {app}; Flags: ignoreversion
Source: ..\docs\LICENSE.txt; DestDir: {app}; Flags: ignoreversion
Source: ..\docs\BUILD_GUIDE.md; DestDir: {app}\docs; Flags: ignoreversion
Source: ..\docs\GUIDE_NOUVELLES_FONCTIONS.md; DestDir: {app}\docs; Flags: ignoreversion
Source: ..\docs\AMELIORATIONS.md; DestDir: {app}\docs; Flags: ignoreversion

[Icons]
; Start Menu icons
Name: {group}\Outil de Maintenance; Filename: {app}\OutilMaintenance.exe; IconFileName: {app}\OutilMaintenance.exe; Flags: createonlyiffileexists
Name: {group}\Uninstall; Filename: {uninstallexe}

; Desktop icon (optional, via task)
Name: {autodesktop}\Outil de Maintenance; Filename: {app}\OutilMaintenance.exe; Tasks: desktopicon; IconFileName: {app}\OutilMaintenance.exe

; Quick Launch icon (optional, via task)
Name: {userappdata}\Microsoft\Internet Explorer\Quick Launch\Outil de Maintenance; Filename: {app}\OutilMaintenance.exe; Tasks: quicklaunch; IconFileName: {app}\OutilMaintenance.exe

[Run]
; Launch application after installation
Filename: {app}\OutilMaintenance.exe; Description: Launch Outil de Maintenance; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up application directory on uninstall
Type: dirifempty; Name: {app}
Type: dirifempty; Name: {app}\docs

[Registry]
; Store installation information in registry
Root: HKLM; Subkey: Software\OutilMaintenance; ValueType: string; ValueName: InstallPath; ValueData: {app}; Flags: createvalueifdoesntexist
Root: HKLM; Subkey: Software\OutilMaintenance; ValueType: string; ValueName: Version; ValueData: 2.1.0; Flags: createvalueifdoesntexist
Root: HKLM; Subkey: Software\OutilMaintenance; ValueType: string; ValueName: PublisherURL; ValueData: https://github.com/christwadel65-ux/OMS; Flags: createvalueifdoesntexist

[Code]
{ Custom functions can be added here if needed in the future }

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssFinished then
  begin
    { Installation completed }
  end;
end;
