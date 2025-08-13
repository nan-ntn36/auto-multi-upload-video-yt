import os
import subprocess
import threading
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from tkinter import messagebox
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow


def open_youtube(profile_key, PROFILES, CHROME_PATH, WINDOW_SIZE, shorts=False):
    profile = PROFILES[profile_key]
    x, y = profile["position"]
    url = "https://www.youtube.com/shorts" if shorts else "https://www.youtube.com"
    try:
        subprocess.Popen([
            CHROME_PATH,
            f"--profile-directory={profile_key}",
            "--new-window",
            f"--app={url}",
            f"--window-position={x},{y}",
            f"--window-size={WINDOW_SIZE[0]},{WINDOW_SIZE[1]}"
        ])
    except FileNotFoundError:
        messagebox.showerror("Lỗi", f"Không tìm thấy Chrome tại:\n{CHROME_PATH}")


def open_all_profiles(PROFILES, CHROME_PATH, WINDOW_SIZE, shorts=False):
    for profile_key in PROFILES:
        open_youtube(profile_key, PROFILES, CHROME_PATH, WINDOW_SIZE, shorts)


def create_token_all_with_profiles(PROFILES, PROFILE_PORTS, CLIENT_SECRET_FILE, SCOPES, CHROME_PATH):
    if not os.path.exists(CLIENT_SECRET_FILE):
        messagebox.showerror("Lỗi", f"Không tìm thấy file OAuth: {CLIENT_SECRET_FILE}")
        return

    def start_server(profile_key, port):
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES,
                redirect_uri=f"http://localhost:{port}/"
            )
            auth_url, _ = flow.authorization_url(
                prompt="consent",
                access_type="offline",
                include_granted_scopes="true"
            )

            class OAuthHandler(BaseHTTPRequestHandler):
                def do_GET(self):
                    params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                    if "code" in params:
                        flow.fetch_token(code=params["code"][0])
                        with open(PROFILES[profile_key]["token"], "w") as token_file:
                            token_file.write(flow.credentials.to_json())
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(f"<h1>Tạo token thành công cho profile {profile_key}</h1>".encode("utf-8"))
                    else:
                        self.send_response(400)
                        self.end_headers()
                        self.wfile.write("<h1>Token thất bại</h1>".encode("utf-8"))

            server = HTTPServer(("localhost", port), OAuthHandler)
            threading.Thread(target=server.serve_forever, daemon=True).start()

            subprocess.Popen([
                CHROME_PATH,
                f"--profile-directory={profile_key}",
                auth_url
            ])
        except Exception as e:
            messagebox.showerror("Lỗi tạo token", f"{profile_key}: {e}")

    for profile_key, port in PROFILE_PORTS.items():
        start_server(profile_key, port)

    messagebox.showinfo("Thông báo", "Đã mở tất cả Chrome profiles.\nVui lòng cấp quyền cho từng tài khoản.")


def upload_video(profile_key, video_path, title, description, PROFILES, SCOPES):
    profile = PROFILES[profile_key]
    token_file = profile["token"]

    if not os.path.exists(token_file):
        messagebox.showerror("Lỗi", f"Chưa có token cho {profile['display_name']}. Hãy tạo token trước.")
        return

    try:
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        youtube = build("youtube", "v3", credentials=creds)

        body = {
            "snippet": {"title": title, "description": description, "categoryId": "22"},
            "status": {"privacyStatus": "public"}
        }
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        response = request.execute()
        print(f"[{profile['display_name']}] Uploaded: https://youtu.be/{response['id']}")
        messagebox.showinfo("Thành công", f"Đã upload video cho {profile['display_name']}")
    except Exception as e:
        messagebox.showerror("Upload Lỗi", f"{profile['display_name']}: {e}")
