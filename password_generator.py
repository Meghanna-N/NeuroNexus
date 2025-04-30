import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

# --- Password Generation Logic ---
def generate_password():
    length = length_var.get()
    if length < 4:
        messagebox.showwarning("Invalid", "Password length must be at least 4.")
        return

    chars = string.ascii_lowercase
    complexity = 1  # Base complexity
    if upper_var.get():
        chars += string.ascii_uppercase
        complexity += 1
    if num_var.get():
        chars += string.digits
        complexity += 1
    if sym_var.get():
        chars += string.punctuation
        complexity += 1

    if not chars:
        messagebox.showerror("Error", "Select at least one character set.")
        return

    password = ''.join(random.choice(chars) for _ in range(length))
    result_var.set(password)
    show_strength(password, complexity)
    add_to_history(password)

def copy_to_clipboard(pwd=None):
    password = pwd if pwd else result_var.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard.")

# --- Password Strength ---
def show_strength(password, complexity):
    if len(password) < 8 or complexity < 2:
        strength = "Weak"
        color = "red"
    elif len(password) < 12 or complexity < 3:
        strength = "Medium"
        color = "orange"
    else:
        strength = "Strong"
        color = "green"
    strength_label.config(text=f"Strength: {strength}", fg=color)

# --- Password History ---
def add_to_history(password):
    history.insert(0, password)
    if len(history) > 5:
        history.pop()
    update_history_display()

def update_history_display():
    for widget in history_frame.winfo_children():
        widget.destroy()
    for i, pwd in enumerate(history):
        lbl = tk.Label(history_frame, text=f"{i+1}. {pwd}", fg="blue", cursor="hand2", bg="#f4f6f8", font=("Segoe UI", 10, "underline"))
        lbl.pack(anchor="w", padx=5)
        lbl.bind("<Button-1>", lambda e, p=pwd: copy_to_clipboard(p))

# --- GUI Setup ---
root = tk.Tk()
root.title("Password Generator")
root.geometry("450x500")
root.configure(bg="#f4f6f8")
root.resizable(False, False)

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TCheckbutton", font=("Segoe UI", 10))

# Title
tk.Label(root, text="Secure Password Generator", font=("Segoe UI", 14, "bold"), bg="#f4f6f8").pack(pady=15)

# Main Frame
frame = tk.Frame(root, bg="#f4f6f8")
frame.pack(pady=10)

# Length
tk.Label(frame, text="Password Length:", bg="#f4f6f8", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w")
length_var = tk.IntVar(value=12)
ttk.Spinbox(frame, from_=4, to=64, textvariable=length_var, width=5).grid(row=0, column=1, sticky="w")

# Options
upper_var = tk.BooleanVar(value=True)
num_var = tk.BooleanVar(value=True)
sym_var = tk.BooleanVar(value=False)

ttk.Checkbutton(frame, text="Include Uppercase Letters", variable=upper_var).grid(row=1, column=0, columnspan=2, sticky="w", pady=5)
ttk.Checkbutton(frame, text="Include Numbers", variable=num_var).grid(row=2, column=0, columnspan=2, sticky="w", pady=5)
ttk.Checkbutton(frame, text="Include Symbols", variable=sym_var).grid(row=3, column=0, columnspan=2, sticky="w", pady=5)

# Generate Button
ttk.Button(root, text="Generate Password", command=generate_password).pack(pady=10)

# Result Display
result_var = tk.StringVar()
tk.Entry(root, textvariable=result_var, font=("Segoe UI", 12), width=35, justify="center").pack(pady=5)

# Strength
strength_label = tk.Label(root, text="Strength: ", font=("Segoe UI", 10, "bold"), bg="#f4f6f8")
strength_label.pack()

# Copy
ttk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard).pack(pady=5)

# History Label
tk.Label(root, text="Recent Passwords", font=("Segoe UI", 11, "bold"), bg="#f4f6f8", pady=10).pack()
history_frame = tk.Frame(root, bg="#f4f6f8")
history_frame.pack()

# Footer
tk.Label(root, text="Made for NeuroNexus Internship", font=("Segoe UI", 9), bg="#f4f6f8", fg="#888").pack(side="bottom", pady=10)

# State
result_var.set("")
history = []
update_history_display()

root.mainloop()
