"""Interfaz gráfica sencilla para operar sobre objetos persistentes."""
import argparse
import tkinter as tk
from tkinter import ttk, messagebox
from orm import Base, conectar, listar, alta, resumen_sql

p = argparse.ArgumentParser()
p.add_argument('--base', default='datos/itc.sqlite')
args = p.parse_args()
from pathlib import Path
Path(args.base).parent.mkdir(parents=True, exist_ok=True)
engine = conectar(args.base)
Base.metadata.create_all(engine)
ventana = tk.Tk()
ventana.title('ITC · Clientes y proyectos · ORM RA3')
ventana.geometry('850x480')
ttk.Label(ventana, text='Clientes y proyectos ITC', font=('Segoe UI', 18)).pack(pady=15)
tabla = ttk.Treeview(ventana, columns=('id','nombre','email','proyectos'), show='headings')
for campo in ('id','nombre','email','proyectos'):
    tabla.heading(campo, text=campo.capitalize())
tabla.pack(fill='both', expand=True, padx=20)
formulario = ttk.Frame(ventana)
formulario.pack(pady=15)
nombre = ttk.Entry(formulario)
email = ttk.Entry(formulario)
ttk.Label(formulario,text='Empresa').grid(row=0,column=0)
nombre.grid(row=0,column=1)
ttk.Label(formulario,text='Email').grid(row=0,column=2)
email.grid(row=0,column=3)
def refrescar():
    tabla.delete(*tabla.get_children())
    for fila in listar(engine): tabla.insert('', 'end', values=fila)
def guardar():
    if not nombre.get().strip() or '@' not in email.get():
        return messagebox.showerror('Datos incompletos','Introduce empresa y correo.')
    try:
        alta(engine,nombre.get().strip(),email.get().strip())
        refrescar()
    except Exception as error: messagebox.showerror('Operación revertida',str(error))
ttk.Button(formulario,text='Crear cliente y proyecto',command=guardar).grid(row=0,column=4,padx=10)
ttk.Button(ventana,text='Consultar resumen SQL',command=lambda:messagebox.showinfo('Estados',str(resumen_sql(engine)))).pack(pady=5)
refrescar()
ventana.mainloop()
engine.dispose()
