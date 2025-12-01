import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

class AplikaciaSlova:
    def __init__(self, root):
        self.root = root
        self.root.title("Analýza dĺžky slov")
        self.root.geometry("400x500")

        # --- Dátové štruktúry ---
        self.slova = []  # Naše pole slov

        # --- GUI Prvky ---
        
        # 1. Sekcia: Vstup M (inicializácia)
        lbl_m = tk.Label(root, text="Vstup M (počet náhodných slov na úvod):", font=("Arial", 10))
        lbl_m.pack(pady=5)
        
        frame_m = tk.Frame(root)
        frame_m.pack(pady=5)
        
        self.entry_m = tk.Entry(frame_m, width=10)
        self.entry_m.pack(side=tk.LEFT, padx=5)
        self.entry_m.insert(0, "3") # Predvolená hodnota
        
        btn_init = tk.Button(frame_m, text="Generovať M slov", command=self.generuj_m_slov)
        btn_init.pack(side=tk.LEFT)

        tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=10)

        # 2. Sekcia: Pridanie nového slova
        lbl_nove = tk.Label(root, text="Pridať nové slovo:", font=("Arial", 10, "bold"))
        lbl_nove.pack(pady=5)

        self.entry_slovo = tk.Entry(root, width=30)
        self.entry_slovo.pack(pady=5)
        # Umožní pridať slovo stlačením Enteru
        self.entry_slovo.bind('<Return>', lambda event: self.pridaj_slovo())

        btn_pridaj = tk.Button(root, text="Pridať slovo", command=self.pridaj_slovo, bg="#dddddd")
        btn_pridaj.pack(pady=5)

        # 3. Sekcia: Zoznam slov a štatistika
        self.listbox = tk.Listbox(root, height=8, width=40)
        self.listbox.pack(pady=10)

        self.lbl_max_slovo = tk.Label(root, text="Najdlhšie slovo: -", fg="blue", font=("Arial", 11, "bold"))
        self.lbl_max_slovo.pack(pady=10)

        # 4. Sekcia: Graf
        btn_graf = tk.Button(root, text="Vykresliť graf dĺžok", command=self.vykresli_graf, bg="lightblue", height=2)
        btn_graf.pack(fill=tk.X, padx=20, pady=10)

    def generuj_m_slov(self):
        """Vygeneruje M placeholder slov podľa vstupu."""
        try:
            m = int(self.entry_m.get())
            self.slova = [] # Vymazať staré
            self.listbox.delete(0, tk.END)
            
            # Generovanie ukážkových slov (Slovo1, Slovo2...)
            for i in range(1, m + 1):
                slovo = f"Slovo_{i}" + ("x" * i) # Aby mali rôznu dĺžku pre efekt
                self.slova.append(slovo)
                self.listbox.insert(tk.END, f"{slovo} (dĺžka: {len(slovo)})")
            
            self.aktualizuj_max()
        except ValueError:
            messagebox.showerror("Chyba", "Zadajte platné celé číslo pre M.")

    def pridaj_slovo(self):
        """Pridá slovo zo vstupu do poľa."""
        nove_slovo = self.entry_slovo.get().strip()
        
        if nove_slovo:
            self.slova.append(nove_slovo)
            self.listbox.insert(tk.END, f"{nove_slovo} (dĺžka: {len(nove_slovo)})")
            self.entry_slovo.delete(0, tk.END) # Vyčistiť pole
            self.aktualizuj_max()
        else:
            messagebox.showwarning("Upozornenie", "Nemožno pridať prázdne slovo.")

    def aktualizuj_max(self):
        """Nájde slovo s max dĺžkou a vypíše ho."""
        if not self.slova:
            self.lbl_max_slovo.config(text="Najdlhšie slovo: -")
            return

        # Logika hľadania maxima
        najdlhsie = max(self.slova, key=len)
        dlzka = len(najdlhsie)
        self.lbl_max_slovo.config(text=f"Najdlhšie slovo: '{najdlhsie}' ({dlzka} znakov)")

    def vykresli_graf(self):
        """Vykreslí stĺpcový graf pomocou Matplotlib."""
        if not self.slova:
            messagebox.showwarning("Upozornenie", "Žiadne slová na vykreslenie.")
            return

        dlzky = [len(s) for s in self.slova]
        
        # Nastavenie grafu
        plt.figure(figsize=(8, 5))
        bar_colors = ['skyblue' if l != max(dlzky) else 'orange' for l in dlzky] # Najdlhšie zvýrazníme oranžovou
        
        plt.bar(self.slova, dlzky, color=bar_colors)
        plt.xlabel('Slová')
        plt.ylabel('Dĺžka (počet znakov)')
        plt.title('Graf dĺžok slov')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Zobrazenie hodnôt nad stĺpcami
        for i, v in enumerate(dlzky):
            plt.text(i, v + 0.1, str(v), ha='center', fontweight='bold')

        plt.show()

# --- Spustenie aplikácie ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AplikaciaSlova(root)
    root.mainloop()