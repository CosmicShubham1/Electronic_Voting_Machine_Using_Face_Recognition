import tkinter as tk
from tkinter import messagebox
from collections import Counter

def show_results():
    try:
        with open("votes.txt", "r") as f:
            votes = [line.strip().split(": ")[1] for line in f]
        results = Counter(votes)

        result_message = "🗳 Voting Results:\n\n"
        for candidate, count in results.items():
            result_message += f"{candidate}: {count} votes\n"

        messagebox.showinfo("Voting Results", result_message)
    except FileNotFoundError:
        messagebox.showerror("Error", "votes.txt not found!")

def show_total_votes():
    try:
        with open("votes.txt", "r") as f:
            total_votes = len(f.readlines())
        messagebox.showinfo("Total Votes", f"Total votes cast: {total_votes}")
    except FileNotFoundError:
        messagebox.showerror("Error", "votes.txt not found!")

def exit_app():
    root.quit()

# 🪔 GUI Setup
root = tk.Tk()
root.title("Admin Panel")
root.geometry("400x350")

# Tricolor background
top = tk.Frame(root, bg="#FF9933", height=100)  # Saffron
middle = tk.Frame(root, bg="white", height=100)
bottom = tk.Frame(root, bg="#138808", height=150)  # Green

top.pack(fill="both", expand=True)
middle.pack(fill="both", expand=True)
bottom.pack(fill="both", expand=True)

# 🪷 Title label at the top (middle frame)
title_label = tk.Label(top, text="AZADI KA AMRIT MAHOTSAV", font=("Arial", 24, "bold"), bg="#FF9933", fg="white")
title_label.pack(pady=20)

# 📊 Show Results button in bottom frame
result_button = tk.Button(bottom, text="Show Results", font=("Arial", 14), command=show_results)
result_button.pack(pady=10)

# 🗳 Total Votes button in bottom frame
total_votes_button = tk.Button(bottom, text="Total Votes", font=("Arial", 14), command=show_total_votes)
total_votes_button.pack(pady=10)

# ❌ Exit button in bottom frame
exit_button = tk.Button(bottom, text="Exit", font=("Arial", 14), command=exit_app)
exit_button.pack(pady=10)

root.mainloop()
