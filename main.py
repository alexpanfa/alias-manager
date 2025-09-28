import customtkinter as ctk
import os
import subprocess

#impostazioni tema di customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#percorso del file .bashrc
BASHRC_PATH = os.path.expanduser("~/.bashrc")

#funzione per aggiunta alias
def aggiunta_alias():
    comando = entry_comando.get().strip()
    alias = entry_alias.get().strip()

    if not comando or not alias:
        label_status.configure(text = "Inserisci sia il comando che l'alias", text_color="red")
        return

    riga = f"alias {alias}='{comando}'\n"

    try:
        with open(BASHRC_PATH, "a") as f:
            f.write(riga)
        label_status.configure(text=f"Alias '{alias}' Aggiunto correttamente", text_color="green")
    except Exception as e:
        label_status.configure(text=f"Errore: {e}", text_color="red")


#funzione per la ricarica della bash a comando inserito
def ricarica_bash():
    try:
        #lancia un nuovo processo che esegue il source
        subprocess.run(f"bash -c 'source {BASHRC_PATH}'", shell=True, check=True)
        label_status.configure(text=".bashrc ricaricato", text_color="green")
    except subprocess.CalledProcessError as e:
        label_status.configure(text=f"Errore nel ricaricare: {e}", text_color="red")


#finestra principale
app = ctk.CTk()
app.title("Alias Manager")
app.geometry("400x350")

#input comando originale
label1 = ctk.CTkLabel(app, text="Comando originale (es. mkdir):")
label1.pack(pady=5)
entry_comando = ctk.CTkEntry(app, width=300)
entry_comando.pack(pady=5)

#input alias
label2 = ctk.CTkLabel(app, text="Nuovo alias (es. folder):")
label2.pack(pady=5)
entry_alias = ctk.CTkEntry(app, width=300)
entry_alias.pack(pady=5)

# Frame contenitore per i bottoni
frame_bottoni = ctk.CTkFrame(app, border_width=0, fg_color="transparent")
frame_bottoni.pack(pady=10)  # il frame è centrato nella finestra

# Bottone aggiungi alias
btn_aggiungi = ctk.CTkButton(frame_bottoni, text="➕ Aggiungi Alias", command=aggiunta_alias)
btn_aggiungi.grid(row=0, column=0, padx=10)

# Bottone ricarica bashrc
btn_ricarica = ctk.CTkButton(frame_bottoni, text="🔄 Ricarica .bashrc", command=ricarica_bash)
btn_ricarica.grid(row=0, column=1, padx=10)

#etichetta di stato
label_status = ctk.CTkLabel(app, text="", text_color="white")
label_status.pack(pady=10)

#avvio app
app.mainloop()