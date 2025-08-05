# Phishing.py
# Meir Shuker 318901527   Noa Agassi 209280635

from user_input       import get_user_details
from template_manager import TemplateManager
from email_service    import EmailService

def main():
    print("=== Phishing Email Automation Tool ===")

    details   = get_user_details()
    svc       = EmailService()
    raw       = svc.read_benign_email()
    template  = svc.parse_email_structure(raw)

    tm        = TemplateManager()
    full_email = tm.compose_email(details, template)

    print("\n--- Generated Phishing Email ---\n")
    print(full_email)

    mode = input("\nChoose delivery mode (1=Real SMTP, 2=MailHog) [2]: ").strip() or "2"
    if mode not in ("1", "2"):
        print("❌ Invalid choice; defaulting to '2'.")
        mode = "2"

    if mode == "1":
        smtp_server     = "smtp.gmail.com"
        smtp_port       = 587
        sender_email    = input("Your SMTP email: ").strip()
        sender_password = input("Your SMTP password: ").strip()
    else:
        smtp_server     = "127.0.0.1"
        smtp_port       = 1025
        sender_email    = "no-reply@internal.test"
        sender_password = None

    to_email  = input("Recipient's email: ").strip()
    fake_from = input("Fake From (or leave blank): ").strip() or None

    svc.send_phishing_email(
        subject         = template['subject'],
        body            = full_email,
        sender_email    = sender_email,
        sender_password = sender_password,
        to_email        = to_email,
        fake_from       = fake_from,
        smtp_server     = smtp_server,
        smtp_port       = smtp_port
    )

if __name__ == "__main__":
    main()
