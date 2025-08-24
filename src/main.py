import shutil, subprocess, sys
from pathlib import Path

INPUT  = Path("input/file_name.pdf")
OUTPUT = Path("output/result.pdf")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

def _gs_exe() -> str | None:
    # Windows: gswin64c/gswin32c; Linux/macOS: gs
    return shutil.which("gs") or shutil.which("gswin64c") or shutil.which("gswin32c")

def _run_gs(src: Path, dst: Path, profile="/ebook", color_dpi=150, gray_dpi=150, mono_dpi=300):
    exe = _gs_exe()
    if not exe:
        raise RuntimeError(
            "Ghostscript not found. Install Ghostscript and ensure it is in your PATH."
        )
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
    # (Optional) Allow to pass the input file via CLI: python main.py input\doc.pdf
    if len(sys.argv) > 1:
        INPUT = Path(sys.argv[1])
        OUTPUT = Path("output") / "result.pdf"
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    if not INPUT.exists():
        raise SystemExit(f"File not found: {INPUT}")

    before = _mb(INPUT)
    used_profile = "/ebook"

    # 1) try moderate (/ebook, ~150 dpi)
    try:
        _run_gs(INPUT, OUTPUT, profile="/ebook", color_dpi=150)
    except subprocess.CalledProcessError as e:
        raise SystemExit(f"Ghostscript failed on first pass: {e}")
    except RuntimeError as e:
        raise SystemExit(str(e))

    after = _mb(OUTPUT)

    # 2) if it reduced < 10%, try harder (/screen, ~100 dpi)
    if after >= before * 0.90:
        try:
            _run_gs(INPUT, OUTPUT, profile="/screen", color_dpi=100, gray_dpi=100)
            used_profile = "/screen"
            after = _mb(OUTPUT)  # << recalcula depois do fallback
        except subprocess.CalledProcessError as e:
            # maintains the previous result if fallback fails
            pass

    reduction = (1 - after / before) * 100 if before > 0 else 0
    print(f"{INPUT.name}: {before:.2f} MB -> {after:.2f} MB  (reduction {reduction:.1f}%)  [profile: {used_profile}]")
    print(f"Final file: {OUTPUT}")








