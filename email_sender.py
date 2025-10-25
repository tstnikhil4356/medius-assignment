import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()


def send_assignment_email():
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    candidate_name = os.getenv('FULL_NAME')

    to_email = 'tech@themedius.ai'
    cc_email = 'hr@themedius.ai'
    subject = f"Python (Selenium) Assignment - {candidate_name}"

    body = f"""Dear Hiring Team,

I am submitting my assignment for the Python (Selenium) position. Please find the attached materials:

1. Screenshot of the form filled via automated code (form_confirmation.png)
2. Source code repository: https://github.com/tstnikhil4356/medius-assignment/
3. Documentation of approach (README.md in repository)
4. Resume (attached)
5. Past projects and work samples:
   - Expose Ai :- https://github.com/tstnikhil4356/Expose-Ai-Spot-the-fake-CipherCop2025
   - DeepLearning Classification :- https://github.com/tstnikhil4356/breast-cancer-image-classification-using-resnet18
   - EventSpace :- https://github.com/tstnikhil4356/EventSpace-2025
6. Availability Confirmation: I am available to work part-time from 4 PM to 8 PM on weekdays, which aligns with my college schedule for the next 3-6 months.

Technical Approach Summary:
- Implemented Selenium WebDriver with Chrome automation
- Used environment variables for secure credential management
- Implemented explicit waits for reliable element interaction
- Created modular, maintainable code structure
- Automated screenshot capture for verification
- Developed email automation system as per requirements

I am excited about the opportunity to contribute to your team and look forward to discussing my application further.

Best regards,
{candidate_name}
"""

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Cc'] = cc_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    attachments = ['form_confirmation.png', 'resume.pdf', 'Technical Documentation.docx']

    for file_path in attachments:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    filename = os.path.basename(file_path)
                    part.add_header('Content-Disposition', f'attachment; filename= {filename}')
                    msg.attach(part)
                print(f"Attached: {file_path}")
            except Exception as e:
                print(f"Error attaching {file_path}: {str(e)}")
        else:
            print(f"Warning: {file_path} not found")

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        recipients = [to_email, cc_email]
        server.send_message(msg)
        server.quit()

        print("\nEmail sent successfully!")
        print(f"To: {to_email}")
        print(f"Cc: {cc_email}")
        print(f"Subject: {subject}")

    except Exception as e:
        print(f"\nError sending email: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Ensure you're using a Gmail App Password, not your regular password")
        print("2. Enable 2-Factor Authentication in your Google Account")
        print("3. Generate an App Password from Google Account Settings")
        print("4. Check your internet connection")


if __name__ == "__main__":
    print("Starting email submission process...")
    print("=" * 50)
    send_assignment_email()
    print("=" * 50)