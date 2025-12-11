"""
Simple QR Code Generator App (Tkinter)
Uses: pyqrcode + pypng + Pillow

Features:
- Enter text/URL and generate a QR code
- Preview inside the app
- Save as PNG with custom filename
- Option to set scale (size) and border

Dependencies:
    pip install pyqrcode pypng pillow

Run:
    python qr_generator.py

"""
import io
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import pyqrcode
from PIL import Image, ImageTk


class QRApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QR Code Generator")
        self.geometry("520x420")
        self.resizable(False, False)

        self._build_ui()
        self.qr_image = None

    def _build_ui(self):
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frm, text="Text / URL:").grid(row=0, column=0, sticky=tk.W)
        self.text_var = tk.StringVar()
        txt = ttk.Entry(frm, textvariable=self.text_var, width=54)
        txt.grid(row=0, column=1, columnspan=3, sticky=tk.W, pady=6)
        txt.focus()

        ttk.Label(frm, text="Scale (pixels per module):").grid(
            row=1, column=0, sticky=tk.W)
        self.scale_var = tk.IntVar(value=8)
        scale_spin = ttk.Spinbox(
            frm, from_=2, to=20, textvariable=self.scale_var, width=6)
        scale_spin.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(frm, text="Border (modules):").grid(
            row=1, column=2, sticky=tk.W)
        self.border_var = tk.IntVar(value=4)
        border_spin = ttk.Spinbox(
            frm, from_=0, to=10, textvariable=self.border_var, width=6)
        border_spin.grid(row=1, column=3, sticky=tk.W)

        gen_btn = ttk.Button(frm, text="Generate", command=self.generate_qr)
        gen_btn.grid(row=2, column=0, columnspan=4, pady=(10, 6))

        self.canvas = ttk.Label(frm, relief=tk.SUNKEN)
        self.canvas.grid(row=3, column=0, columnspan=4, pady=(6, 6))

        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=4, column=0, columnspan=4, pady=(6, 0))

        save_btn = ttk.Button(btn_frame, text="Save PNG",
                              command=self.save_png)
        save_btn.pack(side=tk.LEFT, padx=(0, 8))

        copy_btn = ttk.Button(
            btn_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_btn.pack(side=tk.LEFT)

        ttk.Label(
            frm, text="Tip: you can paste long text or a URL and click Generate.")
        ttk.Label(frm, text="If you need SVG output use pyqrcode.create(...).svg(...)").grid(
            row=5, column=0, columnspan=4, pady=(8, 0))

    def generate_qr(self):
        data = self.text_var.get().strip()
        if not data:
            messagebox.showinfo(
                "No data", "Please enter text or URL to encode.")
            return

        scale = max(1, int(self.scale_var.get()))
        border = max(0, int(self.border_var.get()))

        try:
            qr = pyqrcode.create(data, error='L')
            buf = io.BytesIO()
            # pyqrcode can write PNG into a file-like object (requires pypng)
            qr.png(buf, scale=scale, module_color=[0, 0, 0, 255], background=[
                   255, 255, 255, 255], quiet_zone=border)
            buf.seek(0)
            pil_img = Image.open(buf).convert('RGBA')

            # Keep a reference to avoid garbage collection in Tkinter
            self.qr_image = pil_img
            self._show_image(pil_img)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code:\n{e}")

    def _show_image(self, pil_img):
        # Resize preview if too large for the preview area
        max_w, max_h = 400, 300
        w, h = pil_img.size
        scale = min(max_w / w, max_h / h, 1.0)
        if scale < 1.0:
            display_img = pil_img.resize(
                (int(w * scale), int(h * scale)), Image.NEAREST)
        else:
            display_img = pil_img

        self.tk_image = ImageTk.PhotoImage(display_img)
        self.canvas.config(image=self.tk_image)

    def save_png(self):
        if self.qr_image is None:
            messagebox.showinfo("No image", "Generate a QR code first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension='.png', filetypes=[('PNG files', '*.png')])
        if not path:
            return
        try:
            self.qr_image.save(path, format='PNG')
            messagebox.showinfo("Saved", f"Saved PNG to: {path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PNG:\n{e}")

    def copy_to_clipboard(self):
        # Copy PNG bytes to clipboard as image - platform dependent. We'll copy the raw PNG bytes to clipboard if possible.
        if self.qr_image is None:
            messagebox.showinfo("No image", "Generate a QR code first.")
            return
        try:
            import sys
            if sys.platform.startswith('darwin'):
                # macOS: use pbcopy with PNG data
                buf = io.BytesIO()
                self.qr_image.save(buf, format='PNG')
                buf.seek(0)
                p = os.popen('pbcopy', 'wb')
                p.write(buf.read())
                p.close()
                messagebox.showinfo(
                    'Copied', 'Image copied to clipboard (macOS).')
            elif sys.platform.startswith('win'):
                # Windows: use tkinter image clipboard (works for BMP, so convert)
                output = io.BytesIO()
                self.qr_image.convert('RGB').save(output, format='BMP')
                # BMP file header skip for Windows clipboard
                data = output.getvalue()[14:]
                import win32clipboard  # requires pywin32
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                win32clipboard.CloseClipboard()
                messagebox.showinfo(
                    'Copied', 'Image copied to clipboard (Windows).')
            else:
                messagebox.showinfo(
                    'Not supported', 'Copy-to-clipboard not supported on this platform via this app.')
        except Exception:
            messagebox.showinfo(
                'Not supported', 'Copy-to-clipboard not available (missing optional packages).')


if __name__ == '__main__':
    app = QRApp()
    app.mainloop()
