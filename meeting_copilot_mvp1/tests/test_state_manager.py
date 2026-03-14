from app.schemas import SummaryPayload
from app.services.state_manager import MeetingState


def test_state_aggregation_merges_unique_items():
    state = MeetingState(meeting_title="Test")
    payload_1 = SummaryPayload(
        rolling_summary="one",
        decisions=["Use SQLite"],
        key_discussion_points=["Storage"],
    )
    payload_2 = SummaryPayload(
        rolling_summary="two",
        decisions=["Use SQLite", "Use Streamlit"],
        key_discussion_points=["Storage", "UI"],
    )

    state.update_from_summary(payload_1)
    state.update_from_summary(payload_2)

    assert state.decisions == ["Use SQLite", "Use Streamlit"]
    assert state.key_discussion_points == ["Storage", "UI"]
