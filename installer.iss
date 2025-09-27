; ============================================
; PDF Reducer — Inno Setup Installer Script
; ============================================

#define MyAppName "PDF Reducer"
#define MyAppVersion "1.0.0"
#define MyPublisher "Marcos Kemer"
#define MyURL "https://github.com/your-repo"    ; <-- adjust if you want
#define MyExe "PDF-Reducer.exe"
#define MyIcon "pdf_reducer_whitebg.ico"

[Setup]
; Generate a new GUID in Inno: Tools -> Generate GUID
AppId={{6F6E9F2F-3C0C-4B8D-8B72-52A9D75F6B2E}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyPublisher}
AppPublisherURL={#MyURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputBaseFilename=PDF-Reducer-Setup
OutputDir=Output
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile={#MyIcon}
UninstallDisplayIcon={app}\{#MyExe}
ArchitecturesInstallIn64BitMode=x64
; If you prefer per-user (no admin), uncomment:
;PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked
Name: "open_gs_site"; Description: "Open Ghostscript download page after setup"; GroupDescription: "Optional actions:"; Flags: unchecked

[Files]
; Copy your built EXE and icon into the install folder
Source: "dist\PDF-Reducer.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "pdf_reducer_whitebg.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyExe}"; IconFilename: "{app}\{#MyIcon}"
; Desktop (optional via task)
Name: "{userdesktop}\{#MyAppName}"; Filename: "{app}\{#MyExe}"; IconFilename: "{app}\{#MyIcon}"; Tasks: desktopicon

[Run]
; Run the app after install (checked by default)
Filename: "{app}\{#MyExe}"; Description: "Run {#MyAppName} now"; Flags: nowait postinstall skipifsilent
; Open Ghostscript website if user selected the task
Filename: "https://ghostscript.com/releases/"; Flags: postinstall shellexec runasoriginaluser; Tasks: open_gs_site

; No file associations or registry entries are needed for this app.
