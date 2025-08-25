# PDF Size Reducer (GUI)

A simple **Python + Tkinter** tool to compress PDF files using **Ghostscript**.  
Provides a friendly interface to select a folder, choose a PDF, adjust compression settings, and save the optimized file.

---

## ✨ Features
- Graphical interface with **Tkinter**
- Choose input folder and PDF file
- Choose output location
- Select Ghostscript profile (`/screen`, `/ebook`, `/printer`, `/prepress`)
- Adjust **DPI resolution** for images
- Optional **aggressive fallback**: re-runs compression if the first pass reduces less than a threshold
- Displays before/after file size and % reduction
- Works on **Windows, Linux, macOS** (requires Ghostscript installed)

---

## 📂 Project Structure

pdf-size-reducer/
├── main.py # Tkinter GUI script
├── input/ # (optional) put PDFs here
├── output/ # compressed files saved here
└── README.md



