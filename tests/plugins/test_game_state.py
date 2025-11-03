import pytest

from plugins.client.game_state import GameEvent, GameState, GameStateManager
from plugins.event import EventManager


@pytest.fixture(scope="function")
def event_manager():
    return EventManager()


def test_game_event():
    assert "Running" in GameEvent.__members__
    assert "Paused" in GameEvent.__members__
    assert "Unpaused" in GameEvent.__members__
    assert "Quitting" in GameEvent.__members__


def test_game_state():
    assert "Running" in GameState.__members__
    assert "Paused" in GameState.__members__
    assert "Quitting" in GameState.__members__


def test_game_state_manager(event_manager):
    state = GameStateManager(events=event_manager)
    assert state.current == GameState.Running

    event_manager.emit(GameEvent.Paused)
    event_manager.process_events()
    assert state.current == GameState.Paused

    event_manager.emit(GameEvent.Unpaused)
    event_manager.process_events()
    assert state.current == GameState.Running

    event_manager.emit(GameEvent.Quitting)
    event_manager.process_events()
    assert state.current == GameState.Quitting
