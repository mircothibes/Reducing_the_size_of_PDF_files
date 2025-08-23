import shutil, subprocess
from pathlib import Path

INPUT = Path("entrada/CV_Marcos_Kemer_IT.pdf")  
OUTPUT   = Path("saida/resultado.pdf")
OUTPUT .parent.mkdir(exist_ok=True)

def _gs_exe():
    return shutil.which("gs") or shutil.which("gswin64c") or shutil.which("gswin32c")

def _run_gs(src: Path, dst: Path, profile="/ebook", color_dpi=150, gray_dpi=150, mono_dpi=300):
    exe = _gs_exe()
    if not exe:
        raise RuntimeError("Ghostscript não encontrado. Instale o Ghostscript e tente novamente.")
    cmd = [
        exe, "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={profile}",
        "-dDetectDuplicateImages=true",
        "-dCompressFonts=true",
        "-dSubsetFonts=true",
        "-dColorImageDownsampleType=/Bicubic", f"-dColorImageResolution={color_dpi}",
        "-dGrayImageDownsampleType=/Bicubic",  f"-dGrayImageResolution={gray_dpi}",
        "-dMonoImageDownsampleType=/Subsample", f"-dMonoImageResolution={mono_dpi}",
        "-dNOPAUSE", "-dQUIET", "-dBATCH",
        f"-sOutputFile={str(dst)}",
        str(src)
    ]
    subprocess.run(cmd, check=True)

def _mb(p: Path) -> float:
    return p.stat().st_size / (1024*1024)

if __name__ == "__main__":
    if not INPUT.exists():
        raise SystemExit(f"Arquivo não encontrado: {INPUT}")

    antes = _mb(INPUT)

    # 1) tenta moderado (/ebook, ~150 dpi)
    _run_gs(INPUT, OUTPUT, profile="/ebook", color_dpi=150)
    depois = _mb(OUTPUT)

    # 2) se reduziu < 10%, tenta mais forte (/screen, ~100 dpi)
    if depois >= antes * 0.90:
        _run_gs(INPUT, OUTPUT, profile="/screen", color_dpi=100, gray_dpi=100)
        depois = _mb(OUTPUT)

    print(f"{INPUT.name}: {antes:.2f} MB -> {depois:.2f} MB  (redução {(1 - depois/antes)*100:.1f}%)")
    print(f"Arquivo final: {OUTPUT}")








