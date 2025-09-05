# test_life.py
import pytest
import numpy as np
from life import update_board

def test_blinker():
    """Tests the period-2 oscillator."""
    # Blinker horizontal (phase 1)
    horizontal = np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ])
    # After one step, it should be vertical (phase 2)
    expected_vertical = np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ])
    
    result = update_board(horizontal)
    assert np.array_equal(result, expected_vertical), "Blinker test failed: horizontal -> vertical"

    # Test that it returns to horizontal after second step
    result_phase_2 = update_board(result)
    assert np.array_equal(result_phase_2, horizontal), "Blinker test failed: vertical -> horizontal"

def test_stable_block():
    """Tests a still life (should not change)."""
    block = np.array([
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ])
    result = update_board(block)
    assert np.array_equal(result, block), "Stable block changed unexpectedly."

def test_underpopulation():
    """Tests that a live cell with 0 neighbors dies."""
    single_cell = np.array([
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ])
    expected = np.zeros((3, 3), dtype=int)
    result = update_board(single_cell)
    assert np.array_equal(result, expected), "Underpopulation test failed: single cell should die."