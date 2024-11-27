import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from HDDStructure import HDD
from database_manager import SQLProcessor

class DiskSimulatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Simulador de Disco Duro")

        self.num_platos = 4
        self.num_pistas_por_plato = 8
        self.num_sectores_por_pista = 16
        self.tamano_bytes = 512

        self.query_label = tk.Label(master, text="Ingrese su consulta:")
        self.query_label.pack()

        self.query_text = tk.Text(master, height=10, width=50)
        self.query_text.pack()

        self.execute_button = tk.Button(master, text="Ejecutar Consulta", command=self.execute_query)
        self.execute_button.pack()

        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT)

        self.plot_disk()

    def plot_disk(self):
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.set_title("Simulación de Disco Duro")
        ax.pie([1, 1, 1, 1], labels=["Plato 1", "Plato 2", "Plato 3", "Plato 4"], autopct='%1.1f%%')
        ax.axis('equal')
        self.canvas.draw()

    def execute_query(self):
        query = self.query_text.get("1.0", tk.END).strip()
        if not query:
            messagebox.showerror("Error", "Por favor ingrese una consulta")
            return
        
        try:
            hdd = HDD(self.num_platos, self.num_pistas_por_plato, self.num_sectores_por_pista, self.tamano_bytes)
            sql_processor = SQLProcessor(hdd)
            sql_processor.procesar_query(query)
            self.plot_disk()
            messagebox.showinfo("Consulta Ejecutada", f"Se ejecutó la consulta: {query}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = DiskSimulatorApp(root)
    root.mainloop()