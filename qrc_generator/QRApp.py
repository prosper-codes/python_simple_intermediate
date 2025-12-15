"""
Enhanced QR Code Generator App (Tkinter)
Uses: pyqrcode + pypng + Pillow

Features:
- Enter text/URL and generate a QR code
- Preview inside the app with better quality
- Save as PNG with custom filename
- Configurable scale, border, and error correction
- Copy to clipboard (platform-specific)
- Keyboard shortcuts for common actions
- Better error handling and user feedback

Dependencies:
    pip install pyqrcode pypng pillow
    # Optional for Windows clipboard: pip install pywin32

Run:
    python qr_generator.py
"""
import io
import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import pyqrcode
from PIL import Image, ImageTk


class QRApp(tk.Tk):
    """Main QR Code Generator Application"""

    def __init__(self):
        super().__init__()
        self.title("QR Code Generator")
        self.geometry("580x500")
        self.resizable(False, False)

        # Store references to prevent garbage collection
        self.qr_image = None
        self.tk_image = None

        self._build_ui()
        self._bind_shortcuts()

    def _build_ui(self):
        """Build the user interface"""
        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input section
        self._create_input_section(main_frame)

        # Options section
        self._create_options_section(main_frame)

        # Generate button
        gen_btn = ttk.Button(
            main_frame,
            text="Generate QR Code",
            command=self.generate_qr,
            width=20
        )
        gen_btn.grid(row=3, column=0, columnspan=4, pady=(12, 8))

        # Preview canvas
        self.canvas = ttk.Label(
            main_frame,
            relief=tk.SUNKEN,
            background='white',
            text="QR Code preview will appear here"
        )
        self.canvas.grid(row=4, column=0, columnspan=4, pady=(8, 8))

        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            foreground='gray'
        )
        status_label.grid(row=5, column=0, columnspan=4, pady=(4, 8))

        # Action buttons
        self._create_action_buttons(main_frame)

        # Help text
        self._create_help_section(main_frame)

    def _create_input_section(self, parent):
        """Create the text input section"""
        ttk.Label(parent, text="Text / URL:").grid(
            row=0, column=0, sticky=tk.W, pady=(0, 8)
        )

        self.text_var = tk.StringVar()
        txt = ttk.Entry(parent, textvariable=self.text_var, width=60)
        txt.grid(row=0, column=1, columnspan=3,
                 sticky=(tk.W, tk.E), pady=(0, 8))
        txt.focus()

    def _create_options_section(self, parent):
        """Create the options section"""
        options_frame = ttk.LabelFrame(parent, text="Options", padding=10)
        options_frame.grid(row=1, column=0, columnspan=4,
                           sticky=(tk.W, tk.E), pady=(0, 8))

        # Scale option
        ttk.Label(options_frame, text="Scale (pixels/module):").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 8)
        )
        self.scale_var = tk.IntVar(value=8)
        scale_spin = ttk.Spinbox(
            options_frame,
            from_=2,
            to=20,
            textvariable=self.scale_var,
            width=8
        )
        scale_spin.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))

        # Border option
        ttk.Label(options_frame, text="Border (modules):").grid(
            row=0, column=2, sticky=tk.W, padx=(0, 8)
        )
        self.border_var = tk.IntVar(value=4)
        border_spin = ttk.Spinbox(
            options_frame,
            from_=0,
            to=10,
            textvariable=self.border_var,
            width=8
        )
        border_spin.grid(row=0, column=3, sticky=tk.W)

        # Error correction option
        ttk.Label(options_frame, text="Error Correction:").grid(
            row=1, column=0, sticky=tk.W, padx=(0, 8), pady=(8, 0)
        )
        self.error_var = tk.StringVar(value='M')
        error_combo = ttk.Combobox(
            options_frame,
            textvariable=self.error_var,
            values=['L (7%)', 'M (15%)', 'Q (25%)', 'H (30%)'],
            width=12,
            state='readonly'
        )
        error_combo.grid(row=1, column=1, sticky=tk.W, pady=(8, 0))
        error_combo.set('M (15%)')

    def _create_action_buttons(self, parent):
        """Create action buttons"""
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=6, column=0, columnspan=4, pady=(8, 0))

        save_btn = ttk.Button(
            btn_frame,
            text="Save PNG (Ctrl+S)",
            command=self.save_png,
            width=18
        )
        save_btn.pack(side=tk.LEFT, padx=(0, 10))

        copy_btn = ttk.Button(
            btn_frame,
            text="Copy to Clipboard (Ctrl+C)",
            command=self.copy_to_clipboard,
            width=24
        )
        copy_btn.pack(side=tk.LEFT)

    def _create_help_section(self, parent):
        """Create help text section"""
        help_frame = ttk.Frame(parent)
        help_frame.grid(row=7, column=0, columnspan=4, pady=(12, 0))

        help_text = ttk.Label(
            help_frame,
            text="💡 Tip: Paste long text or URLs and click Generate (or press Ctrl+G)",
            foreground='#666'
        )
        help_text.pack()

        help_text2 = ttk.Label(
            help_frame,
            text="For SVG output, use: pyqrcode.create(data).svg(filename)",
            foreground='#888',
            font=('TkDefaultFont', 8)
        )
        help_text2.pack()

    def _bind_shortcuts(self):
        """Bind keyboard shortcuts"""
        self.bind('<Control-g>', lambda e: self.generate_qr())
        self.bind('<Control-G>', lambda e: self.generate_qr())
        self.bind('<Control-s>', lambda e: self.save_png())
        self.bind('<Control-S>', lambda e: self.save_png())
        self.bind('<Control-c>', lambda e: self.copy_to_clipboard())
        self.bind('<Control-C>', lambda e: self.copy_to_clipboard())
        self.bind('<Return>', lambda e: self.generate_qr())

    def generate_qr(self):
        """Generate QR code from input text"""
        data = self.text_var.get().strip()

        if not data:
            self.status_var.set("⚠️ Please enter text or URL to encode")
            messagebox.showinfo(
                "No Data", "Please enter text or URL to encode.")
            return

        try:
            # Validate and get parameters
            scale = max(1, int(self.scale_var.get()))
            border = max(0, int(self.border_var.get()))
            error_level = self.error_var.get()[0]  # Get 'L', 'M', 'Q', or 'H'

            self.status_var.set("🔄 Generating QR code...")
            self.update_idletasks()

            # Create QR code
            qr = pyqrcode.create(data, error=error_level)

            # Render to PNG in memory
            buf = io.BytesIO()
            qr.png(
                buf,
                scale=scale,
                module_color=[0, 0, 0, 255],
                background=[255, 255, 255, 255],
                quiet_zone=border
            )
            buf.seek(0)

            # Load as PIL image
            pil_img = Image.open(buf).convert('RGBA')

            # Store reference and display
            self.qr_image = pil_img
            self._show_image(pil_img)

            # Update status
            size = f"{pil_img.width}×{pil_img.height}"
            self.status_var.set(
                f"✅ QR code generated successfully ({size} pixels)")

        except ValueError as e:
            error_msg = f"Invalid parameter value: {e}"
            self.status_var.set("❌ Generation failed")
            messagebox.showerror("Invalid Input", error_msg)

        except Exception as e:
            error_msg = f"Failed to generate QR code:\n{type(e).__name__}: {e}"
            self.status_var.set("❌ Generation failed")
            messagebox.showerror("Error", error_msg)

    def _show_image(self, pil_img):
        """Display QR code image in preview canvas"""
        # Calculate preview size
        max_w, max_h = 450, 300
        w, h = pil_img.size
        scale = min(max_w / w, max_h / h, 1.0)

        if scale < 1.0:
            # Resize for preview (use NEAREST to keep QR code sharp)
            new_size = (int(w * scale), int(h * scale))
            display_img = pil_img.resize(new_size, Image.NEAREST)
        else:
            display_img = pil_img

        # Update canvas
        self.tk_image = ImageTk.PhotoImage(display_img)
        self.canvas.config(image=self.tk_image, text="")

    def save_png(self):
        """Save QR code as PNG file"""
        if self.qr_image is None:
            self.status_var.set("⚠️ Generate a QR code first")
            messagebox.showinfo("No Image", "Generate a QR code first.")
            return

        # Open save dialog
        path = filedialog.asksaveasfilename(
            defaultextension='.png',
            filetypes=[
                ('PNG files', '*.png'),
                ('All files', '*.*')
            ],
            title="Save QR Code"
        )

        if not path:
            return

        try:
            self.qr_image.save(path, format='PNG')
            filename = os.path.basename(path)
            self.status_var.set(f"💾 Saved: {filename}")
            messagebox.showinfo("Saved", f"QR code saved to:\n{path}")

        except PermissionError:
            self.status_var.set("❌ Permission denied")
            messagebox.showerror("Permission Denied",
                                 "Cannot write to the selected location.")

        except Exception as e:
            error_msg = f"Failed to save PNG:\n{type(e).__name__}: {e}"
            self.status_var.set("❌ Save failed")
            messagebox.showerror("Error", error_msg)

    def copy_to_clipboard(self):
        """Copy QR code image to clipboard (platform-specific)"""
        if self.qr_image is None:
            self.status_var.set("⚠️ Generate a QR code first")
            messagebox.showinfo("No Image", "Generate a QR code first.")
            return

        try:
            if sys.platform.startswith('darwin'):
                self._copy_to_clipboard_macos()
            elif sys.platform.startswith('win'):
                self._copy_to_clipboard_windows()
            else:
                self._copy_to_clipboard_linux()

        except ImportError as e:
            msg = f"Missing required package: {e}\n\nFor Windows: pip install pywin32"
            self.status_var.set("❌ Copy failed - missing package")
            messagebox.showwarning("Package Required", msg)

        except Exception as e:
            error_msg = f"Failed to copy to clipboard:\n{type(e).__name__}: {e}"
            self.status_var.set("❌ Copy failed")
            messagebox.showerror("Error", error_msg)

    def _copy_to_clipboard_macos(self):
        """Copy to clipboard on macOS"""
        buf = io.BytesIO()
        self.qr_image.save(buf, format='PNG')
        buf.seek(0)

        p = os.popen('pbcopy', 'wb')
        p.write(buf.read())
        p.close()

        self.status_var.set("📋 Copied to clipboard (macOS)")
        messagebox.showinfo('Copied', 'QR code image copied to clipboard.')

    def _copy_to_clipboard_windows(self):
        """Copy to clipboard on Windows"""
        import win32clipboard

        output = io.BytesIO()
        self.qr_image.convert('RGB').save(output, format='BMP')
        data = output.getvalue()[14:]  # Skip BMP file header

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

        self.status_var.set("📋 Copied to clipboard (Windows)")
        messagebox.showinfo('Copied', 'QR code image copied to clipboard.')

    def _copy_to_clipboard_linux(self):
        """Copy to clipboard on Linux"""
        # Try xclip
        buf = io.BytesIO()
        self.qr_image.save(buf, format='PNG')
        buf.seek(0)

        p = os.popen('xclip -selection clipboard -t image/png', 'wb')
        p.write(buf.read())
        p.close()

        self.status_var.set("📋 Copied to clipboard (Linux)")
        messagebox.showinfo('Copied', 'QR code image copied to clipboard.')


def main():
    """Main entry point"""
    try:
        app = QRApp()
        app.mainloop()
    except KeyboardInterrupt:
        print("\nApplication closed by user.")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
