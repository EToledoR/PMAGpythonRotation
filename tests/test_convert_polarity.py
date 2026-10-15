
import pandas as pd
import pytest

from cur_calc_plot.curator_aux_magic import convert_polarity


@pytest.fixture
def directions():
    """Minimal dataset with one normal and two reverse directions."""
    return pd.DataFrame(
        {
            "minc": [30.0, -20.0, -45.0],
            "mdec": [10.0, 30.0, 250.0],
        }
    )


def test_declining_conversion_is_skipped_when_user_answers_no(
    directions, monkeypatch
):
    monkeypatch.setattr("builtins.input", lambda _: "N")

    result = convert_polarity(directions)

    # Reverse directions must remain unchanged when conversion is declined.
    pd.testing.assert_series_equal(result["minc"], directions["minc"])
    pd.testing.assert_series_equal(result["mdec"], directions["mdec"])

    assert result["Polarity"].tolist() == ["Normal", "Reverse", "Reverse"]


def test_reverse_directions_are_converted_when_user_answers_yes(
    directions, monkeypatch
):
    monkeypatch.setattr("builtins.input", lambda _: "Y")

    result = convert_polarity(directions)

    assert result["minc"].tolist() == [30.0, 20.0, 45.0]
    assert result["mdec"].tolist() == [10.0, 210.0, 70.0]
    assert result["Polarity"].tolist() == ["Normal", "Normal", "Normal"]


def test_conversion_is_not_requested_when_all_directions_are_normal(
    monkeypatch,
):
    directions = pd.DataFrame(
        {
            "minc": [10.0, 20.0],
            "mdec": [30.0, 250.0],
        }
    )

    def unexpected_input(_):
        pytest.fail("The function should not prompt when no reverse directions exist.")

    monkeypatch.setattr("builtins.input", unexpected_input)

    result = convert_polarity(directions)

    assert result["Polarity"].tolist() == ["Normal", "Normal"]
