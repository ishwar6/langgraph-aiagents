"""CLI for running the JobHuntAgent end-to-end.

The script expects environment variables with credentials for Google Sheets
and SMTP. A very small set of templates is included for demonstration purposes.
"""
import os
from agents.job_hunt import JobHuntAgent

TEMPLATES = {
    "software": ("Application for Software Role", "Hello {Name},\nI am applying for the software position."),
    "default": ("Job Application", "Hello {Name},\nPlease consider my application."),
}

def main() -> None:
    agent = JobHuntAgent(
        os.environ["GOOGLE_CREDS_FILE"],
        os.environ["SHEET_KEY"],
        os.environ["SMTP_SERVER"],
        int(os.environ.get("SMTP_PORT", 587)),
        os.environ["SMTP_USER"],
        os.environ["SMTP_PASSWORD"],
    )
    sent = agent.run(TEMPLATES)
    print(f"Sent {sent} emails.")


if __name__ == "__main__":  # pragma: no cover - simple script
    main()
