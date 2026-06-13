#import
import tkinter as tk

# main window
root = tk.Tk()
root.title("calculator")
root.geometry("250x400")
root.configure(bg="light grey")

#create global expression
global expression
expression = ""

#entry
entry = tk.Entry(root, font=("Arial", 20), justify="right", width=15)
entry.grid(columnspan=5, row=0)

history = tk.Text(root, font=("Arial", 15), height=5, width=20)
history.place(relx=.02, rely=.65)

#functions
def buttons():
    btn_c = tk.Button(root, text="C",
                    fg="black",
                    bg="gray",
                    height=1,
                    width=3,
                    padx=10,
                    pady=10,
                    )
    btn_c.grid(row=6, column=3)
    btn_c.bind("<Button-1>", press)
    buttons_list = [["7", "8", "9", "/"], ["4", "5", "6", "x"], ["1", "2", "3", "-"], [".", "0", "=", "+"]]
    for i in range(4):
        for j in range(4):
            btn = tk.Button(root, text=buttons_list[i][j],
                            fg="black",
                            bg="white",
                            height=1,
                            width=3,
                            padx=10,
                            pady=10,
                            )
            btn.grid(row=i+2, column=j)
            btn.bind("<Button-1>", press)

def press(event):
    btn_text = event.widget.cget("text")
    if btn_text.isdigit() or btn_text == ".":
        numbers(btn_text)
    elif btn_text == "C":
        clear()
    elif btn_text == "=":
        equal()
    else:
        operators(btn_text)
def numbers(btn_text):
    global expression
    if not entry.get().replace(".", "").isdigit():
        entry.delete(0, tk.END)
    if not "." in entry.get() or btn_text.isdigit():
        entry.insert(tk.END, btn_text)
        history.insert(tk.END, btn_text)
    if entry.get() == ".":
        entry.delete(0, tk.END)
        entry.insert(tk.END, "0.")
        history.delete("end-2c", "end-1c")
        history.insert(tk.END, "0.")
def clear():
    global expression
    expression = ""
    entry.delete(0, tk.END)
    history.delete("1.0", tk.END)

def operators(btn_text):
    global expression
    if entry.get() != "" and entry.get() != "/" and entry.get() != "x" and entry.get() != "-" and entry.get() != "+":
        expression += entry.get()
        entry.delete(0, tk.END)
        entry.insert(tk.END, btn_text)
        history.insert(tk.END, btn_text)
        expression += btn_text
def equal():
    global expression
    if ("/" in expression or "x" in expression or "+" in expression or "-" in expression) and (entry.get() != "+" and entry.get() != "x" and entry.get() != "-" and entry.get() != "/"):
        expression += entry.get()
        expression = expression.replace("x", "*")
        entry.delete(0, tk.END)
        print(expression)
        entry.insert(tk.END, eval(expression))
        expression = ""
        history.delete("1.0", tk.END)
        history.insert(tk.END, entry.get())
#run
buttons()
root.mainloop()