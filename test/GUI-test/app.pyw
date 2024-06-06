import tkinter as tk
from tkinter import messagebox
import subprocess
import os


scripts_dir = os.getcwd() + "/test/GUI-test"
print(scripts_dir)

# funções que executam o script
def script1():
    try:
        subprocess.run(["python3", os.path.join(scripts_dir, "script1.py")], check=True)
        messagebox.showinfo("Script 1", "Script 1 executado com sucesso!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Erro ao executar Script 1: {e}")

def script2():
    try:
        subprocess.run(["python3", os.path.join(scripts_dir, "script2.py")], check=True)
        messagebox.showinfo("Script 2", "Script 2 executado com sucesso!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Erro ao executar Script 2: {e}")

def script3():
    try:
        subprocess.run(["python3", os.path.join(scripts_dir, "script3.py")], check=True)
        messagebox.showinfo("Script 3", "Script 3 executado com sucesso!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Erro ao executar Script 3: {e}")

def script4():
    try:
        subprocess.run(["python3", os.path.join(scripts_dir, "script4.py")], check=True)
        messagebox.showinfo("Script 4", "Script 4 executado com sucesso!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Erro ao executar Script 4: {e}")

# cria a janela principal
root = tk.Tk()
root.title("Projeto de Visão Computacional")
root.geometry("400x300")
root.configure(bg="#2C3E50")

# estilização dos botoes
button_style = {
    "font": ("Helvetica", 12, "bold"),
    "bg": "#3498DB",
    "fg": "white",
    "relief": tk.RAISED,
    "bd": 3,
    "width": 20,
    "height": 2,
}

# add os botoes a janela e coloca o que eles tem que fazer (command)
button1 = tk.Button(root, text="Count Fingers", command=script1, **button_style)
button1.pack(pady=10)

button2 = tk.Button(root, text="Pyautogui Mouse", command=script2, **button_style)
button2.pack(pady=10)

button3 = tk.Button(root, text="Volume Hand Control", command=script3, **button_style)
button3.pack(pady=10)

button4 = tk.Button(root, text="Projeto final", command=script4, **button_style)
button4.pack(pady=10)

root.mainloop()
