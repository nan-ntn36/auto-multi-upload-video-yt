import os
import json
import tkinter as tk
from tkinter import messagebox, filedialog

def load_config():
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ chính

    messagebox.showinfo("Chọn cấu hình", "📂 Vui lòng chọn file cấu hình (.json)")
    config_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if not config_path:
        messagebox.showerror("Lỗi", "Bạn chưa chọn file cấu hình!")
        exit()

    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    os.makedirs("tokens", exist_ok=True)
    root.destroy()

    return {
        "CHROME_PATH": cfg["CHROME_PATH"],
        "CLIENT_SECRET_FILE": cfg["CLIENT_SECRET_FILE"],
        "SCOPES": ["https://www.googleapis.com/auth/youtube.upload"],
        "PROFILES": cfg["PROFILES"],
        "PROFILE_PORTS": cfg["PROFILE_PORTS"],
        "WINDOW_SIZE": tuple(cfg["WINDOW_SIZE"])
    }
