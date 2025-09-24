; ============================================
; PDF Reducer — Inno Setup Installer Script
; ============================================

[Setup]
AppName=PDF Reducer
AppVersion=1.0.0
AppPublisher=Marcos Kemer
AppPublisherURL=https://github.com/your-repo   ; <-- adjust to your GitHub
DefaultDirName={pf}\PDF Reducer
DefaultGroupName=PDF Reducer
DisableDirPage=no
DisableProgramGroupPage=no
OutputBaseFilename=PDF-Reducer-Setup
OutputDir=Output
Compression=lzma
SolidCompression=yes
SetupIconFile=pdf_reducer_whitebg.ico
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
UninstallDisplayIcon={app}\PDF-Reducer.exe
AppMutex=PDFReducerMutex

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
; Copy the executable and the icon
Source: "dist\PDF-Reducer.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "pdf_reducer_whitebg.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu shortcut
Name: "{group}\PDF Reducer"; Filename: "{app}\PDF-Reducer.exe"; IconFilename: "{app}\pdf_reducer_whitebg.ico"
; Desktop shortcut (optional, controlled by task)
Name: "{userdesktop}\PDF Reducer"; Filename: "{app}\PDF-Reducer.exe"; IconFilename: "{app}\pdf_reducer_whitebg.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked
Name: "open_gs_site"; Description: "Open Ghostscript download page after setup"; GroupDescription: "Optional actions:"; Flags: unchecked

[Run]
; Run the app after installation (default: checked)
Filename: "{app}\PDF-Reducer.exe"; Description: "Run PDF Reducer now"; Flags: nowait postinstall skipifsilent
; Open Ghostscript website if user checked the option
Filename: "https://ghostscript.com/releases/"; Flags: postinstall shellexec runasoriginaluser; Tasks: open_gs_site

[Code]
; Show a reminder about Ghostscript at the end
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssDone then begin
    MsgBox('Installation finished!' + #13#10 +
           'Reminder: PDF Reducer requires Ghostscript.' + #13#10 +
           'If you do not have it installed, please download it from:' + #13#10 +
           'https://ghostscript.com/releases/',
           mbInformation, MB_OK);
  end;
end;
