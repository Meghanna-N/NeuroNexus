import json
import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog

CONTACTS_FILE = "contacts.json"

def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)

def refresh_contact_list():
    contact_list.delete(*contact_list.get_children())
    for contact in contacts:
        contact_list.insert("", tk.END, values=(contact["name"], contact["phone"], contact["email"], contact["address"]))
    update_counter()

def update_counter():
    total_var.set(f"{len(contacts)} Contact(s)")

def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()
    address = address_entry.get().strip()

    if not name or not phone:
        messagebox.showwarning("Input Error", "Name and Phone are required.")
        return

    if any(c["phone"] == phone for c in contacts):
        messagebox.showwarning("Duplicate", "A contact with this phone number already exists.")
        return

    contacts.append({"name": name, "phone": phone, "email": email, "address": address})
    save_contacts(contacts)
    clear_form()
    refresh_contact_list()
    messagebox.showinfo("Success", "Contact added.")

def clear_form():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

def delete_contact():
    selected = contact_list.selection()
    if not selected:
        messagebox.showwarning("Delete", "Select a contact to delete.")
        return
    index = contact_list.index(selected[0])
    deleted = contacts.pop(index)
    save_contacts(contacts)
    refresh_contact_list()
    messagebox.showinfo("Deleted", f"Contact '{deleted['name']}' deleted.")

def search_contact():
    query = simpledialog.askstring("Search", "Enter name or phone:")
    if not query:
        return
    filtered = [c for c in contacts if query.lower() in c["name"].lower() or query in c["phone"]]
    contact_list.delete(*contact_list.get_children())
    for contact in filtered:
        contact_list.insert("", tk.END, values=(contact["name"], contact["phone"], contact["email"], contact["address"]))
    total_var.set(f"{len(filtered)} Search Result(s)")

def clear_search():
    refresh_contact_list()

def update_contact():
    selected = contact_list.selection()
    if not selected:
        messagebox.showwarning("Update", "Select a contact to update.")
        return

    index = contact_list.index(selected[0])
    current = contacts[index]

    # Pop-up window for editing
    edit_win = tk.Toplevel(root)
    edit_win.title("Update Contact")
    edit_win.geometry("400x300")
    edit_win.resizable(False, False)

    # Input fields
    tk.Label(edit_win, text="Name:", font=("Segoe UI", 10)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
    name_var = tk.StringVar(value=current['name'])
    name_entry_ = ttk.Entry(edit_win, textvariable=name_var, width=30)
    name_entry_.grid(row=0, column=1)

    tk.Label(edit_win, text="Phone:", font=("Segoe UI", 10)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
    phone_var = tk.StringVar(value=current['phone'])
    phone_entry_ = ttk.Entry(edit_win, textvariable=phone_var, width=30)
    phone_entry_.grid(row=1, column=1)

    tk.Label(edit_win, text="Email:", font=("Segoe UI", 10)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
    email_var = tk.StringVar(value=current['email'])
    email_entry_ = ttk.Entry(edit_win, textvariable=email_var, width=30)
    email_entry_.grid(row=2, column=1)

    tk.Label(edit_win, text="Address:", font=("Segoe UI", 10)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
    address_var = tk.StringVar(value=current['address'])
    address_entry_ = ttk.Entry(edit_win, textvariable=address_var, width=30)
    address_entry_.grid(row=3, column=1)

    def save_update():
        new_name = name_var.get().strip()
        new_phone = phone_var.get().strip()
        new_email = email_var.get().strip()
        new_address = address_var.get().strip()

        if not new_name or not new_phone:
            messagebox.showerror("Input Error", "Name and Phone are required.")
            return

        contacts[index] = {
            "name": new_name,
            "phone": new_phone,
            "email": new_email,
            "address": new_address
        }
        save_contacts(contacts)
        refresh_contact_list()
        messagebox.showinfo("Updated", "Contact updated successfully.")
        edit_win.destroy()

    ttk.Button(edit_win, text="Save Changes", command=save_update).grid(row=4, column=0, columnspan=2, pady=20)

def export_to_csv():
    filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not filepath:
        return
    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Phone", "Email", "Address"])
        for c in contacts:
            writer.writerow([c["name"], c["phone"], c["email"], c["address"]])
    messagebox.showinfo("Exported", f"Contacts exported to {filepath}")

def sort_column(col):
    global sort_order
    reverse = sort_order.get(col, False)
    sorted_contacts = sorted(contacts, key=lambda x: x[col].lower(), reverse=reverse)
    sort_order[col] = not reverse
    contact_list.delete(*contact_list.get_children())
    for contact in sorted_contacts:
        contact_list.insert("", tk.END, values=(contact["name"], contact["phone"], contact["email"], contact["address"]))
    total_var.set(f"{len(sorted_contacts)} Contact(s)")

# App state
contacts = load_contacts()
sort_order = {}

# GUI setup
root = tk.Tk()
root.title("Contact Book")
root.geometry("800x550")
root.configure(bg="#f4f6f8")

style = ttk.Style()
style.configure("Treeview", font=("Segoe UI", 10), rowheight=24)
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
style.configure("TButton", font=("Segoe UI", 10), padding=6)

# Input form
form_frame = tk.Frame(root, bg="#f4f6f8")
form_frame.pack(padx=20, pady=15)

tk.Label(form_frame, text="Name", bg="#f4f6f8", font=("Segoe UI", 10)).grid(row=0, column=0, padx=5, pady=5)
name_entry = ttk.Entry(form_frame, width=25)
name_entry.grid(row=0, column=1, padx=5)

tk.Label(form_frame, text="Phone", bg="#f4f6f8", font=("Segoe UI", 10)).grid(row=0, column=2, padx=5, pady=5)
phone_entry = ttk.Entry(form_frame, width=25)
phone_entry.grid(row=0, column=3, padx=5)

tk.Label(form_frame, text="Email", bg="#f4f6f8", font=("Segoe UI", 10)).grid(row=1, column=0, padx=5, pady=5)
email_entry = ttk.Entry(form_frame, width=25)
email_entry.grid(row=1, column=1, padx=5)

tk.Label(form_frame, text="Address", bg="#f4f6f8", font=("Segoe UI", 10)).grid(row=1, column=2, padx=5, pady=5)
address_entry = ttk.Entry(form_frame, width=25)
address_entry.grid(row=1, column=3, padx=5)

ttk.Button(form_frame, text="Add Contact", command=add_contact).grid(row=2, column=0, columnspan=4, pady=10)

# Contact list
list_frame = tk.Frame(root)
list_frame.pack(padx=20, pady=5, fill="both", expand=True)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

contact_list = ttk.Treeview(list_frame, columns=("Name", "Phone", "Email", "Address"), show="headings", yscrollcommand=scrollbar.set)
for col in ("Name", "Phone", "Email", "Address"):
    contact_list.heading(col, text=col, command=lambda c=col.lower(): sort_column(c))
    contact_list.column(col, width=180, anchor="center")
contact_list.pack(fill="both", expand=True)
scrollbar.config(command=contact_list.yview)

# Action buttons
btn_frame = tk.Frame(root, bg="#f4f6f8")
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="Search", width=12, command=search_contact).grid(row=0, column=0, padx=8)
ttk.Button(btn_frame, text="Update", width=12, command=update_contact).grid(row=0, column=1, padx=8)
ttk.Button(btn_frame, text="Delete", width=12, command=delete_contact).grid(row=0, column=2, padx=8)
ttk.Button(btn_frame, text="View All", width=12, command=clear_search).grid(row=0, column=3, padx=8)
ttk.Button(btn_frame, text="Export CSV", width=12, command=export_to_csv).grid(row=0, column=4, padx=8)
ttk.Button(btn_frame, text="Exit", width=12, command=root.quit).grid(row=0, column=5, padx=8)

# Footer
total_var = tk.StringVar()
footer = tk.Label(root, textvariable=total_var, bg="#f4f6f8", font=("Segoe UI", 10))
footer.pack(side=tk.BOTTOM, pady=8)

refresh_contact_list()
root.mainloop()
