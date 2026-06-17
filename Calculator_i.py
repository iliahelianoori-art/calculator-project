#import
import tkinter as tk

# main window
root = tk.Tk()
root.title("Calculator")
root.geometry("320x500")
root.configure(bg="#1c1c1c")
root.resizable(False, False)

#create global expression
global expression, mod
expression = ""
mod = "Standard"

#entry
entry = tk.Entry(
    root,
    font=("Segoe UI", 24),
    justify="right",
    width=15,
    bg="#2d2d2d",
    fg="white",
    insertbackground="white",
    relief="flat"
)
entry.grid(columnspan=4, row=0, padx=10, pady=(15, 10), sticky="nsew")

history = tk.Text(
    root,
    font=("Segoe UI", 12),
    height=5,
    width=20,
    bg="#2d2d2d",
    fg="#cfcfcf",
    relief="flat",
)
history.grid(row=1, column=0, columnspan=4, padx=10, pady=(0, 15), sticky="nsew")

#functions
def buttons():

    btn_c = tk.Button(
        root,
        text="C",
        fg="white",
        bg="#a83232",
        activebackground="#c73d3d",
        relief="flat",
        font=("Segoe UI", 14, "bold"),
        width=5,
        height=2
    )
    btn_c.grid(row=6, column=3, padx=5, pady=5, sticky="nsew")
    btn_c.bind("<Button-1>", press)

    buttons_list = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "x"],
        ["1", "2", "3", "-"],
        [".", "0", "=", "+"]
    ]

    for i in range(4):
        for j in range(4):

            text = buttons_list[i][j]

            if text in ["/", "x", "-", "+", "="]:
                bg = "#ff9500"
                fg = "white"
            else:
                bg = "#3a3a3a"
                fg = "white"

            btn = tk.Button(
                root,
                text=text,
                fg=fg,
                bg=bg,
                activebackground="#555555",
                relief="flat",
                font=("Segoe UI", 14, "bold"),
                width=5,
                height=2
            )

            btn.grid(
                row=i + 2,
                column=j,
                padx=5,
                pady=5,
                sticky="nsew"
            )

            btn.bind("<Button-1>", press)
    btn_setmode = tk.Button(
                  root,
                  text="Standard",
                  fg="white",
                  bg="#3a3a3a",
                  activebackground="#555555",
                  relief="flat",
                  font=("Segoe UI", 14, "bold"),
                  height=2
    )
    btn_setmode.grid(
        row=6,
        column=0,
        columnspan=3,
        padx=5,
        pady=5,
        sticky="nsew"

    )
    btn_setmode.bind("<Button-1>", press)
def press(event):
    global mod, expression
    btn_text = event.widget.cget("text")
    if btn_text.isdigit() or btn_text == ".":
        numbers(btn_text)
    elif btn_text == "C":
        clear()
    elif btn_text == "=":
        if mod == "Standard":
            equal_standard()
        else:
            equal_scientific()
    elif btn_text == "Standard":
        event.widget.config(text="Scientific")
        mod = "Scientific"
        entry.delete(0, tk.END)
        expression = ""
        history.delete("1.0", tk.END)
    elif btn_text == "Scientific":
        event.widget.config(text="Standard")
        entry.delete(0, tk.END)
        expression = ""
        history.delete("1.0", tk.END)
        mod = "Standard"
    else:
        if mod == "Standard":
            operators_standard(btn_text)
        else:
            operators_scientific(btn_text)

def numbers(btn_text):
    global expression
    if not entry.get().replace(".", "").isdigit():
        if mod == "Scientific":
            entry.delete(0, tk.END)

    if btn_text.isdigit():
        entry.insert(tk.END, btn_text)
        history.insert(tk.END, btn_text)
    else:
        left = ""
        right = ""
        if mod == "Scientific":
            if not "." in entry.get():
                entry.insert(tk.END, btn_text)
                history.insert(tk.END, btn_text)
        else:
            for i in entry.get():
                if i != "." and not i.isdigit():
                    left = entry.get().partition(i)[0]
                    right = entry.get().partition(i)[2]
            if not left:
                if not "." in entry.get():
                    entry.insert(tk.END, btn_text)
            else:
                if not right:
                    entry.insert(tk.END, "0.")
                else:
                    if not "." in right:
                        entry.insert(tk.END, btn_text)

    if entry.get() == ".":
        entry.delete(0, tk.END)
        entry.insert(tk.END, "0.")
        history.delete("end-2c", "end-1c")
        history.insert(tk.END, "0.")

def clear():
    global expression
    expression = ""
    entry.delete(0, tk.END)
    last_line = int(history.index("end-1c").split(".")[0])
    history.delete(f"{last_line}.0", f"{last_line+1}.0")
    history.insert( tk.END, "\n")

def operators_scientific(btn_text):
    global expression

    if not entry.get() in " x/-+":
        expression += entry.get()
        entry.delete(0, tk.END)
        entry.insert(tk.END, btn_text)
        history.insert(tk.END, btn_text)
        expression += btn_text

def operators_standard(btn_text):
    global expression
    check = True
    if not entry.get() == "":
        if entry.get()[len(entry.get()) - 1] not in "x-/+":
            if not entry.get() in " x/-+":
                for i in  "x/-+":
                    if i in expression:
                        check = False
                        break
                if check:
                    expression += entry.get()
                else:
                    temp_result = eval(entry.get().replace("x", "*"))
                    entry.delete(0, tk.END)
                    entry.insert(tk.END, temp_result)
                    expression = entry.get()
                entry.insert(tk.END, btn_text)
                history.insert(tk.END, btn_text)
                expression += btn_text

def equal_scientific():
    global expression
    if any(op in expression for op in "x/-+") and (not entry.get() in " x/-+"):
        expression += entry.get()
        expression = expression.replace("x", "*")
        entry.delete(0, tk.END)
        result = eval(expression)
        len_result = len(str(result))
        if str(result)[len_result - 1] == "0":
            result = int(result)
        entry.insert(tk.END, str(result))
        expression = ""
        history.insert(tk.END, f"={result}\n{result}")

def equal_standard():
    check = True
    for i in "x-/+":
        if i in entry.get():
            try:
                a = entry.get()[entry.get().find(i) + 1]
                check = False
            except IndexError:
                pass
    if not check and entry.get() != "":
        result = eval(entry.get().replace("x", "*"))
        len_result = len(str(result))
        if str(result)[len_result - 1] == "0":
            result = int(result)
        entry.delete(0, tk.END)
        entry.insert(tk.END, result)
        history.insert(tk.END, f"={result}\n{result}")
for i in range(7):
    root.grid_rowconfigure(i, weight=1)

for j in range(4):
    root.grid_columnconfigure(j, weight=1)

#run
buttons()
root.mainloop()