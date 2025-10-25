import os
import sys
import subprocess
from pathlib import Path


class QuickStart:
    def __init__(self):
        self.project_root = Path.cwd()
        self.steps_completed = []

    def print_header(self, text):
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60 + "\n")

    def print_step(self, step_num, description):
        print(f"\n[Step {step_num}] {description}")
        print("-" * 60)

    def check_python_version(self):
        self.print_step(1, "Checking Python Version")
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
            return True
        else:
            print(f"✗ Python 3.8+ required. Current: {version.major}.{version.minor}")
            return False

    def check_env_file(self):
        self.print_step(2, "Checking Environment Configuration")
        env_path = self.project_root / '.env'
        env_example_path = self.project_root / '.env.example'

        if not env_path.exists():
            print("✗ .env file not found")
            if env_example_path.exists():
                print("\nℹ Copy .env.example to .env and fill in your details:")
                print("  cp .env.example .env")
            return False

        print("✓ .env file found")

        with open(env_path, 'r') as f:
            content = f.read()
            required_vars = [
                'FORM_URL', 'FULL_NAME', 'CONTACT_NUMBER',
                'EMAIL_ID', 'SENDER_EMAIL', 'SENDER_PASSWORD'
            ]
            missing = []
            for var in required_vars:
                if var not in content or f'{var}=' in content:
                    missing.append(var)

            if missing:
                print(f"⚠ Warning: These variables might be empty: {', '.join(missing)}")
                return False

        print("✓ Environment variables configured")
        return True

    def check_dependencies(self):
        self.print_step(3, "Checking Dependencies")
        try:
            import selenium
            import flask
            from dotenv import load_dotenv
            print("✓ All dependencies installed")
            return True
        except ImportError as e:
            print(f"✗ Missing dependency: {e.name}")
            print("\nInstall dependencies:")
            print("  pip install -r requirements.txt")
            return False

    def check_resume(self):
        self.print_step(4, "Checking Resume File")
        resume_path = self.project_root / 'resume.pdf'
        if resume_path.exists():
            size_mb = resume_path.stat().st_size / (1024 * 1024)
            print(f"✓ resume.pdf found ({size_mb:.2f} MB)")
            return True
        else:
            print("✗ resume.pdf not found in project root")
            print("\nℹ Place your resume as 'resume.pdf' in the project directory")
            return False

    def run_form_automation(self):
        self.print_step(5, "Running Form Automation")
        print("This will open Chrome and fill the form automatically...")
        response = input("\nProceed with form automation? (y/n): ")

        if response.lower() == 'y':
            try:
                print("\nStarting automation...")
                result = subprocess.run(
                    [sys.executable, 'form_automation.py'],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    print("✓ Form automation completed successfully")
                    print("\nCheck for:")
                    print("  - form_confirmation.png")
                    print("  - form_filled_before_submit.png")
                    return True
                else:
                    print(f"✗ Automation failed: {result.stderr}")
                    return False
            except Exception as e:
                print(f"✗ Error running automation: {str(e)}")
                return False
        else:
            print("⊘ Skipped form automation")
            return False

    def verify_screenshots(self):
        self.print_step(6, "Verifying Screenshots")
        confirmation = self.project_root / 'form_confirmation.png'

        if confirmation.exists():
            print("✓ form_confirmation.png found")
            return True
        else:
            print("✗ form_confirmation.png not found")
            print("\nℹ Run form automation first to generate screenshot")
            return False

    def setup_email(self):
        self.print_step(7, "Email Submission Setup")
        print("\nChoose email sending method:")
        print("1. Flask Web Interface (Recommended)")
        print("2. Simple Python Script")
        print("3. Skip for now")

        choice = input("\nEnter choice (1/2/3): ")

        if choice == '1':
            print("\nStarting Flask server...")
            print("Open browser to: http://localhost:5000")
            print("\nPress Ctrl+C to stop server")
            try:
                subprocess.run([sys.executable, 'email_sender.py'])
            except KeyboardInterrupt:
                print("\n\nServer stopped")
        elif choice == '2':
            print("\nℹ Before running, update the GitHub link in send_email_simple.py")
            response = input("Ready to send? (y/n): ")
            if response.lower() == 'y':
                subprocess.run([sys.executable, 'send_email_simple.py'])
        else:
            print("⊘ Skipped email sending")

    def show_final_checklist(self):
        self.print_header("FINAL SUBMISSION CHECKLIST")

        checklist = [
            "Form successfully filled and submitted",
            "Screenshots generated (form_confirmation.png)",
            "Code uploaded to GitHub repository",
            ".env file NOT uploaded (check .gitignore)",
            "README.md is comprehensive",
            "requirements.txt includes all dependencies",
            "resume.pdf is ready",
            "Email sent to tech@themedius.ai",
            "CC sent to hr@themedius.ai",
            "Subject: Python (Selenium) Assignment - [Your Name]",
            "Availability mentioned: 4 PM - 10 PM",
            "GitHub repository link included",
            "All attachments verified"
        ]

        for i, item in enumerate(checklist, 1):
            print(f"{i:2d}. [ ] {item}")

        print("\n" + "=" * 60)
        print("Review this checklist before final submission!")
        print("=" * 60)

    def run(self):
        self.print_header("GOOGLE FORM AUTOMATION - QUICK START")

        checks = [
            ("Python Version", self.check_python_version),
            ("Environment Config", self.check_env_file),
            ("Dependencies", self.check_dependencies),
            ("Resume File", self.check_resume),
        ]

        all_passed = True
        for name, check_func in checks:
            if not check_func():
                all_passed = False

        if not all_passed:
            print("\n" + "=" * 60)
            print("⚠ Please fix the issues above before proceeding")
            print("=" * 60)
            return

        print("\n" + "=" * 60)
        print("✓ All prerequisite checks passed!")
        print("=" * 60)

        if self.run_form_automation():
            self.verify_screenshots()

        self.setup_email()

        self.show_final_checklist()

        print("\n🎉 Setup complete! Good luck with your assignment!")


if __name__ == "__main__":
    quick_start = QuickStart()
    quick_start.run()