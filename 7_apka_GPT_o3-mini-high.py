import customtkinter as ctk
import tkinter.filedialog as fd
import tkinter.messagebox as messagebox
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CSVAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CSV Analyzer App")
        self.geometry("1200x800")
        self.df = None  # Przechowuje wczytany DataFrame

        # Ramka z opcjami (parametry wczytywania CSV i przyciski akcji)
        self.option_frame = ctk.CTkFrame(self)
        self.option_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Wybór kodowania
        self.encoding_var = ctk.StringVar(value="utf-8")
        encoding_label = ctk.CTkLabel(self.option_frame, text="Encoding:")
        encoding_label.grid(row=0, column=0, padx=5, pady=5)
        self.encoding_dropdown = ctk.CTkOptionMenu(
            self.option_frame,
            values=["utf-8", "latin1", "cp1250", "utf-16"],
            variable=self.encoding_var
        )
        self.encoding_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Wybór separatora
        self.sep_var = ctk.StringVar(value=",")
        sep_label = ctk.CTkLabel(self.option_frame, text="Separator:")
        sep_label.grid(row=0, column=2, padx=5, pady=5)
        self.sep_dropdown = ctk.CTkOptionMenu(
            self.option_frame,
            values=[",", ";", "\t"],
            variable=self.sep_var
        )
        self.sep_dropdown.grid(row=0, column=3, padx=5, pady=5)

        # Wybór znaku komentarza
        self.comment_var = ctk.StringVar(value="")
        comment_label = ctk.CTkLabel(self.option_frame, text="Comment:")
        comment_label.grid(row=0, column=4, padx=5, pady=5)
        self.comment_dropdown = ctk.CTkOptionMenu(
            self.option_frame,
            values=["", "#", "//"],
            variable=self.comment_var
        )
        self.comment_dropdown.grid(row=0, column=5, padx=5, pady=5)

        # Przyciski akcji
        self.load_button = ctk.CTkButton(self.option_frame, text="Load CSV", command=self.load_csv)
        self.load_button.grid(row=0, column=6, padx=5, pady=5)

        self.describe_button = ctk.CTkButton(self.option_frame, text="Describe", command=self.show_describe)
        self.describe_button.grid(row=0, column=7, padx=5, pady=5)

        self.heatmap_button = ctk.CTkButton(self.option_frame, text="Heatmap", command=self.show_heatmap)
        self.heatmap_button.grid(row=0, column=8, padx=5, pady=5)

        self.save_button = ctk.CTkButton(self.option_frame, text="Save CSV", command=self.save_csv)
        self.save_button.grid(row=0, column=9, padx=5, pady=5)

        # Pole tekstowe do wyświetlania danych lub wyników describe
        self.text_box = ctk.CTkTextbox(self, width=600, height=200)
        self.text_box.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Ramka do osadzenia wykresu heatmapy
        self.heatmap_frame = ctk.CTkFrame(self)
        self.heatmap_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.canvas = None  # Miejsce na wykres matplotlib

    def load_csv(self):
        file_path = fd.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            try:
                encoding = self.encoding_var.get()
                sep = self.sep_var.get()
                comment = self.comment_var.get() if self.comment_var.get() != "" else None

                self.df = pd.read_csv(file_path, encoding=encoding, sep=sep, comment=comment)
                # Wyświetlenie pierwszych 5 wierszy w polu tekstowym
                self.text_box.delete("1.0", "end")
                self.text_box.insert("end", self.df.head().to_string())
            except Exception as e:
                messagebox.showerror("Error", f"Error reading CSV file:\n{e}")

    def show_describe(self):
        if self.df is not None:
            try:
                desc = self.df.describe().to_string()
                self.text_box.delete("1.0", "end")
                self.text_box.insert("end", desc)
            except Exception as e:
                messagebox.showerror("Error", f"Error generating describe:\n{e}")
        else:
            messagebox.showwarning("Warning", "No CSV loaded.")

    def show_heatmap(self):
        if self.df is not None:
            try:
                # Obliczenie macierzy korelacji
                corr = self.df.corr()
                plt.figure(figsize=(6, 5))
                sns.heatmap(corr, annot=True, cmap="coolwarm")
                plt.title("Correlation Heatmap")
                # Jeśli wcześniej był osadzony wykres – usuwamy go
                if self.canvas:
                    self.canvas.get_tk_widget().destroy()
                figure = plt.gcf()
                self.canvas = FigureCanvasTkAgg(figure, master=self.heatmap_frame)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack(fill="both", expand=True)
                plt.close(figure)
            except Exception as e:
                messagebox.showerror("Error", f"Error generating heatmap:\n{e}")
        else:
            messagebox.showwarning("Warning", "No CSV loaded.")

    def save_csv(self):
        if self.df is not None:
            file_path = fd.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                try:
                    # Zapisujemy aktualny DataFrame (ew. można rozszerzyć – np. odczytać zmodyfikowaną treść z text_box)
                    self.df.to_csv(file_path, index=False)
                    messagebox.showinfo("Saved", f"CSV file saved to:\n{file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error saving CSV file:\n{e}")
        else:
            messagebox.showwarning("Warning", "No CSV loaded.")

if __name__ == "__main__":
    app = CSVAnalyzerApp()
    app.mainloop()
