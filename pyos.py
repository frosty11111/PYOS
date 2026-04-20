from time import sleep
import os
import tkinter as tk
import sys
import builtins
import threading
import editor

version = "0.1.1 ALPHA TEST"

sys.path.append(os.path.dirname(__file__))

class TerminalWindow:
    def __init__(self, window):
        self.window = window
        self.text_area = tk.Text(window, bg="#1e1e1e", fg="#d4d4d4", 
                                 insertbackground="white", font=("Courier New", 11),
                                 padx=10, pady=10)
        self.text_area.pack(expand=True, fill="both")

        self.input_queue = []
        self.input_event = threading.Event()

        sys.stdout = self
        builtins.input = self.custom_input

        self.text_area.bind("<Return>", self.handle_enter)
        self.input_start_index = "1.0"

    def write(self, string):
        self.text_area.insert(tk.END, string)
        self.text_area.see(tk.END)
        self.input_start_index = self.text_area.index(tk.INSERT)

    def flush(self):
        pass

    # Метод очистки внутри класса
    def clear_screen(self):
        self.text_area.delete("1.0", tk.END)
        self.input_start_index = "1.0"

    def custom_input(self, prompt=""):
        if prompt:
            self.write(prompt)
        self.input_event.wait()
        self.input_event.clear()
        return self.input_queue.pop(0)

    def handle_enter(self, event):
        line = self.text_area.get(self.input_start_index, tk.INSERT).strip()
        self.input_queue.append(line)
        self.text_area.insert(tk.END, "\n")
        self.input_start_index = self.text_area.index(tk.INSERT)
        self.input_event.set()
        return "break"

# timer function
def timer(time):
    while time > 0:
        time -= 1
        sleep(1)
        if time == 0:
            print("Time is over!")
            break

# Calculator function
def calc():
     a = float(input("First num: "))
     b = input("Enter operator(+,-,/,*): ")
     c = float(input("Second num: "))
     if b == "+":
         print(a + c)
     if b == "-":
         print(a - c)
     if b == "*":
         print(a * c)
     if b == "/":
         print(a / c)

def terminal_logic(app):
     print("Welcome to PYOS terminal!")
     print("hint: use help command to get the list of all available commands!")
     while True:
         usr_input = input(">>> ")
         if usr_input == "text editor":
             editor.start_editor(root)
         elif usr_input == "timer":
             time_input = float(input("Set time: "))
             timer(time_input)
         elif usr_input == "help":
             print("help: prints out a page with all available commands")
             sleep(0.1)
             print("timer: sets a timer for how long you'd like (in seconds)")
             sleep(0.1)
             print("clear: clears the terminal to give more space")
             sleep(0.1)
             print("calc/calculator: starts up built-in calculator")
             sleep(0.1)
             print("exit: exits PYOS terminal")
             sleep(0.1)
             print("version: displays current version of PYOS")
         elif usr_input == "calc":
             calc()
         elif usr_input == "calculator":
             calc()
         elif usr_input == "clear":
             print("Clearing...")
             sleep(0.3)
             app.clear_screen()
         elif usr_input == "exit":
             print("Exitting PYOS")
             sleep(0.2)
             os.abort() # Жесткое завершение всей программы
         elif usr_input == "version":
             print("Current version of PYOS: " + version)
         else:
             print('"' + usr_input + '"', "is not a command, try again")

def terminal_start():
    # Создаем Toplevel (дочернее окно)
    win = tk.Toplevel(root)
    win.geometry("700x450")
    app = TerminalWindow(win)

    # Запускаем логику и передаем объект app для работы clear
    logic_thread = threading.Thread(target=terminal_logic, args=(app,), daemon=True)
    logic_thread.start()

# --- Главный интерфейс ---
root = tk.Tk()
root.geometry("1000x700")
root.title("PYOS")
root.configure(bg="teal")
root.attributes("-fullscreen", True)

print("PYOS started")

taskbar = tk.Frame(root, bg="#c0c0c0", height=40, bd=2, relief="raised")
taskbar.pack(side="bottom", fill="x")

terminal_btn = tk.Button(taskbar, text="Terminal", bg="#c0c0c0", bd=2, relief="raised", width=20, command=terminal_start)
terminal_btn.pack(side="left", padx=5, pady=2)

editor_btn = tk.Button(taskbar, text="Notepad", bg="#c0c0c0", bd=2, relief="raised", width=20, command=lambda: editor.start_editor(root))
editor_btn.pack(side="left", padx=5, pady=2)

root.mainloop()
