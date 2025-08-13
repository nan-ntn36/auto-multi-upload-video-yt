import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from services.youtube_tools import open_all_profiles, upload_video, create_token_all_with_profiles


def upload_all_profiles_ui(root, PROFILES, SCOPES):
    win = tk.Toplevel(root)
    win.title("📤 Upload video cho tất cả tài khoản")
    win.geometry("500x300")
    win.resizable(False, False)

    file_var = tk.StringVar()
    title_var = tk.StringVar()
    desc_var = tk.StringVar()

    frame_file = tk.Frame(win)
    frame_file.pack(pady=10, fill="x", padx=10)
    tk.Label(frame_file, text="📂 Chọn file video:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
    tk.Entry(frame_file, textvariable=file_var, width=40).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_file, text="Browse", command=lambda: file_var.set(
        filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    )).pack(side=tk.LEFT)

    frame_title = tk.Frame(win)
    frame_title.pack(pady=5, fill="x", padx=10)
    tk.Label(frame_title, text="📝 Tiêu đề:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
    tk.Entry(frame_title, textvariable=title_var, width=50).pack(side=tk.LEFT, padx=5)

    frame_desc = tk.Frame(win)
    frame_desc.pack(pady=5, fill="x", padx=10)
    tk.Label(frame_desc, text="📄 Mô tả:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
    tk.Entry(frame_desc, textvariable=desc_var, width=50).pack(side=tk.LEFT, padx=5)

    tk.Label(win, text="Tiến trình upload:", font=("Arial", 10, "bold")).pack(pady=10)
    progress = ttk.Progressbar(win, orient="horizontal", length=400, mode="determinate")
    progress.pack(pady=5)

    def confirm_upload():
        video_path = file_var.get()
        title = title_var.get()
        desc = desc_var.get()
        if not video_path or not title:
            messagebox.showwarning("Thiếu thông tin", "Bạn cần chọn video và nhập tiêu đề!")
            return
        total = len(PROFILES)
        progress["maximum"] = total
        progress["value"] = 0
        for i, profile_key in enumerate(PROFILES, start=1):
            upload_video(profile_key, video_path, title, desc, PROFILES, SCOPES)
            progress["value"] = i
            win.update_idletasks()
        messagebox.showinfo("Hoàn tất", "🎉 Đã upload xong cho tất cả tài khoản.")

    tk.Button(win, text="✅ Confirm Upload", bg="orange", fg="black",
              font=("Arial", 11, "bold"), command=confirm_upload).pack(pady=15)


def create_main_ui(config):
    root = tk.Tk()
    root.title("🎬 Multi YouTube Launcher + Uploader")
    root.geometry("400x350")
    root.configure(bg="#f5f5f5")

    title_label = tk.Label(root, text="📺 Quản lý tài khoản YouTube",
                           font=("Arial", 14, "bold"), bg="#f5f5f5", fg="#333")
    title_label.pack(pady=15)

    btn_frame = tk.Frame(root, bg="#f5f5f5")
    btn_frame.pack(pady=10)

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 11), padding=5)

    ttk.Button(btn_frame, text="🌐 Mở tất cả profiles", width=30,
               command=lambda: open_all_profiles(config["PROFILES"], config["CHROME_PATH"], config["WINDOW_SIZE"])).pack(pady=8)

    ttk.Button(btn_frame, text="📤 Upload video cho tất cả", width=30,
               command=lambda: upload_all_profiles_ui(root, config["PROFILES"], config["SCOPES"])).pack(pady=8)

    ttk.Button(btn_frame, text="🔑 Tạo token cho tất cả", width=30,
               command=lambda: create_token_all_with_profiles(config["PROFILES"], config["PROFILE_PORTS"],
                                                              config["CLIENT_SECRET_FILE"], config["SCOPES"],
                                                              config["CHROME_PATH"])).pack(pady=8)

    footer_label = tk.Label(root, text="Made with ❤️ by NghiaDz",
                            font=("Arial", 8), bg="#f5f5f5", fg="#777")
    footer_label.pack(side=tk.BOTTOM, pady=10)

    root.mainloop()
