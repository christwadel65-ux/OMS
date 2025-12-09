; Script Inno Setup pour Outil de Maintenance Système
; Auteur: c.Lecomte
; Version: 2.1
; Date: 9 décembre 2025

#define MyAppName "Outil de Maintenance Système"
#define MyAppVersion "2.1"
#define MyAppPublisher "c.Lecomte"
#define MyAppExeName "OutilMaintenance.exe"
#define MyAppURL "https://github.com/votrecompte/outil-maintenance"

[Setup]
; Informations de base
AppId={{A5B3C4D5-E6F7-8A9B-0C1D-2E3F4A5B6C7D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\OutilMaintenance
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=..\docs\LICENSE.txt
InfoBeforeFile=..\docs\README.txt
OutputDir=..\installer
OutputBaseFilename=OutilMaintenance_Setup_v{#MyAppVersion}
SetupIconFile=..\assets\icon.ico
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

; Configuration visuelle
WizardImageFile=..\assets\installer_banner.bmp
WizardSmallImageFile=..\assets\installer_small.bmp

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode
Name: "startmenuicon"; Description: "Créer un raccourci dans le menu Démarrer"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checked

[Files]
; Exécutable principal (généré avec PyInstaller)
Source: "..\dist\OutilMaintenance\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Ne pas utiliser "Flags: ignoreversion" sur les fichiers système partagés

; Documentation
Source: "..\docs\README.txt"; DestDir: "{app}"; Flags: isreadme
Source: "..\docs\GUIDE_NOUVELLES_FONCTIONS.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\docs\AMELIORATIONS.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\docs\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"
Name: "{group}\Guide d'utilisation"; Filename: "{app}\GUIDE_NOUVELLES_FONCTIONS.md"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; WorkingDir: "{app}"
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon; WorkingDir: "{app}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\logs"
Type: filesandordirs; Name: "{app}\exports"
Type: filesandordirs; Name: "{app}\__pycache__"

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  // Vérifier si .NET Framework 4.5 ou supérieur est installé (pour certaines dépendances)
  Result := True;
  
  if MsgBox('Cet outil nécessite des droits administrateur pour certaines fonctionnalités (nettoyage Prefetch, analyse système).' + #13#10 + #13#10 + 
            'Voulez-vous continuer l''installation ?', mbConfirmation, MB_YESNO) = IDNO then
  begin
    Result := False;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Créer les dossiers de travail
    CreateDir(ExpandConstant('{app}\logs'));
    CreateDir(ExpandConstant('{app}\exports'));
  end;
end;

function InitializeUninstall(): Boolean;
begin
  Result := True;
  if MsgBox('Voulez-vous également supprimer les logs et exports générés par l''application ?', mbConfirmation, MB_YESNO) = IDYES then
  begin
    DelTree(ExpandConstant('{app}\logs'), True, True, True);
    DelTree(ExpandConstant('{app}\exports'), True, True, True);
  end;
end;

[Registry]
; Ajouter l'application au registre pour l'associer aux tâches de maintenance
Root: HKLM; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; ValueType: string; ValueName: "Version"; ValueData: "{#MyAppVersion}"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; ValueType: string; ValueName: "InstallDate"; ValueData: "{code:GetDateTimeString}"; Flags: uninsdeletekey

[Code]
function GetDateTimeString(Param: String): String;
begin
  Result := GetDateTimeString('yyyy-mm-dd hh:nn:ss', '-', ':');
end;

[Messages]
french.BeveledLabel=Installation par c.Lecomte
french.SetupAppTitle=Installation - {#MyAppName}
french.SetupWindowTitle=Installation - {#MyAppName} {#MyAppVersion}

[CustomMessages]
french.AppDescription=Outil complet de maintenance système Windows avec analyse disque, nettoyage et sécurité.
