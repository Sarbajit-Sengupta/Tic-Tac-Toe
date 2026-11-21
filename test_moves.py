import contextlib
import io
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import MagicMock, patch
import numpy as np


class MoveTests(unittest.TestCase):
    def test_draw_and_offboard_clicks(self):
        board = np.array([[1, 2, 1], [1, 2, 2], [2, 1, 0]])
        pygame = MagicMock()
        pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN = 1, 2, 3
        pygame.event.get.return_value = [
            types.SimpleNamespace(type=2, pos=(600, 0)),
            types.SimpleNamespace(type=2, pos=(-1, 0)),
            types.SimpleNamespace(type=2, pos=(450, 450)),
            types.SimpleNamespace(type=2, pos=(10, 10)),
            types.SimpleNamespace(type=1)]
        namespace = {'__name__': '__test__'}
        source = Path(__file__).with_name('main.py').read_text()
        with patch.dict(sys.modules, {'pygame': pygame}), patch.object(np, 'zeros', return_value=board), \
                contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit):
                exec(compile(source, 'main.py', 'exec'), namespace)
        self.assertTrue(namespace['game_over'])
        self.assertEqual(board[2, 2], 1)
        self.assertFalse(namespace['available_square'](-1, 0))
        self.assertFalse(namespace['available_square'](0, 3))


if __name__ == '__main__':
    unittest.main()
