'''Module to test the project.background.model module'''
import pytest
from unittest.mock import Mock, patch
from background.model import Background

@pytest.fixture
def mock_background():
    with patch('background.model.random') as mock_random, patch('background.model.pyxel') as mock_pyxel:
        mock_pyxel.width = 100
        mock_pyxel.height = 100
        mock_random.return_value = 0.5
        background = Background()
        yield background

def test_init(mock_background):
    assert len(mock_background.star_list) == mock_background.STAR_COUNT
    for star in mock_background.star_list:
        x, y, speed = star
        assert x == 0.5 * mock_background.width
        assert y == 0.5 * mock_background.height
        assert speed == 0.5 * 1.5 + 1

@patch('background.model.pyxel')
def test_update(mock_pyxel, mock_background):
    mock_pyxel.height = 100

    mock_background.update()
    for star in mock_background.star_list:
        x, y, speed = star
        assert y < mock_pyxel.height

@patch('background.model.pyxel')
def test_draw(mock_pyxel, mock_background):
    mock_background.draw()

    mock_pyxel.pset.assert_called()
    for star in mock_background.star_list:
        x, y, speed = star
        color = mock_background.STAR_COLOR_HIGH if speed > 1.8 \
            else mock_background.STAR_COLOR_LOW
        mock_pyxel.pset.assert_any_call(x, y, color)
