import numpy as np
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.font import Font

class ImageEncryptor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔒 PixelCrypt - Image Encryption Tool")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2e2e2e")
        
        self.eye_icon = self.create_eye_icon()
        self.original_image = None
        self.encrypted_image = None
        self.decrypted_image = None
        self.key = 42
        
        self.setup_gui()

    def create_eye_icon(self):
        img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((5, 10, 15, 20), fill="white", outline="cyan")
        draw.ellipse((8, 13, 12, 17), fill="black")
        draw.ellipse((17, 10, 27, 20), fill="white", outline="cyan")
        draw.ellipse((20, 13, 24, 17), fill="black")
        return ImageTk.PhotoImage(img)

    def setup_gui(self):
        title_font = Font(family="Helvetica", size=16, weight="bold")
        label_font = Font(family="Arial", size=10, weight="bold")

        header_frame = tk.Frame(self.root, bg="#2e2e2e")
        header_frame.pack(pady=10)
        
        tk.Label(
            header_frame,
            image=self.eye_icon,
            compound=tk.LEFT,
            text="  PixelCrypt  ",
            font=title_font,
            fg="cyan",
            bg="#2e2e2e"
        ).pack(side=tk.LEFT)

        main_frame = tk.Frame(self.root, bg="#2e2e2e")
        main_frame.pack(pady=10)
        
        original_frame = tk.Frame(main_frame, bg="#2e2e2e")
        original_frame.grid(row=0, column=0, padx=10)
        tk.Label(original_frame, text="Original Image", font=label_font, bg="#2e2e2e", fg="white").pack()
        self.original_canvas = tk.Canvas(original_frame, width=300, height=250, bg="#3a3a3a", highlightthickness=0)
        self.original_canvas.pack()

        encrypted_frame = tk.Frame(main_frame, bg="#2e2e2e")
        encrypted_frame.grid(row=0, column=1, padx=10)
        tk.Label(encrypted_frame, text="Encrypted Image", font=label_font, bg="#2e2e2e", fg="white").pack()
        self.encrypted_canvas = tk.Canvas(encrypted_frame, width=300, height=250, bg="#3a3a3a", highlightthickness=0)
        self.encrypted_canvas.pack()

        decrypted_frame = tk.Frame(main_frame, bg="#2e2e2e")
        decrypted_frame.grid(row=0, column=2, padx=10)
        tk.Label(decrypted_frame, text="Decrypted Image", font=label_font, bg="#2e2e2e", fg="white").pack()
        self.decrypted_canvas = tk.Canvas(decrypted_frame, width=300, height=250, bg="#3a3a3a", highlightthickness=0)
        self.decrypted_canvas.pack()

        control_frame = tk.Frame(self.root, bg="#2e2e2e")
        control_frame.pack(pady=20)

        buttons = [
            ("📁 Upload Image", self.load_image, "#3a3a3a"),
            ("📁 Upload Encrypted", self.load_encrypted_image, "#3a3a3a"),
            ("🔑 Key (1-255):", None, "#2e2e2e"),
            ("🔒 Encrypt", self.encrypt_image, "#4CAF50"),
            ("🔓 Decrypt", self.decrypt_image, "#2196F3"),
            ("🔓 Direct Decrypt", self.direct_decrypt_image, "#2196F3"),
            ("🗑️ Clear All", self.clear_all, "#f44336"),
            ("⬇️ Encrypted", self.download_encrypted, "#FF9800"),
            ("⬇️ Decrypted", self.download_decrypted, "#9C27B0")
        ]

        col = 0
        for text, command, bg in buttons:
            if text.startswith("🔑"):
                tk.Label(control_frame, text=text, font=label_font, bg=bg, fg="white").grid(row=0, column=col, padx=5)
                col += 1
                self.key_entry = tk.Entry(control_frame, width=5, bg="#3a3a3a", fg="white", insertbackground="white")
                self.key_entry.grid(row=0, column=col, padx=5)
                self.key_entry.insert(0, str(self.key))
                col += 1
            else:
                tk.Button(
                    control_frame,
                    text=text,
                    command=command,
                    bg=bg,
                    fg="white",
                    relief=tk.FLAT,
                    padx=10
                ).grid(row=0, column=col, padx=5)
                col += 1

        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg="#3a3a3a",
            fg="white"
        ).pack(side=tk.BOTTOM, fill=tk.X)

    def clear_all(self):
        self.original_image = None
        self.encrypted_image = None
        self.decrypted_image = None
        self.original_canvas.delete("all")
        self.encrypted_canvas.delete("all")
        self.decrypted_canvas.delete("all")
        self.key = 42
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, str(self.key))
        self.original_canvas.config(bg="#3a3a3a")
        self.encrypted_canvas.config(bg="#3a3a3a")
        self.decrypted_canvas.config(bg="#3a3a3a")
        self.status_var.set("All cleared and ready")

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.display_image(self.original_image, self.original_canvas)
                self.status_var.set(f"Loaded: {file_path.split('/')[-1]}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")

    def load_encrypted_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            try:
                self.encrypted_image = Image.open(file_path)
                self.display_image(self.encrypted_image, self.encrypted_canvas)
                self.status_var.set(f"Loaded encrypted: {file_path.split('/')[-1]}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load encrypted image: {e}")

    def display_image(self, image, canvas):
        canvas.delete("all")
        img = image.copy()
        img.thumbnail((300, 250))
        photo = ImageTk.PhotoImage(img)
        canvas.image = photo
        canvas.create_image(150, 125, image=photo, anchor=tk.CENTER)

    def get_key(self):
        try:
            key = int(self.key_entry.get())
            if 1 <= key <= 255:
                self.key = key
                return True
            messagebox.showerror("Error", "Key must be between 1 and 255")
            return False
        except ValueError:
            messagebox.showerror("Error", "Key must be an integer")
            return False

    def encrypt_image(self):
        if not self.original_image:
            messagebox.showerror("Error", "Please upload an image first")
            return
        
        if not self.get_key():
            return
        
        try:
            img_array = np.array(self.original_image)
            encrypted_array = img_array ^ self.key
            self.encrypted_image = Image.fromarray(encrypted_array)
            self.display_image(self.encrypted_image, self.encrypted_canvas)
            self.status_var.set("Image encrypted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {e}")

    def decrypt_image(self):
        if not self.encrypted_image:
            messagebox.showerror("Error", "Please encrypt an image first or upload an encrypted image")
            return
        
        if not self.get_key():
            return
        
        try:
            img_array = np.array(self.encrypted_image)
            decrypted_array = img_array ^ self.key
            self.decrypted_image = Image.fromarray(decrypted_array)
            self.display_image(self.decrypted_image, self.decrypted_canvas)
            self.status_var.set("Image decrypted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {e}")

    def direct_decrypt_image(self):
        if not self.encrypted_image:
            messagebox.showerror("Error", "Please upload an encrypted image first")
            return
        
        if not self.get_key():
            return
        
        try:
            img_array = np.array(self.encrypted_image)
            decrypted_array = img_array ^ self.key
            self.decrypted_image = Image.fromarray(decrypted_array)
            self.display_image(self.decrypted_image, self.decrypted_canvas)
            self.status_var.set("Image directly decrypted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Direct decryption failed: {e}")

    def download_encrypted(self):
        if not self.encrypted_image:
            messagebox.showerror("Error", "No encrypted image to download")
            return
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]
        )
        if save_path:
            self.encrypted_image.save(save_path)
            self.status_var.set(f"Encrypted image saved as {save_path.split('/')[-1]}")

    def download_decrypted(self):
        if not self.decrypted_image:
            messagebox.showerror("Error", "No decrypted image to download")
            return
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]
        )
        if save_path:
            self.decrypted_image.save(save_path)
            self.status_var.set(f"Decrypted image saved as {save_path.split('/')[-1]}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ImageEncryptor()
    app.run()