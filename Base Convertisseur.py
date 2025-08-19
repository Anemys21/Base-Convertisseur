import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont

# Supported bases 2-36
BASES = [(2, "Base 2 (binaire)"), (8, "Base 8 (octal)"), (10, "Base 10 (décimal)"), (16, "Base 16 (hexadécimal)")]
ALL_BASES = list(range(2, 37))

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def int_to_base(n: int, base: int) -> str:
    if base < 2 or base > 36:
        raise ValueError("La base doit être entre 2 et 36")
    if n == 0:
        return "0"
    neg = n < 0
    n = abs(n)
    out = []
    while n > 0:
        n, r = divmod(n, base)
        out.append(DIGITS[r])
    s = ("-" if neg else "") + "".join(reversed(out))

def auto_detect(value: str):
    v = value.strip().upper()
    if v.startswith("0B"):
        return v[2:], 2
    if v.startswith("0O"):
        return v[2:], 8
    if v.startswith("0X"):
        return v[2:], 16
    return v, None


class BaseConverterApp(ttk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master, padding=12)
        self.master.title("Convertisseur de bases — Anemys37")
        self.master.geometry("760x460")
        self.master.minsize(640, 420)
        self.master.configure()

        # Styles (dark artistic theme)
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        # Palette
        bg = "#0b1020"        # page background
        card = "#0f1426"      # card background
        border = "#1d2642"
        text = "#eaf2ff"
        muted = "#a5b4d6"
        field_bg = "#0b1228"
        accent = "#38bdf8"
        accent700 = "#0ea5e9"

        self.master.configure(bg=bg)
        self.configure(style="Root.TFrame")

        style.configure("Root.TFrame", background=bg)
        style.configure("TFrame", background=card)
        style.configure("Card.TFrame", background=card, relief="groove", borderwidth=1)
        style.configure("TLabel", background=card, foreground=text, padding=4)
        style.configure("Head.TLabel", background=bg, foreground=text)
        style.configure("Footer.TLabel", background=bg, foreground=muted)
        style.configure("Muted.TLabel", background=card, foreground=muted)
        style.configure(
            "TEntry",
            fieldbackground=field_bg,
            foreground=text,
            padding=4,
            insertcolor=text,
            bordercolor=border,
            lightcolor=border,
            darkcolor=border,
            relief="flat",
        )
        style.configure(
            "RO.TEntry",
            fieldbackground=field_bg,
            foreground=text,
            padding=4,
            relief="flat",
        )
        style.configure(
            "Accent.TButton",
            background=accent,
            foreground="#07111d",
            padding=8,
            focusthickness=0,
            borderwidth=0,
        )
        style.map("Accent.TButton", background=[("pressed", accent700), ("active", accent700)])

        self.grid(column=0, row=0, sticky="nsew")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Header gradient banner
        self.header = tk.Canvas(self, height=120, highlightthickness=0, bd=0, bg=bg)
        self.header.grid(column=0, row=0, sticky="ew")
        self.header.bind("<Configure>", lambda e: self._paint_header(self.header))

        # Top input area
        top = ttk.Frame(self)
        top.grid(column=0, row=1, sticky="ew")
        for i in range(6):
            top.columnconfigure(i, weight=1)

        ttk.Label(top, text="Valeur à convertir:").grid(column=0, row=0, sticky="w")
        self.value_var = tk.StringVar()
        self.entry = ttk.Entry(top, textvariable=self.value_var)
        self.entry.grid(column=0, row=1, columnspan=3, sticky="ew", pady=(0, 6))
        self.entry.insert(0, "0xFF")

        ttk.Label(top, text="Base source:").grid(column=3, row=0, sticky="w", padx=(12, 0))
        self.src_var = tk.StringVar(value="Auto (préfixes 0b/0o/0x)")
        src_values = ["Auto (préfixes 0b/0o/0x)"] + [f"{b}" for b in ALL_BASES]
        self.src_combo = ttk.Combobox(top, textvariable=self.src_var, values=src_values, state="readonly")
        self.src_combo.grid(column=3, row=1, sticky="ew", padx=(12, 0))

        ttk.Label(top, text="Base cible:").grid(column=4, row=0, sticky="w", padx=(12, 0))
        self.dst_var = tk.StringVar(value="10")
        self.dst_combo = ttk.Combobox(top, textvariable=self.dst_var, values=[f"{b}" for b in ALL_BASES], state="readonly")
        self.dst_combo.grid(column=4, row=1, sticky="ew", padx=(12, 0))

        self.btn = ttk.Button(top, text="Convertir", command=self.convert, style="Accent.TButton")
        self.btn.grid(column=5, row=1, sticky="e", padx=(12, 0))

        # Results card
        card = ttk.Frame(self, style="Card.TFrame", padding=12)
        card.grid(column=0, row=2, sticky="nsew", pady=(12, 0))
        self.rowconfigure(1, weight=0)
        card.columnconfigure(0, weight=1)

        # Output fields
        grid = ttk.Frame(card)
        grid.grid(column=0, row=0, sticky="nsew")
        for i in range(2):
            grid.columnconfigure(i, weight=1)

        self.lbl_info = ttk.Label(grid, text="Résultats dans les bases courantes:")
        self.lbl_info.grid(column=0, row=0, columnspan=2, sticky="w")

        self.out_dec = self._add_row(grid, 1, "Décimal (10)")
        self.out_bin = self._add_row(grid, 2, "Binaire (2)")
        self.out_oct = self._add_row(grid, 3, "Octal (8)")
        self.out_hex = self._add_row(grid, 4, "Hexadécimal (16)")

        # Custom output for selected target base
        self.custom_title = ttk.Label(grid, text="Base cible")
        self.custom_title.grid(column=0, row=5, sticky="w", pady=(8, 0))
        self.custom_value = ttk.Entry(grid, style="RO.TEntry")
        self.custom_value.grid(column=1, row=5, sticky="ew", pady=(8, 0))

        # Bindings
        self.entry.bind("<Return>", lambda e: self.convert())
        self.src_combo.bind("<<ComboboxSelected>>", lambda e: self.convert())
        self.dst_combo.bind("<<ComboboxSelected>>", lambda e: self.convert())

        # Footer
        self.footer = ttk.Label(self, text="© 2025 AMOUBE NDE LOUANGE-MYSTERE", style="Footer.TLabel")
        self.footer.grid(column=0, row=3, sticky="ew", pady=(10, 6))

        # Initial computation
        # Schedule conversion after widgets are fully initialized to avoid early Tcl calls
        self.after(0, self.convert)

    def _add_row(self, parent, r, title: str):
        ttk.Label(parent, text=title).grid(column=0, row=r, sticky="w", pady=4)
        ent = ttk.Entry(parent, style="RO.TEntry")
        ent.grid(column=1, row=r, sticky="ew", pady=4)
        ent.configure(state="readonly")
        return ent

    def _set_entry(self, entry: ttk.Entry, text: str):
        entry.configure(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, str(text))
        entry.configure(state="readonly")

    def parse_input(self):
        raw = self.value_var.get().strip()
        if not raw:
            raise ValueError("Veuillez saisir une valeur")

        v, detected = auto_detect(raw)
        # Determine source base
        src_text = self.src_var.get()
        if src_text.startswith("Auto"):
            base_src = detected if detected is not None else 10
        else:
            try:
                base_src = int(src_text)
            except ValueError:
                raise ValueError("Base source invalide")
        # Validate characters
        allowed = set(DIGITS[:base_src] + ("-"))
        if any(ch not in allowed for ch in v):
            raise ValueError(f"Caractère invalide pour la base {base_src}")

        return int(v, base_src)

    def convert(self):
        try:
            n = self.parse_input()
            # Determine target base
            try:
                base_dst = int(self.dst_var.get())
            except ValueError:
                base_dst = 10

            # Fill standard bases
            self._set_entry(self.out_dec, str(n))
            self._set_entry(self.out_bin, int_to_base(n, 2))
            self._set_entry(self.out_oct, int_to_base(n, 8))
            self._set_entry(self.out_hex, int_to_base(n, 16))

            # Custom base
            self.custom_title.configure(text=f"Base cible ({base_dst})")
            self.custom_value.configure(state="normal")
            self.custom_value.delete(0, tk.END)
            self.custom_value.insert(0, str(int_to_base(n, base_dst)))
            self.custom_value.configure(state="readonly")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    # Artistic gradient header painter
    def _paint_header(self, canvas: tk.Canvas):
        canvas.delete("all")
        w = canvas.winfo_width() or 1
        h = canvas.winfo_height() or 1
        # Gradient from accent to deep blue
        c1 = (56, 189, 248)   # #38bdf8
        c2 = (14, 165, 233)   # #0ea5e9
        steps = max(1, h)
        for i in range(steps):
            r = int(c1[0] + (c2[0]-c1[0]) * i/steps)
            g = int(c1[1] + (c2[1]-c1[1]) * i/steps)
            b = int(c1[2] + (c2[2]-c1[2]) * i/steps)
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(0, i, w, i, fill=color)
        # Title text
        title_font = tkfont.Font(family="Poppins", size=18, weight="bold")
        subtitle_font = tkfont.Font(family="Poppins", size=11)
        canvas.create_text(18, h/2 - 8, anchor="w", text="Anemys37 — Convertisseur de bases", fill="#07111d", font=title_font)
        canvas.create_text(18, h/2 + 16, anchor="w", text="Convertissez rapidement entre binaire, octal, décimal, hexadécimal et plus", fill="#082638", font=subtitle_font)


def main():
    root = tk.Tk()
    app = BaseConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
