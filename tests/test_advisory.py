from agents.advisory_agent import _extract_json


def test_extract_json_from_plain_text():
    text = '{"summary":"ok","actions":["a"],"outdoor_guidance":"x","personalization_reason":"y"}'
    result = _extract_json(text)
    assert result["summary"] == "ok"
