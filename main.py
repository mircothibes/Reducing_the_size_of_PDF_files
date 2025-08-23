import shutil, subprocess
from pathlib import Path

INPUT = Path("input/file_name.pdf")  
OUTPUT   = Path("output/result.pdf")
OUTPUT .parent.mkdir(exist_ok=True)

def _gs_exe():
    return shutil.which("gs") or shutil.which("gswin64c") or shutil.which("gswin32c")

def _run_gs(src: Path, dst: Path, profile="/ebook", color_dpi=150, gray_dpi=150, mono_dpi=300):
    exe = _gs_exe()
    if not exe:
        raise RuntimeError("Ghostscript not found. Install the Ghostscript and try it again.")
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
        raise SystemExit(f"File not found: {INPUT}")

    before = _mb(INPUT)

    # 1) try moderate (/ebook, ~150 dpi)
    _run_gs(INPUT, OUTPUT, profile="/ebook", color_dpi=150)
    after = _mb(OUTPUT)

    # 2) if it reduced < 10%, try harder (/screen, ~100 dpi)
    if before >= after * 0.90:
        _run_gs(INPUT, OUTPUT, profile="/screen", color_dpi=100, gray_dpi=100)
        depois = _mb(OUTPUT)

    print(f"{INPUT.name}: {before:.2f} MB -> {after:.2f} MB  (reduction {(1 - after/before)*100:.1f}%)")
    print(f"Final file: {OUTPUT}")








