import re
import secrets
import string
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
# from keras.models import load_model

def predict_strength_with_model(pw):
    # Dummy strength predictor based on character variety
    score = sum([
        bool(re.search(r"[a-z]", pw)),
        bool(re.search(r"[A-Z]", pw)),
        bool(re.search(r"\d", pw)),
        bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", pw)),
        len(pw) >= 12
    ])
    return score / 5.0

# --- Password Evaluation ---
def evaluate_strength(pw):
    score = 0
    feedback = []

    if len(pw) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters.")

    if re.search(r"[a-z]", pw):
        score += 1
    else:
        feedback.append("Include lowercase letters.")

    if re.search(r"[A-Z]", pw):
        score += 1
    else:
        feedback.append("Include uppercase letters.")

    if re.search(r"[0-9]", pw):
        score += 1
    else:
        feedback.append("Add some digits.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", pw):
        score += 1
    else:
        feedback.append("Use special characters (!@#$ etc).")

    return score, feedback

def suggest_passwords(name, email, dob, count=5):
    ideas = []
    try:
        bdate = datetime.strptime(dob, "%Y-%m-%d")
        birth_fmt = bdate.strftime("%d%m%Y")
    except:
        birth_fmt = secrets.token_hex(2)

    keywords = []
    if name:
        keywords.append(name.strip().split()[0])
    if email:
        keywords.append(email.strip().split('@')[0])
    keywords.append(birth_fmt)

    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    for _ in range(count):
        base = secrets.choice(keywords).capitalize()
        rand = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(3))
        symbol = secrets.choice(special_chars)
        number = str(secrets.randbelow(100))
        ideas.append(f"{base}{symbol}{rand}{number}")

    return ideas

def random_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    return ''.join(secrets.choice(chars) for _ in range(length))

# --- Pandas: History Logging ---
history_df = pd.DataFrame(columns=["Name", "Email", "DOB", "Password", "Score", "AI Score", "Timestamp"])

def log_history(name, email, dob, pw, score, ai_score):
    global history_df
    history_df.loc[len(history_df)] = {
        "Name": name, "Email": email, "DOB": dob,
        "Password": pw, "Score": score, "AI Score": ai_score,
        "Timestamp": datetime.now()
    }

# --- Matplotlib Chart for Password ---
def plot_character_distribution(pw):
    labels = ['Lowercase', 'Uppercase', 'Digits', 'Special']
    counts = [
        len(re.findall(r"[a-z]", pw)),
        len(re.findall(r"[A-Z]", pw)),
        len(re.findall(r"\d", pw)),
        len(re.findall(r"[!@#$%^&*(),.?\":{}|<>]", pw))
    ]
    plt.figure(figsize=(4, 2.5))
    plt.bar(labels, counts, color='lightgreen')
    plt.title("Character Distribution")
    plt.tight_layout()
    plt.savefig("char_dist.png")
    plt.close()

# --- GUI Logic ---
def run_check():
    name = name_entry.get()
    email = email_entry.get()
    dob = dob_entry.get()
    pw = pw_entry.get()

    if not pw:
        messagebox.showwarning("Missing Info", "Enter a password to check.")
        return

    score, notes = evaluate_strength(pw)
    ai_score = predict_strength_with_model(pw)

    out = f"Password Score: {score}/5\nAI Predicted Strength: {round(ai_score * 100)}%\n"

    if score < 4:
        out += "\nSuggestions to improve:\n"
        for n in notes:
            out += f" - {n}\n"
    else:
        out += "\nLooks good! Your password seems strong.\n"

    out += "\nPassword Suggestions:\n"
    for s in suggest_passwords(name, email, dob):
        out += f" - {s}\n"

    log_history(name, email, dob, pw, score, ai_score)
    display_output(out)

    plot_character_distribution(pw)
    show_chart()

def show_chart():
    try:
        img = Image.open("char_dist.png")
        img = img.resize((400, 200), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        chart_label.config(image=img)
        chart_label.image = img
    except Exception as e:
        print("Chart error:", e)

def more_suggestions():
    name = name_entry.get()
    email = email_entry.get()
    dob = dob_entry.get()
    extra = "\nMore Suggestions:\n"
    for s in suggest_passwords(name, email, dob):
        extra += f" - {s}\n"
    append_output(extra)

def gen_random():
    pw = random_password()
    out = f"\nRandom Password:\n - {pw}\n"
    append_output(out)

def clear_fields():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    dob_entry.delete(0, tk.END)
    pw_entry.delete(0, tk.END)
    output_box.config(state='normal')
    output_box.delete("1.0", tk.END)
    output_box.config(state='disabled')
    chart_label.config(image="")

def display_output(text):
    output_box.config(state='normal')
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, text)
    output_box.config(state='disabled')

def append_output(text):
    output_box.config(state='normal')
    output_box.insert(tk.END, text)
    output_box.config(state='disabled')

# --- GUI Setup ---
root = tk.Tk()
root.title("Smart Password Checker")
root.geometry("580x800")
root.resizable(False, False)

bg = "#1e1e1e"
fg = "#ffffff"
entry_bg = "#2e2e2e"
btn_primary = "#4CAF50"
btn_secondary = "#3b3b3b"

root.configure(bg=bg)

def labeled_input(label_text):
    tk.Label(root, text=label_text, bg=bg, fg=fg).pack()
    entry = tk.Entry(root, width=50, bg=entry_bg, fg=fg, insertbackground=fg)
    entry.pack()
    return entry

# Inputs
name_entry = labeled_input("Name:")
email_entry = labeled_input("Email:")
dob_entry = labeled_input("Birthdate (YYYY-MM-DD):")
pw_entry = labeled_input("Password:")
pw_entry.config(show="*")

# Buttons
tk.Button(root, text="Check Password", command=run_check,
          bg=btn_primary, fg="white", activebackground=btn_primary).pack(pady=10)

tk.Button(root, text="More Suggestions", command=more_suggestions,
          bg=btn_secondary, fg="white").pack(pady=5)

tk.Button(root, text="Generate Random Password", command=gen_random,
          bg=btn_secondary, fg="white").pack(pady=5)

tk.Button(root, text="Clear All", command=clear_fields,
          bg="#992222", fg="white").pack(pady=10)

# Output Text Box
output_box = tk.Text(root, height=14, width=70, wrap="word", state='disabled',
                     bg="#2a2a2a", fg=fg, insertbackground=fg)
output_box.pack(pady=10)

# Image Label for Chart
chart_label = tk.Label(root, bg=bg)
chart_label.pack()

root.mainloop()
