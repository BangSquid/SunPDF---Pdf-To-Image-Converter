import os
from pdf2image import convert_from_path
import tkinter as tk
from tkinter import filedialog
import subprocess
from pdf2image import pdfinfo_from_path

# DPI Options
dpi_options = {
    "1": 72,
    "2": 96,
    "3": 150,
    "4": 300,
    "5": 600,
    "6": 1200
}

# Format Options
format_options = {
    "1": "JPEG",
    "2": "PNG",
    "3": "TIFF"
}

print("===== PDF → IMAGE Converter =====\n")

# STEP 1: FILE PICKER
print("📄 Pilih file PDF yang mau di-convert...\n")
root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
    title="Pilih PDF",
    filetypes=[("PDF files", "*.pdf")]
)

root.destroy()  # <===== FIX supaya CMD ga auto close

if not file_path:
    print("❌ Tidak ada file dipilih. Keluar...")
    input("\nTekan ENTER untuk keluar...")
    exit()

print(f"\n✔️ File terpilih: {os.path.basename(file_path)}\n")

# 🔍 SMART DETECTION
print("🔍 Analisa PDF...")

pdf_info = pdfinfo_from_path(file_path)

detected_dpi = 0
pdf_type = "Vector"

for key, value in pdf_info.items():
    if "dpi" in key.lower():
        detected_dpi = int(value)
        pdf_type = "Raster"
        break

# Display Smart Result
print(f"➡️ Tipe PDF: {pdf_type}")

if pdf_type == "Raster":
    print(f"➡️ Detected Source Resolution: {detected_dpi} DPI")

    # Generate Recommendation
    if detected_dpi <= 96:
        suggestion = "Disarankan export max 96–150 DPI (lebih tinggi bakal blur)."
    elif detected_dpi <= 150:
        suggestion = "Export 150–300 DPI masih oke."
    elif detected_dpi <= 300:
        suggestion = "300 DPI recommended untuk printing."
    else:
        suggestion = "File sudah high resolution. 300–600 DPI aman."
else:
    suggestion = "PDF Vector → kualitas unlimited. 300–600 DPI recommended."

print(f"📌 Saran: {suggestion}\n")

# STEP 2: FORMAT CHOICE
print("Pilih format output:")
print("""
1. JPEG (Kecil, universal)
2. PNG (Kualitas tinggi)
3. TIFF (Printing profesional)
""")

format_choice = input("Masukkan pilihan (1-3): ")

if format_choice not in format_options:
    print("\n⚠️ Format nggak valid → default: JPEG.")
    output_format = "JPEG"
else:
    output_format = format_options[format_choice]

print(f"\n📌 Format dipilih: {output_format}\n")

# STEP 3: DPI CHOICE (with smart suggestions)
print("Pilih kualitas DPI:")
print("""
1. 72 DPI
2. 96 DPI   {}
3. 150 DPI
4. 300 DPI  {}
5. 600 DPI  {}
6. 1200 DPI {}
""".format(
    "(Recommended)" if pdf_type == "Raster" and detected_dpi <= 96 else "",
    "(Recommended)" if pdf_type == "Vector" or detected_dpi >= 150 else "",
    "(Overkill)" if pdf_type == "Raster" and detected_dpi < 300 else "",
    "(Overkill)" if pdf_type == "Raster" else ""
))

dpi_choice = input("Masukkan pilihan (1-6): ")

if dpi_choice not in dpi_options:
    print("\n⚠️ DPI invalid → set default: 300 DPI.")
    DPI = 300
else:
    DPI = dpi_options[dpi_choice]

print(f"\n📌 DPI terpilih: {DPI}\n")
root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
    title="Pilih PDF",
    filetypes=[("PDF files", "*.pdf")]
)

# STEP 4: PROCESS & SAVE
output_folder = f"output_{output_format.lower()}"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

print(f"▶️ Converting... {os.path.basename(file_path)}\n")

pages = convert_from_path(file_path, DPI)
base_name = os.path.splitext(os.path.basename(file_path))[0]

for i, page in enumerate(pages):
    filename = f"{base_name}_page_{i+1}_{DPI}dpi.{output_format.lower()}"
    save_path = os.path.join(output_folder, filename)
    page.save(save_path, output_format)
    print(f"✔️ Saved → {filename}")

print(f"\n🎉 Conversion selesai!\n📂 Folder hasil: {output_folder}")

# Auto open folder
subprocess.Popen(f'explorer "{os.path.abspath(output_folder)}"')

input("\nTekan ENTER buat keluar...")
