import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from P2048.Logic import Logic as Logic2048
from TetrisGame.Logic import Logic as TetrisLogic


def test_2048_move_merges_left():
    logic = Logic2048()
    logic.mat = [
        [2, 1, 1, 1],
        [2, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
    ]

    changed = logic.move(Logic2048.LEFT)

    assert changed is True
    assert logic.mat[0][0] == 4
    assert sum(1 for col in logic.mat for value in col if value != 1) == 2


def test_2048_lost_state_on_full_locked_board():
    logic = Logic2048()
    logic.mat = [
        [2, 4, 2, 4],
        [4, 2, 4, 2],
        [2, 4, 2, 4],
        [4, 2, 4, 2],
    ]

    assert logic.get_current_state() == Logic2048.LOST


def test_tetris_reset_builds_empty_board():
    logic = TetrisLogic()

    assert len(logic.board) == logic.BOARD_HEIGHT
    assert all(len(row) == logic.BOARD_WIDTH for row in logic.board)
    assert logic.game_over is False
