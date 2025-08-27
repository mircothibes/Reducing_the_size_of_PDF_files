"""
PDF Size Reducer (Tkinter GUI)

This script provides a graphical interface (built with Tkinter) to reduce the size
of PDF files using Ghostscript. The user can choose a folder, select a PDF, adjust
compression settings, and save the optimized result.

✨ Features:
- Friendly GUI for selecting input/output PDF files
- Ghostscript integration for compression
- Support for Ghostscript profiles: /screen, /ebook, /printer, /prepress
- Adjustable DPI resolution for color/gray and monochrome images
- Aggressive fallback: if the reduction is below a threshold, rerun with stronger settings
- Progress feedback and before/after file size comparison

⚡ Requirements:
- Python 3.9+
- Tkinter (comes with standard Python installation)
- Ghostscript installed and available in PATH

Typical Usage:
--------------
1. Run: `python main.py`
2. Select input folder and PDF.
3. Adjust profile/DPI if necessary.
4. Click "Compress".
5. The reduced PDF will be saved in the output folder.
"""

import shutil
import subprocess
from pathlib import Path
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# -----------------------
# Ghostscript helpers
# -----------------------
def _gs_exe():
    """
    Detect Ghostscript executable on the system.

    Returns
    -------
    str or None
        Path to the Ghostscript executable, or None if not found.
    """
    return shutil.which("gs") or shutil.which("gswin64c") or shutil.which("gswin32c")

def _run_gs(src: Path, dst: Path, profile="/ebook", color_dpi=150, gray_dpi=150, mono_dpi=300, quiet=True):
    """
    Run Ghostscript to compress a PDF file.

    Parameters
    ----------
    src : Path
        Path to the input PDF.
    dst : Path
        Path to the output PDF.
    profile : str, optional
        Ghostscript profile (/screen, /ebook, /printer, /prepress).
    color_dpi : int, optional
        DPI resolution for color images.
    gray_dpi : int, optional
        DPI resolution for grayscale images.
    mono_dpi : int, optional
        DPI resolution for monochrome images.
    quiet : bool, optional
        If True, suppress Ghostscript output.
    """
    exe = _gs_exe()
    if not exe:
        raise RuntimeError("Ghostscript not found. Install Ghostscript and ensure it is in PATH.")
    dst.parent.mkdir(parents=True, exist_ok=True)
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
        "-dNOPAUSE", "-dBATCH",
        f"-sOutputFile={str(dst)}",
        str(src)
    ]
    if quiet:
        cmd.insert(-2, "-dQUIET")  # antes do -dBATCH
    subprocess.run(cmd, check=True)

def _mb(p: Path) -> float:
    """
    Calculate file size in MB.

    Parameters
    ----------
    p : Path
        Path to the file.

    Returns
    -------
    float
        File size in megabytes.
    """
    return p.stat().st_size / (1024*1024)

# -----------------------
# GUI
# -----------------------
class App(tk.Tk):
    """
    Tkinter-based GUI application for PDF compression.

    Attributes
    ----------
    selected_dir : StringVar
        Folder containing input PDFs.
    selected_file : StringVar
        Path to the selected input PDF.
    output_path : StringVar
        Path to the output compressed PDF.
    profile : StringVar
        Ghostscript profile.
    dpi : IntVar
        DPI for color/gray images.
    mono_dpi : IntVar
        DPI for monochrome images.
    aggressive : BooleanVar
        Enable aggressive fallback compression.
    aggr_profile : StringVar
        Profile for aggressive fallback.
    aggr_dpi : IntVar
        DPI for aggressive fallback.
    min_gain : DoubleVar
        Minimum percentage gain required before triggering fallback.
    status : StringVar
        Current status text displayed at the bottom of the GUI.
    """
    def __init__(self):
        """
        Initialize the main application window and variables.
        """
        super().__init__()
        self.title("PDF Size Reducer — Ghostscript")
        self.geometry("640x360")
        self.minsize(640, 360)

        self.selected_dir = tk.StringVar(value=str(Path.cwd() / "input"))
        self.selected_file = tk.StringVar(value="")
        self.output_path = tk.StringVar(value=str(Path.cwd() / "output" / "result.pdf"))

        self.profile = tk.StringVar(value="/ebook")
        self.dpi = tk.IntVar(value=150)
        self.mono_dpi = tk.IntVar(value=300)
        self.aggressive = tk.BooleanVar(value=True)
        self.aggr_profile = tk.StringVar(value="/screen")
        self.aggr_dpi = tk.IntVar(value=100)
        self.min_gain = tk.DoubleVar(value=10.0)

        self.status = tk.StringVar(value="Ready.")
        self._build_ui()

    def _build_ui(self):
        """
        Build the Tkinter GUI layout: input/output selectors, options, and buttons.
        """
        pad = {"padx": 8, "pady": 6}

        # Folder row
        row1 = ttk.Frame(self)
        row1.pack(fill="x", **pad)
        ttk.Label(row1, text="Folder:").pack(side="left")
        ttk.Entry(row1, textvariable=self.selected_dir).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(row1, text="Choose Folder…", command=self.choose_folder).pack(side="left")

        # File row
        row2 = ttk.Frame(self)
        row2.pack(fill="x", **pad)
        ttk.Label(row2, text="Input PDF:").pack(side="left")
        ttk.Entry(row2, textvariable=self.selected_file).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(row2, text="Choose PDF…", command=self.choose_pdf).pack(side="left")

        # Output row
        row3 = ttk.Frame(self)
        row3.pack(fill="x", **pad)
        ttk.Label(row3, text="Output file:").pack(side="left")
        ttk.Entry(row3, textvariable=self.output_path).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(row3, text="Save as…", command=self.choose_output).pack(side="left")

        # Options row
        row4 = ttk.Labelframe(self, text="Options")
        row4.pack(fill="x", **pad)

        ttk.Label(row4, text="Profile:").grid(row=0, column=0, sticky="w", padx=6, pady=4)
        cb = ttk.Combobox(row4, textvariable=self.profile, values=["/screen", "/ebook", "/printer", "/prepress"], state="readonly", width=12)
        cb.grid(row=0, column=1, sticky="w")

        ttk.Label(row4, text="DPI (color/gray):").grid(row=0, column=2, sticky="e", padx=(16,6))
        sp_dpi = ttk.Spinbox(row4, from_=50, to=600, textvariable=self.dpi, width=6)
        sp_dpi.grid(row=0, column=3, sticky="w")

        ttk.Label(row4, text="DPI (mono):").grid(row=0, column=4, sticky="e", padx=(16,6))
        sp_mono = ttk.Spinbox(row4, from_=100, to=1200, textvariable=self.mono_dpi, width=6)
        sp_mono.grid(row=0, column=5, sticky="w")

        # Aggressive
        chk = ttk.Checkbutton(row4, text="Aggressive fallback if reduction < (%)", variable=self.aggressive)
        chk.grid(row=1, column=0, columnspan=2, sticky="w", pady=(6,0))

        sp_min = ttk.Spinbox(row4, from_=0, to=100, increment=1, textvariable=self.min_gain, width=6)
        sp_min.grid(row=1, column=2, sticky="w", pady=(6,0))

        ttk.Label(row4, text="Aggressive profile:").grid(row=1, column=3, sticky="e", padx=(16,6), pady=(6,0))
        cb2 = ttk.Combobox(row4, textvariable=self.aggr_profile, values=["/screen", "/ebook", "/printer", "/prepress"], state="readonly", width=12)
        cb2.grid(row=1, column=4, sticky="w", pady=(6,0))

        ttk.Label(row4, text="Aggressive DPI:").grid(row=1, column=5, sticky="e", padx=(16,6), pady=(6,0))
        sp_agdpi = ttk.Spinbox(row4, from_=50, to=600, textvariable=self.aggr_dpi, width=6)
        sp_agdpi.grid(row=1, column=6, sticky="w", pady=(6,0))

        for i in range(7):
            row4.grid_columnconfigure(i, weight=1)

        # Action row
        row5 = ttk.Frame(self)
        row5.pack(fill="x", **pad)
        ttk.Button(row5, text="Compress", command=self.on_compress).pack(side="right")
        ttk.Button(row5, text="Exit", command=self.destroy).pack(side="right", padx=(0,6))

        # Status
        bar = ttk.Frame(self)
        bar.pack(fill="x", side="bottom")
        ttk.Label(bar, textvariable=self.status, anchor="w").pack(fill="x", padx=8, pady=6)

    def choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self.selected_dir.get() or str(Path.cwd()))
        if folder:
            self.selected_dir.set(folder)

    def choose_pdf(self):
        init = self.selected_dir.get() or str(Path.cwd())
        file = filedialog.askopenfilename(
            initialdir=init,
            title="Select PDF",
            filetypes=[("PDF files", "*.pdf")],
        )
        if file:
            self.selected_file.set(file)
            # se saída não definida, sugere output/result_<nome>.pdf
            out_dir = Path.cwd() / "output"
            out_name = f"{Path(file).stem}_reduced.pdf"
            self.output_path.set(str(out_dir / out_name))

    def choose_output(self):
        initdir = str(Path(self.output_path.get()).parent) if self.output_path.get() else str(Path.cwd() / "output")
        file = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialdir=initdir,
            initialfile=Path(self.output_path.get()).name if self.output_path.get() else "result.pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save compressed PDF as…",
        )
        if file:
            self.output_path.set(file)

    def on_compress(self):
        src = Path(self.selected_file.get())
        if not src.exists():
            messagebox.showerror("Error", "Please choose a valid input PDF.")
            return

        dst = Path(self.output_path.get() or (Path.cwd() / "output" / "result.pdf"))
        prof = self.profile.get()
        dpi = int(self.dpi.get())
        mono = int(self.mono_dpi.get())
        aggr = bool(self.aggressive.get())
        aggr_prof = self.aggr_profile.get()
        aggr_dpi = int(self.aggr_dpi.get())
        min_gain = float(self.min_gain.get())

        self.status.set("Compressing…")
        self._disable()

        # rodar em thread para não travar a UI
        th = threading.Thread(
            target=self._do_compress,
            args=(src, dst, prof, dpi, mono, aggr, aggr_prof, aggr_dpi, min_gain),
            daemon=True
        )
        th.start()

    def _do_compress(self, src, dst, prof, dpi, mono, aggr, aggr_prof, aggr_dpi, min_gain):
        try:
            before = _mb(src)
            self._update_status(f"Pass 1: {prof} @ {dpi}dpi…")
            _run_gs(src, dst, profile=prof, color_dpi=dpi, gray_dpi=dpi, mono_dpi=mono)
            after = _mb(dst)

            used_prof = prof
            # fallback agressivo se ganho < min_gain
            min_factor = 1 - (min_gain / 100.0)
            if aggr and after >= before * min_factor:
                self._update_status(f"Pass 2 (aggressive): {aggr_prof} @ {aggr_dpi}dpi…")
                _run_gs(src, dst, profile=aggr_prof, color_dpi=aggr_dpi, gray_dpi=aggr_dpi, mono_dpi=mono)
                after = _mb(dst)
                used_prof = aggr_prof

            reduction = (1 - after / before) * 100 if before > 0 else 0.0
            msg = (f"{src.name}: {before:.2f} → {after:.2f} MB  "
                   f"(reduction {reduction:.1f}%)  [profile: {used_prof}]\n"
                   f"Saved to: {dst}")
            self._update_status("Done.")
            self._enable()
            messagebox.showinfo("Success", msg)
        except subprocess.CalledProcessError as e:
            self._update_status("Error.")
            self._enable()
            messagebox.showerror("Ghostscript error", f"Ghostscript failed.\n\n{e}")
        except RuntimeError as e:
            self._update_status("Error.")
            self._enable()
            messagebox.showerror("Ghostscript not found", str(e))
        except Exception as e:
            self._update_status("Error.")
            self._enable()
            messagebox.showerror("Unexpected error", repr(e))

    def _update_status(self, text):
        self.status.set(text)

    def _disable(self):
        for child in self.winfo_children():
            try:
                child.configure(state="disabled")
            except tk.TclError:
                pass

    def _enable(self):
        for child in self.winfo_children():
            try:
                child.configure(state="normal")
            except tk.TclError:
                pass

if __name__ == "__main__":
    app = App()
    app.mainloop()








