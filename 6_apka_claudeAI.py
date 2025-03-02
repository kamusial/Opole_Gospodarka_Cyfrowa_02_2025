import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import os


class CSVAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizator plików CSV")
        self.root.geometry("1200x800")
        self.df = None
        self.file_path = None

        # Główny kontener
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Panel lewy
        self.left_frame = ttk.LabelFrame(self.main_frame, text="Operacje")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Panel do wyboru pliku
        self.file_frame = ttk.LabelFrame(self.left_frame, text="Wczytywanie pliku")
        self.file_frame.pack(fill=tk.X, padx=5, pady=5)

        self.load_btn = ttk.Button(self.file_frame, text="Wybierz plik CSV", command=self.select_file)
        self.load_btn.pack(fill=tk.X, pady=5)

        self.file_label = ttk.Label(self.file_frame, text="Nie wybrano pliku")
        self.file_label.pack(fill=tk.X, pady=5)

        # Opcje wczytywania pliku
        # Separator
        sep_frame = ttk.Frame(self.file_frame)
        sep_frame.pack(fill=tk.X, pady=2)
        ttk.Label(sep_frame, text="Separator:").pack(side=tk.LEFT)
        self.sep_var = tk.StringVar(value=",")
        self.sep_combo = ttk.Combobox(sep_frame, textvariable=self.sep_var, values=[",", ";", "\t", " ", "|"], width=5)
        self.sep_combo.pack(side=tk.LEFT, padx=5)

        # Komentarz
        comment_frame = ttk.Frame(self.file_frame)
        comment_frame.pack(fill=tk.X, pady=2)
        ttk.Label(comment_frame, text="Znak komentarza:").pack(side=tk.LEFT)
        self.comment_var = tk.StringVar(value="#")
        self.comment_entry = ttk.Entry(comment_frame, textvariable=self.comment_var, width=5)
        self.comment_entry.pack(side=tk.LEFT, padx=5)

        # Kodowanie
        encoding_frame = ttk.Frame(self.file_frame)
        encoding_frame.pack(fill=tk.X, pady=2)
        ttk.Label(encoding_frame, text="Kodowanie:").pack(side=tk.LEFT)
        self.encoding_var = tk.StringVar(value="utf-8")
        self.encoding_combo = ttk.Combobox(encoding_frame, textvariable=self.encoding_var,
                                           values=["utf-8", "latin1", "cp1250", "cp1251", "ascii"])
        self.encoding_combo.pack(side=tk.LEFT, padx=5)

        # Header
        header_frame = ttk.Frame(self.file_frame)
        header_frame.pack(fill=tk.X, pady=2)
        ttk.Label(header_frame, text="Nagłówek:").pack(side=tk.LEFT)
        self.header_var = tk.IntVar(value=0)
        self.header_combo = ttk.Combobox(header_frame, textvariable=self.header_var,
                                         values=["0 (Pierwszy wiersz)", "None (Brak)"])
        self.header_combo.pack(side=tk.LEFT, padx=5)

        # Przycisk załadowania pliku z wybranymi opcjami
        self.load_with_options_btn = ttk.Button(self.file_frame, text="Załaduj plik z opcjami",
                                                command=self.load_csv_with_options, state="disabled")
        self.load_with_options_btn.pack(fill=tk.X, pady=5)

        # Panel wyboru kolumn
        self.columns_frame = ttk.LabelFrame(self.left_frame, text="Wybór kolumn")
        self.columns_frame.pack(fill=tk.X, padx=5, pady=5)

        self.column_label = ttk.Label(self.columns_frame, text="Wybierz kolumnę:")
        self.column_label.pack(anchor=tk.W, pady=2)

        self.column_var = tk.StringVar()
        self.column_combo = ttk.Combobox(self.columns_frame, textvariable=self.column_var, state="disabled")
        self.column_combo.pack(fill=tk.X, pady=2)

        # Panel analizy
        self.analysis_frame = ttk.LabelFrame(self.left_frame, text="Analiza")
        self.analysis_frame.pack(fill=tk.X, padx=5, pady=5)

        self.describe_btn = ttk.Button(self.analysis_frame, text="Describe", command=self.show_describe,
                                       state="disabled")
        self.describe_btn.pack(fill=tk.X, pady=5)

        self.heatmap_btn = ttk.Button(self.analysis_frame, text="Mapa ciepła", command=self.show_heatmap,
                                      state="disabled")
        self.heatmap_btn.pack(fill=tk.X, pady=5)

        self.plot_btn = ttk.Button(self.analysis_frame, text="Wykres", command=self.plot_data, state="disabled")
        self.plot_btn.pack(fill=tk.X, pady=5)

        # Panel modyfikacji
        self.modify_frame = ttk.LabelFrame(self.left_frame, text="Modyfikacja danych")
        self.modify_frame.pack(fill=tk.X, padx=5, pady=5)

        self.operation_label = ttk.Label(self.modify_frame, text="Operacja:")
        self.operation_label.pack(anchor=tk.W, pady=2)

        self.operation_var = tk.StringVar()
        self.operation_combo = ttk.Combobox(self.modify_frame, textvariable=self.operation_var,
                                            values=["Usuń brakujące dane", "Normalizuj", "Dodaj kolumnę",
                                                    "Usuń kolumnę"],
                                            state="disabled")
        self.operation_combo.pack(fill=tk.X, pady=2)

        self.apply_btn = ttk.Button(self.modify_frame, text="Zastosuj", command=self.apply_modification,
                                    state="disabled")
        self.apply_btn.pack(fill=tk.X, pady=5)

        self.save_btn = ttk.Button(self.left_frame, text="Zapisz zmodyfikowany CSV", command=self.save_csv,
                                   state="disabled")
        self.save_btn.pack(fill=tk.X, pady=10)

        # Panel prawy
        self.right_frame = ttk.Notebook(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Zakładka podglądu danych
        self.data_frame = ttk.Frame(self.right_frame)
        self.right_frame.add(self.data_frame, text="Dane")

        # Zakładka wykresu
        self.plot_frame = ttk.Frame(self.right_frame)
        self.right_frame.add(self.plot_frame, text="Wykres")

        # Zakładka analizy
        self.analysis_display_frame = ttk.Frame(self.right_frame)
        self.right_frame.add(self.analysis_display_frame, text="Analiza")

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            self.file_path = file_path
            filename = os.path.basename(file_path)
            self.file_label.config(text=f"Wybrany plik: {filename}")
            self.load_with_options_btn.config(state="normal")

            # Podgląd pierwszych kilku linii pliku
            try:
                with open(file_path, 'r', encoding=self.encoding_var.get()) as f:
                    lines = [f.readline() for _ in range(5)]

                # Usuń poprzednie widgety
                for widget in self.data_frame.winfo_children():
                    widget.destroy()

                preview_label = ttk.Label(self.data_frame, text="Podgląd pliku (pierwsze 5 linii):")
                preview_label.pack(anchor=tk.W, pady=5)

                preview_text = tk.Text(self.data_frame, height=10, width=80, wrap=tk.NONE)
                preview_text.pack(fill=tk.BOTH, expand=True)

                for line in lines:
                    preview_text.insert(tk.END, line)

                preview_text.config(state=tk.DISABLED)

                # Przełącz na zakładkę danych
                self.right_frame.select(self.data_frame)
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się otworzyć pliku dla podglądu: {str(e)}")

    def load_csv_with_options(self):
        if self.file_path:
            try:
                # Przygotuj parametry dla pd.read_csv
                params = {
                    'filepath_or_buffer': self.file_path,
                    'sep': self.sep_var.get(),
                    'encoding': self.encoding_var.get()
                }

                # Obsłuż parametr comment
                comment = self.comment_var.get()
                if comment:
                    params['comment'] = comment

                # Obsłuż parametr header
                header_val = self.header_var.get()
                if header_val == 0:
                    params['header'] = 0
                else:
                    params['header'] = None

                # Wczytaj dane
                self.df = pd.read_csv(**params)

                # Jeśli brak nagłówków, utwórz domyślne nazwy kolumn
                if header_val != 0:
                    self.df.columns = [f"Kolumna_{i}" for i in range(len(self.df.columns))]

                # Aktywuj przyciski
                self.describe_btn.config(state="normal")
                self.heatmap_btn.config(state="normal")
                self.plot_btn.config(state="normal")
                self.operation_combo.config(state="normal")
                self.apply_btn.config(state="normal")
                self.save_btn.config(state="normal")

                # Aktualizuj combobox kolumn
                self.column_combo.config(state="normal")
                self.column_combo["values"] = list(self.df.columns)
                if len(self.df.columns) > 0:
                    self.column_combo.current(0)

                # Wyświetl dane
                self.display_data()
                messagebox.showinfo("Sukces", f"Załadowano plik z wybranymi opcjami")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się załadować pliku: {str(e)}")

    def display_data(self):
        # Usuń poprzednie widgety
        for widget in self.data_frame.winfo_children():
            widget.destroy()

        if self.df is not None:
            # Informacje o danych
            info_frame = ttk.Frame(self.data_frame)
            info_frame.pack(fill=tk.X, pady=5)

            rows_label = ttk.Label(info_frame, text=f"Liczba wierszy: {len(self.df)}")
            rows_label.pack(side=tk.LEFT, padx=5)

            cols_label = ttk.Label(info_frame, text=f"Liczba kolumn: {len(self.df.columns)}")
            cols_label.pack(side=tk.LEFT, padx=5)

            # Utwórz tabelę
            tree_frame = ttk.Frame(self.data_frame)
            tree_frame.pack(fill=tk.BOTH, expand=True)

            tree_scroll_y = ttk.Scrollbar(tree_frame)
            tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

            tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")
            tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

            self.tree = ttk.Treeview(tree_frame,
                                     yscrollcommand=tree_scroll_y.set,
                                     xscrollcommand=tree_scroll_x.set)

            tree_scroll_y.config(command=self.tree.yview)
            tree_scroll_x.config(command=self.tree.xview)

            # Definiuj kolumny
            self.tree["columns"] = list(self.df.columns)
            self.tree.column("#0", width=0, stretch=tk.NO)
            for col in self.df.columns:
                self.tree.column(col, anchor=tk.W, width=100)
                self.tree.heading(col, text=col, anchor=tk.W)

            # Dodaj dane (ogranicz do 100 wierszy dla wydajności)
            for i, row in self.df.head(100).iterrows():
                values = [str(row[col]) for col in self.df.columns]
                self.tree.insert("", tk.END, text=i, values=values)

            self.tree.pack(fill=tk.BOTH, expand=True)

            # Przełącz na zakładkę danych
            self.right_frame.select(self.data_frame)

    def show_describe(self):
        if self.df is not None:
            # Usuń poprzednie widgety
            for widget in self.analysis_display_frame.winfo_children():
                widget.destroy()

            try:
                # Wybierz tylko kolumny numeryczne
                numeric_df = self.df.select_dtypes(include=['number'])

                if numeric_df.empty:
                    non_numeric_info = ttk.Label(self.analysis_display_frame,
                                                 text="Brak kolumn numerycznych do analizy statystycznej.")
                    non_numeric_info.pack(pady=10)

                    # Podstawowe informacje o danych
                    info_text = tk.Text(self.analysis_display_frame, height=20, width=80)
                    info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

                    info_text.insert(tk.END, "Informacje o danych:\n\n")
                    info_text.insert(tk.END, f"Liczba wierszy: {len(self.df)}\n")
                    info_text.insert(tk.END, f"Liczba kolumn: {len(self.df.columns)}\n\n")

                    info_text.insert(tk.END, "Typy danych:\n")
                    for col, dtype in self.df.dtypes.items():
                        info_text.insert(tk.END, f"- {col}: {dtype}\n")

                    info_text.insert(tk.END, "\nLiczba brakujących wartości:\n")
                    for col, count in self.df.isna().sum().items():
                        info_text.insert(tk.END, f"- {col}: {count}\n")

                    info_text.config(state=tk.DISABLED)
                else:
                    # Oblicz statystyki
                    desc = numeric_df.describe().reset_index()

                    # Utwórz tabelę statystyk
                    tree_frame = ttk.Frame(self.analysis_display_frame)
                    tree_frame.pack(fill=tk.BOTH, expand=True)

                    tree_scroll_y = ttk.Scrollbar(tree_frame)
                    tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

                    tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")
                    tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

                    tree = ttk.Treeview(tree_frame,
                                        yscrollcommand=tree_scroll_y.set,
                                        xscrollcommand=tree_scroll_x.set)

                    tree_scroll_y.config(command=tree.yview)
                    tree_scroll_x.config(command=tree.xview)

                    # Definiuj kolumny
                    tree["columns"] = list(desc.columns)
                    tree.column("#0", width=0, stretch=tk.NO)
                    for col in desc.columns:
                        tree.column(col, anchor=tk.W, width=100)
                        tree.heading(col, text=col, anchor=tk.W)

                    # Dodaj dane
                    for i, row in desc.iterrows():
                        values = [str(row[col]) for col in desc.columns]
                        tree.insert("", tk.END, text=i, values=values)

                    tree.pack(fill=tk.BOTH, expand=True)

                    # Dodaj informacje o brakujących wartościach
                    missing_frame = ttk.LabelFrame(self.analysis_display_frame, text="Brakujące wartości")
                    missing_frame.pack(fill=tk.X, padx=5, pady=5)

                    missing_text = tk.Text(missing_frame, height=5, width=80)
                    missing_text.pack(fill=tk.BOTH, expand=True)

                    for col, count in numeric_df.isna().sum().items():
                        percent = (count / len(numeric_df)) * 100
                        missing_text.insert(tk.END, f"{col}: {count} ({percent:.2f}%)\n")

                    missing_text.config(state=tk.DISABLED)

                # Przełącz na zakładkę analizy
                self.right_frame.select(self.analysis_display_frame)
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się wykonać analizy statystycznej: {str(e)}")

    def show_heatmap(self):
        if self.df is not None:
            # Usuń poprzednie widgety
            for widget in self.plot_frame.winfo_children():
                widget.destroy()

            try:
                # Wybierz tylko kolumny numeryczne
                numeric_df = self.df.select_dtypes(include=['number'])

                if numeric_df.empty:
                    messagebox.showerror("Błąd", "Brak kolumn numerycznych do utworzenia mapy ciepła")
                    return
                elif len(numeric_df.columns) < 2:
                    messagebox.showerror("Błąd",
                                         "Potrzebne są co najmniej dwie kolumny numeryczne do utworzenia mapy ciepła")
                    return

                # Dodaj kontrolki konfiguracji wykresu
                control_frame = ttk.Frame(self.plot_frame)
                control_frame.pack(fill=tk.X, pady=5)

                ttk.Label(control_frame, text="Paleta kolorów:").pack(side=tk.LEFT, padx=5)
                cmap_var = tk.StringVar(value="coolwarm")
                cmap_combo = ttk.Combobox(control_frame, textvariable=cmap_var,
                                          values=["coolwarm", "viridis", "plasma", "inferno", "Blues", "RdBu"])
                cmap_combo.pack(side=tk.LEFT, padx=5)

                annotate_var = tk.BooleanVar(value=True)
                annotate_check = ttk.Checkbutton(control_frame, text="Pokaż wartości", variable=annotate_var)
                annotate_check.pack(side=tk.LEFT, padx=15)

                def update_heatmap():
                    # Usuń poprzedni wykres
                    for widget in plot_container.winfo_children():
                        widget.destroy()

                    # Generuj mapę ciepła
                    fig, ax = plt.subplots(figsize=(10, 8))
                    correlation_matrix = numeric_df.corr()
                    sns.heatmap(correlation_matrix, annot=annotate_var.get(),
                                cmap=cmap_var.get(), ax=ax, fmt=".2f")
                    ax.set_title("Mapa ciepła korelacji")

                    # Utwórz canvas Matplotlib
                    canvas = FigureCanvasTkAgg(fig, master=plot_container)
                    canvas.draw()
                    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

                update_btn = ttk.Button(control_frame, text="Aktualizuj wykres", command=update_heatmap)
                update_btn.pack(side=tk.LEFT, padx=15)

                # Kontener na wykres
                plot_container = ttk.Frame(self.plot_frame)
                plot_container.pack(fill=tk.BOTH, expand=True)

                # Wywołaj funkcję aktualizacji wykresu
                update_heatmap()

                # Przełącz na zakładkę wykresu
                self.right_frame.select(self.plot_frame)
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się utworzyć mapy ciepła: {str(e)}")

    def plot_data(self):
        if self.df is not None and self.column_var.get():
            # Usuń poprzednie widgety
            for widget in self.plot_frame.winfo_children():
                widget.destroy()

            selected_column = self.column_var.get()

            try:
                # Dodaj kontrolki konfiguracji wykresu
                control_frame = ttk.Frame(self.plot_frame)
                control_frame.pack(fill=tk.X, pady=5)

                ttk.Label(control_frame, text="Typ wykresu:").pack(side=tk.LEFT, padx=5)

                # Sprawdź typ danych kolumny
                is_numeric = pd.api.types.is_numeric_dtype(self.df[selected_column])

                if is_numeric:
                    plot_types = ["histogram", "boxplot", "kde", "line"]
                else:
                    plot_types = ["bar", "pie", "count"]

                plot_type_var = tk.StringVar(value=plot_types[0])
                plot_type_combo = ttk.Combobox(control_frame, textvariable=plot_type_var, values=plot_types)
                plot_type_combo.pack(side=tk.LEFT, padx=5)

                # Druga kolumna (opcjonalnie)
                ttk.Label(control_frame, text="Druga kolumna (opcjonalnie):").pack(side=tk.LEFT, padx=15)
                second_col_var = tk.StringVar()
                second_col_combo = ttk.Combobox(control_frame, textvariable=second_col_var,
                                                values=[""] + list(self.df.columns))
                second_col_combo.pack(side=tk.LEFT, padx=5)

                def update_plot():
                    # Usuń poprzedni wykres
                    for widget in plot_container.winfo_children():
                        widget.destroy()

                    # Utwórz figurę i canvas
                    fig, ax = plt.subplots(figsize=(10, 6))
                    plot_type = plot_type_var.get()
                    second_col = second_col_var.get()

                    # Wykres w zależności od typu danych i wybranego typu wykresu
                    if is_numeric:
                        if plot_type == "histogram":
                            self.df[selected_column].hist(ax=ax, bins=20)
                            ax.set_title(f"Histogram: {selected_column}")
                        elif plot_type == "boxplot":
                            self.df.boxplot(column=selected_column, ax=ax)
                            ax.set_title(f"Boxplot: {selected_column}")
                        elif plot_type == "kde":
                            self.df[selected_column].plot.kde(ax=ax)
                            ax.set_title(f"Wykres gęstości: {selected_column}")
                        elif plot_type == "line":
                            self.df[selected_column].plot(kind='line', ax=ax)
                            ax.set_title(f"Wykres liniowy: {selected_column}")
                    else:
                        if plot_type == "bar":
                            self.df[selected_column].value_counts().plot(kind='bar', ax=ax)
                            ax.set_title(f"Rozkład wartości: {selected_column}")
                        elif plot_type == "pie":
                            self.df[selected_column].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%')
                            ax.set_title(f"Wykres kołowy: {selected_column}")
                        elif plot_type == "count":
                            self.df[selected_column].value_counts().plot(kind='barh', ax=ax)
                            ax.set_title(f"Liczba wystąpień: {selected_column}")

                    # Jeśli wybrano drugą kolumnę, utwórz wykres rozrzutu (tylko dla danych numerycznych)
                    if second_col and pd.api.types.is_numeric_dtype(self.df[second_col]):
                        plt.clf()  # Wyczyść poprzedni wykres
                        ax = fig.add_subplot(111)

                        if is_numeric:
                            self.df.plot.scatter(x=selected_column, y=second_col, ax=ax)
                            ax.set_title(f"Wykres rozrzutu: {selected_column} vs {second_col}")
                        else:
                            # Grupowanie według kategorii
                            grouped = self.df.groupby(selected_column)[second_col].mean().sort_values()
                            grouped.plot(kind='bar', ax=ax)
                            ax.set_title(f"Średnia {second_col} według {selected_column}")

                    # Formatowanie wykresu
                    ax.set_xlabel(selected_column)
                    if is_numeric:
                        ax.set_ylabel("Częstość" if plot_type == "histogram" else "Wartość")
                    else:
                        ax.set_ylabel("Liczba" if plot_type in ["bar", "count"] else "")

                    plt.tight_layout()

                    # Utwórz canvas Matplotlib
                    canvas = FigureCanvasTkAgg(fig, master=plot_container)
                    canvas.draw()
                    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

                update_btn = ttk.Button(control_frame, text="Aktualizuj wykres", command=update_plot)
                update_btn.pack(side=tk.LEFT, padx=15)

                # Przycisk zapisu wykresu
                def save_plot():
                    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                             filetypes=[("PNG Image", "*.png"),
                                                                        ("JPEG Image", "*.jpg"),
                                                                        ("PDF Document", "*.pdf")])
                    if file_path:
                        for widget in plot_container.winfo_children():
                            if isinstance(widget, FigureCanvasTkAgg):
                                widget.figure.savefig(file_path, dpi=300, bbox_inches='tight')
                                messagebox.showinfo("Sukces",
                                                    f"Zapisano wykres do pliku: {os.path.basename(file_path)}")
                                break

                save_btn = ttk.Button(control_frame, text="Zapisz wykres", command=save_plot)
                save_btn.pack(side=tk.LEFT, padx=15)

                # Kontener na wykres
                plot_container = ttk.Frame(self.plot_frame)
                plot_container.pack(fill=tk.BOTH, expand=True)

                # Wywołaj funkcję aktualizacji wykresu
                update_plot()

                # Przełącz na zakładkę wykresu
                self.right_frame.select(self.plot_frame)
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się utworzyć wykresu: {str(e)}")

    def apply_modification(self):
        if self.df is not None:
            operation = self.operation_var.get()

            try:
                if operation == "Usuń brakujące dane":
                    original_rows = len(self.df)
                    self.df = self.df.dropna()
                    new_rows = len(self.df)
                    messagebox.showinfo("Operacja zakończona",
                                        f"Usunięto {original_rows - new_rows} wierszy z brakującymi danymi.")

                elif operation == "Normalizuj":
                    # Wybierz tylko kolumny numeryczne
                    numeric_cols = self.df.select_dtypes(include=['number']).columns