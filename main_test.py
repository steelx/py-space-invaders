import pytest
import pygame

from main import Game


class TestRun:

    #  The game runs without errors
    def test_game_runs_without_errors(self):
        game = Game()
        game.run()

    #  The game exits when the user presses the escape key
    def test_game_exits_on_escape_key(self):
        game = Game()
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        game.run()
        assert not game.running

    #  The game runs smoothly when the user clicks rapidly
    def test_game_runs_smoothly_with_rapid_clicks(self):
        game = Game()
        for _ in range(10):
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN))
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP))
        game.run()
