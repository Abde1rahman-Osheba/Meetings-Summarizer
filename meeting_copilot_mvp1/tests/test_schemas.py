from app.schemas import parse_json_payload, parse_summary_payload


def test_parse_json_payload_valid():
    payload = parse_json_payload('{"x": 1}')
    assert payload["x"] == 1


def test_parse_summary_payload_valid():
    text = """
    {
      "rolling_summary": "Team aligned on release goals",
      "key_discussion_points": ["timeline"],
      "decisions": ["ship Friday"],
      "action_items": [{"description":"prepare QA","owner":"unknown","due_date":"unknown","status":"open"}],
      "blockers_risks": ["env drift"],
      "open_questions": ["need extra headcount?"]
    }
    """
    parsed = parse_summary_payload(text)
    assert parsed.decisions == ["ship Friday"]
