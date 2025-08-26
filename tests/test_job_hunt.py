from unittest.mock import Mock
import pytest

from agents.job_hunt import JobHuntAgent


class DummySheet:
    def __init__(self, header, records):
        self.header = header
        # normalize records to include all headers, ignoring case
        self._records = [
            {h: r.get(h, r.get(h.lower(), "")) for h in header} for r in records
        ]

    def get_all_records(self):
        return self._records

    def row_values(self, row):
        if row == 1:
            return self.header
        return [self._records[row - 2].get(h, "") for h in self.header]

    def update_cell(self, row, col, value):
        self._records[row - 2][self.header[col - 1]] = value


def _agent_for(sheet):
    return JobHuntAgent(
        "creds.json",
        "sheet-key",
        "smtp.example.com",
        587,
        "user",
        "pass",
        sheet=sheet,
    )


def test_run_sends_emails_and_marks_status():
    sheet = DummySheet(
        ["Email", "Type", "Status", "Name"],
        [
            {"Email": "alice@example.com", "Type": "Software", "Name": "Alice"},
            {"email": "bob@example.com", "type": "default", "Name": "Bob"},
        ],
    )
    agent = _agent_for(sheet)
    agent._send_email = Mock()
    templates = {
        "software": ("Subject1 {Name}", "Body1 for {Name}"),
        "default": ("Subject2 {Name}", "Body2 for {Name}"),
    }
    sent = agent.run(templates)
    assert sent == 2
    agent._send_email.assert_any_call(
        "alice@example.com", "Subject1 Alice", "Body1 for Alice"
    )
    agent._send_email.assert_any_call(
        "bob@example.com", "Subject2 Bob", "Body2 for Bob"
    )
    assert sheet.get_all_records()[0]["Status"] == "Sent"
    assert sheet.get_all_records()[1]["Status"] == "Sent"


def test_skips_rows_with_sent_status():
    sheet = DummySheet(
        ["Email", "Type", "Status"],
        [
            {"Email": "charlie@example.com", "Type": "Software", "Status": "Sent"},
            {"Email": "dave@example.com", "Type": "Software", "Status": ""},
        ],
    )
    agent = _agent_for(sheet)
    agent._send_email = Mock()
    templates = {"software": ("S", "B")}
    sent = agent.run(templates)
    assert sent == 1
    agent._send_email.assert_called_once_with("dave@example.com", "S", "B")


def test_missing_columns_raise():
    sheet = DummySheet(["Email"], [{"Email": "eve@example.com"}])
    agent = _agent_for(sheet)
    with pytest.raises(ValueError):
        agent.run({})
