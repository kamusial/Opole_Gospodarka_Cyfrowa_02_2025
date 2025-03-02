import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

try:
    from pandastable import Table
except ImportError:
    messagebox.showerror("Błąd", "Brak modułu 'pandastable'. Zainstaluj go komendą:\npip install pandastable")
    exit()

class CSVAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Analyzer")
        self.root.geometry("800x600")

        self.data = None

        # Opcje wczytywania pliku
        self.sep_label = tk.Label(root, text="Separator:")
        self.sep_label.pack()
        self.sep_entry = tk.Entry(root)
        self.sep_entry.insert(0, ",")  # Domyślnie CSV używa przecinka
        self.sep_entry.pack()

        self.comment_label = tk.Label(root, text="Znak komentarza:")
        self.comment_label.pack()
        self.comment_entry = tk.Entry(root)
        self.comment_entry.pack()

        self.encoding_label = tk.Label(root, text="Kodowanie:")
        self.encoding_label.pack()
        self.encoding_entry = tk.Entry(root)
        self.encoding_entry.insert(0, "utf-8")  # Domyślne kodowanie
        self.encoding_entry.pack()

        # Przycisk do wczytania pliku CSV
        self.load_button = tk.Button(root, text="Wczytaj CSV", command=self.load_csv)
        self.load_button.pack(pady=5)

        # Lista rozwijana z kolumnami
        self.column_label = tk.Label(root, text="Wybierz kolumnę:")
        self.column_label.pack()
        self.column_combo = ttk.Combobox(root, state="readonly")
        self.column_combo.pack()

        # Przyciski do analizy i wizualizacji danych
        self.describe_button = tk.Button(root, text="Opis statystyczny", command=self.describe_data)
        self.describe_button.pack(pady=5)

        self.heatmap_button = tk.Button(root, text="Pokaż mapę ciepła", command=self.show_heatmap)
        self.heatmap_button.pack(pady=5)

        self.plot_button = tk.Button(root, text="Pokaż wykres", command=self.show_plot)
        self.plot_button.pack(pady=5)

        self.edit_button = tk.Button(root, text="Edytuj dane", command=self.edit_data)
        self.edit_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Zapisz CSV", command=self.save_csv)
        self.save_button.pack(pady=5)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pliki CSV", "*.csv")])
        if file_path:
            sep = self.sep_entry.get()
            comment = self.comment_entry.get() or None
            encoding = self.encoding_entry.get()
            try:
                self.data = pd.read_csv(file_path, sep=sep, comment=comment, encoding=encoding)
                self.column_combo["values"] = list(self.data.columns)
                messagebox.showinfo("Sukces", "Plik CSV załadowany poprawnie")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się wczytać pliku: {e}")

    def describe_data(self):
        if self.data is not None:
            desc = self.data.describe()
            print(desc)
            messagebox.showinfo("Opis statystyczny", str(desc))
        else:
            messagebox.showwarning("Błąd", "Brak danych do analizy")

    def show_heatmap(self):
        if self.data is not None:
            plt.figure(figsize=(10, 6))
            sns.heatmap(self.data.corr(), annot=True, cmap="coolwarm", fmt=".2f")
            plt.title("Mapa ciepła korelacji")
            plt.show()
        else:
            messagebox.showwarning("Błąd", "Brak danych")

    def show_plot(self):
        if self.data is not None and self.column_combo.get():
            column = self.column_combo.get()
            plt.figure(figsize=(8, 5))
            sns.histplot(self.data[column], kde=True)
            plt.title(f"Rozkład wartości: {column}")
            plt.show()
        else:
            messagebox.showwarning("Błąd", "Nie wybrano kolumny")

    def edit_data(self):
        if self.data is not None:
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edytor danych")
            edit_window.geometry("800x400")
            frame = tk.Frame(edit_window)
            frame.pack(fill=tk.BOTH, expand=True)
            pt = Table(frame, dataframe=self.data, showtoolbar=True, showstatusbar=True)
            pt.show()
            self.pt = pt
        else:
            messagebox.showwarning("Błąd", "Brak danych")

    def save_csv(self):
        if self.data is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Pliki CSV", "*.csv")])
            if file_path:
                self.data.to_csv(file_path, index=False)
                messagebox.showinfo("Sukces", "Plik zapisany poprawnie")
        else:
            messagebox.showwarning("Błąd", "Brak danych do zapisania")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVAnalyzerApp(root)
    root.mainloop()
