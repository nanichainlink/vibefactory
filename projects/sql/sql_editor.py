import sqlite3
import tkinter as tk
from tkinter import scrolledtext, messagebox

class SQLEditor(tk.Frame):
    def __init__(self, master, db_path):
        super().__init__(master)
        self.master = master
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_widgets()
    
    def create_widgets(self):
        # Editor de consultas
        self.query_editor = scrolledtext.ScrolledText(self, height=10, width=80, font=("Consolas", 12))
        self.query_editor.pack(padx=10, pady=10)

        # Botón para ejecutar consulta
        self.run_button = tk.Button(self, text="Ejecutar Consulta", command=self.execute_query)
        self.run_button.pack(pady=(0,10))

        # Área de resultados
        self.result_area = scrolledtext.ScrolledText(self, height=15, width=80, font=("Consolas", 12), state='disabled')
        self.result_area.pack(padx=10, pady=10)

    def execute_query(self):
        query = self.query_editor.get("1.0", tk.END).strip()
        if not query:
            messagebox.showwarning("Advertencia", "Por favor, escribe una consulta SQL.")
            return

        try:
            self.cursor.execute(query)
            if query.lower().startswith("select"):
                rows = self.cursor.fetchall()
                columns = [desc[0] for desc in self.cursor.description]
                result = self.format_results(columns, rows)
            else:
                self.connection.commit()
                result = "Consulta ejecutada correctamente."
        except sqlite3.Error as e:
            result = f"Error: {e}"

        self.result_area.config(state='normal')
        self.result_area.delete("1.0", tk.END)
        self.result_area.insert(tk.END, result)
        self.result_area.config(state='disabled')

    def format_results(self, columns, rows):
        if not rows:
            return "Sin resultados."
        col_widths = [max(len(str(col)), 12) for col in columns]
        for row in rows:
            for i, val in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(val)))
        header = " | ".join(col.ljust(col_widths[i]) for i, col in enumerate(columns))
        separator = "-+-".join("-" * w for w in col_widths)
        data = "\n".join(" | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)) for row in rows)
        return f"{header}\n{separator}\n{data}"

    def close(self):
        self.connection.close()

def main():
    root = tk.Tk()
    root.title("Editor de Consultas SQL")
    editor = SQLEditor(root, db_path="game.db")  # Cambia 'game.db' por el nombre de tu base de datos
    editor.pack(fill="both", expand=True)
    root.protocol("WM_DELETE_WINDOW", lambda: (editor.close(), root.destroy()))
    root.mainloop()

if __name__ == "__main__":
    main()