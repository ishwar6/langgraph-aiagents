"""Agent for sending job application emails from Google Sheets.

The agent fetches contacts from a sheet, chooses a template based on the
vacancy type, formats the template with row values and dispatches the email.
Rows that already contain ``Sent`` in the status column are skipped and marked
once an email is successfully delivered.
"""
from typing import Dict, Tuple, Optional
import smtplib
from email.mime.text import MIMEText


class JobHuntAgent:
    """Reads a sheet and emails contacts based on vacancy type."""

    def __init__(
        self,
        creds_file: str,
        sheet_key: str,
        smtp_server: str,
        smtp_port: int,
        smtp_user: str,
        smtp_password: str,
        sheet: Optional[object] = None,
    ) -> None:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/drive.readonly",
        ]
        if sheet is None:
            import gspread
            from google.oauth2.service_account import Credentials

            credentials = Credentials.from_service_account_file(creds_file, scopes=scopes)
            client = gspread.authorize(credentials)
            sheet = client.open_by_key(sheet_key).sheet1
        self.sheet = sheet
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    def _send_email(self, recipient: str, subject: str, body: str) -> None:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.smtp_user
        msg["To"] = recipient
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.smtp_user, [recipient], msg.as_string())

    def run(
        self,
        templates: Dict[str, Tuple[str, str]],
        email_column: str = "Email",
        type_column: str = "Type",
        status_column: str = "Status",
    ) -> int:
        """Reads contacts and sends emails using templates.

        Args:
            templates: Map of vacancy type to ``(subject, body)`` templates.
            email_column: Column name containing email addresses.
            type_column: Column describing the vacancy type.
            status_column: Column used to mark already-contacted rows.

        Returns:
            Number of successfully dispatched emails.
        """

        header = [h.lower() for h in self.sheet.row_values(1)]
        try:
            email_idx = header.index(email_column.lower())
            type_idx = header.index(type_column.lower())
        except ValueError as exc:  # pragma: no cover - defensive programming
            raise ValueError("Required column missing") from exc

        status_idx = header.index(status_column.lower()) if status_column.lower() in header else None

        rows = self.sheet.get_all_records()
        sent = 0
        for row_num, row in enumerate(rows, start=2):
            lowered = {k.lower(): v for k, v in row.items()}
            email = lowered.get(email_column.lower())
            job_type = lowered.get(type_column.lower())
            status = lowered.get(status_column.lower()) if status_idx is not None else None
            if not email or not job_type or (status and str(status).strip().lower() == "sent"):
                continue
            key = str(job_type).strip().lower()
            subject_tpl, body_tpl = templates.get(
                key, templates.get("default", ("Job Application", ""))
            )
            subject = subject_tpl.format(**row)
            body = body_tpl.format(**row)
            self._send_email(email, subject, body)
            sent += 1
            if status_idx is not None:
                self.sheet.update_cell(row_num, status_idx + 1, "Sent")
        return sent
