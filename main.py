import importlib.util
import subprocess
import sys
import os
import tkinter as tk
from tkinter import messagebox

BASHRC_PATH = os.path.expanduser("~/.bashrc")


# -------------------------------
# Funzioni core
# -------------------------------
def aggiungi_alias(entry_comando, entry_alias, label_status):
    """Aggiunge un alias al file .bashrc"""
    comando = entry_comando.get().strip()
    alias = entry_alias.get().strip()

    if not comando or not alias:
        label_status.config(text="❌ Insert both command and alias", fg="red")
        return

    riga = f"alias {alias}='{comando}'\n"

    try:
        with open(BASHRC_PATH, "a") as f:
            f.write(riga)
        label_status.config(text=f"✅ Alias '{alias}' added successfully!", fg="green")

        #reset entry
        entry_comando.delete(0, tk.END)
        entry_alias.delete(0, tk.END)
    except Exception as e:
        label_status.config(text=f"Error: {e}", fg="red")


def ricarica_bashrc(label_status):
    """Ricarica il file .bashrc"""
    try:
        subprocess.run(f"bash -c 'source {BASHRC_PATH}'", shell=True, check=True)
        label_status.config(text="🔄 .bashrc reloaded!", fg="green")
    except subprocess.CalledProcessError as e:
        label_status.config(text=f"Error reloading: {e}", fg="red")


def start_main_app():
    """Avvia l'app principale"""
    app = tk.Tk()
    app.title("Alias Manager")
    app.geometry("430x270")

    label1 = tk.Label(app, text="Original command (e.g., mkdir):")
    label1.pack(pady=5)
    entry_comando = tk.Entry(app, width=40)
    entry_comando.pack(pady=5)

    label2 = tk.Label(app, text="New alias (e.g., folder):")
    label2.pack(pady=5)
    entry_alias = tk.Entry(app, width=40)
    entry_alias.pack(pady=5)

    frame_bottoni = tk.Frame(app)
    frame_bottoni.pack(pady=10)

    btn_aggiungi = tk.Button(
        frame_bottoni,
        text="➕ Add Alias",
        command=lambda: aggiungi_alias(entry_comando, entry_alias, label_status)
    )
    btn_aggiungi.grid(row=0, column=0, padx=10)

    btn_ricarica = tk.Button(
        frame_bottoni,
        text="🔄 Reload .bashrc",
        command=lambda: ricarica_bashrc(label_status)
    )
    btn_ricarica.grid(row=0, column=1, padx=10)

    label_status = tk.Label(app, text="", fg="black")
    label_status.pack(pady=10)

    app.mainloop()


# -------------------------------
# Bootstrap: controllo tkinter
# -------------------------------
def is_tkinter_installed():
    return importlib.util.find_spec("tkinter") is not None


if not is_tkinter_installed():
    root = tk.Tk()
    root.withdraw()  # nasconde la finestra principale
    messagebox.showerror(
        "Dependency Missing",
        "⚠️ Tkinter is not installed.\n\n"
        "Please install the Tkinter package for your system:\n\n"
        "- Debian/Ubuntu: sudo apt install python3-tk\n"
        "- Fedora: sudo dnf install python3-tkinter\n"
        "- Arch: sudo pacman -S tk\n"
        "- Windows: included in standard Python installer\n"
        "- macOS: included in system Python\n"
    )
    sys.exit(1)
else:
    start_main_app()
