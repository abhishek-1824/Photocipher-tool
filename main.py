import tkinter as tk
from tkinter import filedialog, messagebox
from encryptor import ImageEncryptor
from PIL import Image, ImageTk
import webbrowser
import urllib.parse
import os

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Cipher Tool")
        self.root.geometry("600x650")

        self.encrypted_files = []  # Keep track of encrypted file paths

        tk.Label(root, text="Image Encryption & Decryption", font=("Italic", 16), bg='black', fg='white').pack(pady=10)

        tk.Label(root, text="Select Image(s):", bg='black', fg='white').pack()
        self.file_path_entry = tk.Entry(root, width=40)
        self.file_path_entry.pack(pady=5)
        tk.Button(root, text="Browse", bg='blue', fg='black', command=self.browse_file).pack(pady=5)

        tk.Label(root, text="Password:", bg='black', fg='white').pack()
        self.password_entry = tk.Entry(root, show="*", width=30)
        self.password_entry.pack(pady=5)

        tk.Label(root, text="Recipient Email:", bg='black', fg='white').pack()
        self.email_entry = tk.Entry(root, width=40)
        self.email_entry.pack(pady=5)

        self.image_label = tk.Label(root, text="Preview", bg='black', fg='white')
        self.image_label.pack(pady=5)

        tk.Button(root, text="Encrypt", bg='orange', fg='black', command=self.encrypt_only).pack(pady=10)
        tk.Button(root, text="Redirect to Gmail with Encrypted File", bg='red', fg='black', command=self.redirect_to_gmail).pack(pady=10)
        tk.Button(root, text="Decrypt", bg='green', fg='black', command=self.decrypt).pack(pady=10)

        tk.Label(root, text="Team 7.", fg="white", bg='black').pack(side="bottom", pady=10)

    def browse_file(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if file_paths:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, ', '.join(file_paths))
            self.preview_image(file_paths[0])

    def preview_image(self, file_path):
        try:
            img = Image.open(file_path)
            img.thumbnail((250, 250))
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk
        except Exception as e:
            messagebox.showerror("Error", f"Unable to load image preview: {str(e)}")

    def encrypt_only(self):
        file_paths = self.file_path_entry.get().split(", ")
        password = self.password_entry.get()

        if not file_paths or not password:
            messagebox.showerror("Error", "Please select files and enter a password.")
            return

        try:
            self.encrypted_files = []
            for file_path in file_paths:
                encrypted_path = ImageEncryptor.encrypt_image(file_path, password)
                if encrypted_path:
                    self.encrypted_files.append(encrypted_path)
            messagebox.showinfo("Success", "Files encrypted successfully!")
            self.password_entry.delete(0, tk.END)
            self.image_label.config(image='')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def redirect_to_gmail(self):
        if not self.encrypted_files:
            messagebox.showerror("Error", "No encrypted file found. Please encrypt a file first.")
            return

        recipient = self.email_entry.get()
        if not recipient:
            messagebox.showerror("Error", "Please enter the recipient's email address.")
            return

        subject = urllib.parse.quote("Encrypted File from Photo Cipher Tool")
        body = urllib.parse.quote("Your file is encrypted. Please attach the following file from your system manually.\n\nEncrypted File Path(s):\n" + "\n".join(self.encrypted_files))
        mailto_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={recipient}&su={subject}&body={body}"

        # Open Gmail in Chrome
        webbrowser.open(mailto_url)
        messagebox.showinfo("Redirected", "Gmail opened in browser.\nPlease attach the encrypted file manually.")

    def decrypt(self):
        file_paths = self.file_path_entry.get().split(", ")
        password = self.password_entry.get()

        if not file_paths or not password:
            messagebox.showerror("Error", "Please select a file and enter the password.")
            return

        try:
            for file_path in file_paths:
                ImageEncryptor.decrypt_image(file_path, password)
            messagebox.showinfo("Success", "Files decrypted successfully!")
            self.password_entry.delete(0, tk.END)
            self.preview_image(file_paths[0])
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
