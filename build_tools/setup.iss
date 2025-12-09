[Setup]
AppId={{A5B3C4D5-E6F7-8A9B-0C1D-2E3F4A5B6C7D}}
AppName=Outil de Maintenance
AppVersion=2.1
DefaultDirName={autopf}\OutilMaintenance
DefaultGroupName=Outil de Maintenance
OutputDir=..\installer
OutputBaseFilename=OutilMaintenance_Setup_v2.1
SetupIconFile=..\assets\icon.ico
Compression=lzma2/max
SolidCompression=yes
PrivilegesRequired=admin

[Languages]
Name: english; MessagesFile: compiler:Default.isl

[Files]
Source: ..\dist\OutilMaintenance\*; DestDir: {app}; Flags: ignoreversion recursesubdirs
Source: ..\docs\README.txt; DestDir: {app}
Source: ..\docs\LICENSE.txt; DestDir: {app}

[Icons]
Name: {group}\Outil de Maintenance; Filename: {app}\OutilMaintenance.exe
Name: {group}\{cm:UninstallProgram,Outil de Maintenance}; Filename: {uninstallexe}
Name: {autodesktop}\Outil de Maintenance; Filename: {app}\OutilMaintenance.exe

[Run]
Filename: {app}\OutilMaintenance.exe; Description: Launch Application; Flags: nowait postinstall skipifsilent

[Code]
procedure DummyProcedure;
begin
end;
