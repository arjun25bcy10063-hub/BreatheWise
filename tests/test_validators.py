from utils.validators import validate_advisory, validate_coordinates


def test_coordinates():
    validate_coordinates(28.6, 77.2)


def test_advisory():
    assert validate_advisory({
        "summary": "ok",
        "actions": ["a"],
        "outdoor_guidance": "ok",
        "personalization_reason": "ok",
    })
