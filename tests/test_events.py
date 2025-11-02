"""
EventManager Test Suite

This file contains comprehensive tests for the EventManager class.

Test Coverage:
--------------
Core Functionality:
  - test_subscribe_and_emit: Basic event subscription and emission
  - test_multiple_subscribers: Multiple handlers for same event
  - test_multiple_event_types: Different event types handling
  - test_unsubscribe: Removing event handlers
  - test_queue_ordering: FIFO queue processing order
  - test_clear_queue: Clearing the event queue

Error Handling:
  - test_unsubscribe_nonexistent_callback_raises_error: ValueError on invalid unsubscribe
  - test_callback_exception_propagates: Exception propagation from callbacks
  - test_partial_queue_processing_on_error: Queue state after error

Memory Management:
  - test_unsubscribe_cleans_empty_listeners: Auto-cleanup of empty listener lists

Data Handling:
  - test_callback_with_none_data: Support for None as event data
  - test_callback_with_complex_data: Support for complex data structures

Edge Cases:
  - test_emit_without_subscribers: Emit to non-existent event type
  - test_subscribe_same_callback_multiple_times: Duplicate subscriptions allowed
  - test_empty_queue_process: Processing empty queue
  - test_unsubscribe_from_empty_manager: Unsubscribe when no listeners exist
  - test_multiple_unsubscribe_same_callback: Multiple unsubscribe calls
  - test_resubscribe_after_unsubscribe: Re-subscribing after unsubscribe
"""

import pytest

from plugins.event import EventManager


def test_subscribe_and_emit():
    """Basic event subscription and emission"""
    manager = EventManager()
    results = []

    def handler(data):
        results.append(data)

    manager.subscribe("test_event", handler)
    manager.emit("test_event", "hello")
    manager.process_events()

    assert results == ["hello"]


def test_multiple_subscribers():
    """Multiple handlers for same event"""
    manager = EventManager()
    results = []

    def handler1(data):
        results.append(f"h1:{data}")

    def handler2(data):
        results.append(f"h2:{data}")

    manager.subscribe("test_event", handler1)
    manager.subscribe("test_event", handler2)
    manager.emit("test_event", "data")
    manager.process_events()

    assert results == ["h1:data", "h2:data"]


def test_multiple_event_types():
    """Different event types handling"""
    manager = EventManager()
    results = []

    def handler1(data):
        results.append(f"click:{data}")

    def handler2(data):
        results.append(f"hover:{data}")

    manager.subscribe("click", handler1)
    manager.subscribe("hover", handler2)

    manager.emit("click", 1)
    manager.emit("hover", 2)
    manager.emit("click", 3)
    manager.process_events()

    assert results == ["click:1", "hover:2", "click:3"]


def test_unsubscribe():
    """Removing event handlers"""
    manager = EventManager()
    results = []

    def handler(data):
        results.append(data)

    manager.subscribe("test_event", handler)
    manager.emit("test_event", "before")
    manager.process_events()

    manager.unsubscribe("test_event", handler)
    manager.emit("test_event", "after")
    manager.process_events()

    # Only "before" should be processed
    assert results == ["before"]


def test_unsubscribe_nonexistent_callback_raises_error():
    """ValueError on invalid unsubscribe"""
    manager = EventManager()

    def handler(data):
        pass

    manager.subscribe("test_event", handler)

    def other_handler(data):
        pass

    # Attempting to unsubscribe a non-subscribed callback should raise ValueError
    with pytest.raises(ValueError):
        manager.unsubscribe("test_event", other_handler)


def test_unsubscribe_cleans_empty_listeners():
    """Auto-cleanup of empty listener lists"""
    manager = EventManager()

    def handler(data):
        pass

    manager.subscribe("test_event", handler)
    assert "test_event" in manager.listeners

    manager.unsubscribe("test_event", handler)
    # Should clean up empty listener list
    assert "test_event" not in manager.listeners


def test_emit_without_subscribers():
    """Emit to non-existent event type"""
    manager = EventManager()
    manager.emit("nonexistent_event", "data")
    # Should not raise any exception
    manager.process_events()


def test_queue_ordering():
    """FIFO queue processing order"""
    manager = EventManager()
    results = []

    def handler(data):
        results.append(data)

    manager.subscribe("test_event", handler)

    manager.emit("test_event", 1)
    manager.emit("test_event", 2)
    manager.emit("test_event", 3)
    manager.process_events()

    assert results == [1, 2, 3]


def test_clear_queue():
    """Clearing the event queue"""
    manager = EventManager()
    results = []

    def handler(data):
        results.append(data)

    manager.subscribe("test_event", handler)

    manager.emit("test_event", 1)
    manager.emit("test_event", 2)
    manager.clear()
    manager.process_events()

    # Queue was cleared, should have no results
    assert results == []


def test_callback_with_none_data():
    """Support for None as event data"""
    manager = EventManager()
    results = []

    def handler(data):
        results.append(data)

    manager.subscribe("test_event", handler)
    manager.emit("test_event", None)
    manager.process_events()

    assert results == [None]


def test_callback_with_complex_data():
    """Support for complex data structures"""
    manager = EventManager()
    results = []

    def handler(data):
        results.append(data)

    manager.subscribe("test_event", handler)

    complex_data = {
        "type": "click",
        "position": (100, 200),
        "nested": {"value": 42},
    }
    manager.emit("test_event", complex_data)
    manager.process_events()

    assert results == [complex_data]


def test_callback_exception_propagates():
    """Exception propagation from callbacks"""
    manager = EventManager()

    def failing_handler(data):
        raise RuntimeError("Handler failed")

    manager.subscribe("test_event", failing_handler)
    manager.emit("test_event", "data")

    # By design, exceptions should propagate
    with pytest.raises(RuntimeError, match="Handler failed"):
        manager.process_events()


def test_subscribe_same_callback_multiple_times():
    """Duplicate subscriptions allowed"""
    manager = EventManager()
    results = []

    def handler(data):
        results.append(data)

    # Subscribe same handler twice
    manager.subscribe("test_event", handler)
    manager.subscribe("test_event", handler)

    manager.emit("test_event", "data")
    manager.process_events()

    # Should execute twice
    assert results == ["data", "data"]


def test_partial_queue_processing_on_error():
    """Queue state after error"""
    manager = EventManager()
    results = []

    def normal_handler(data):
        results.append(data)

    def failing_handler(data):
        raise RuntimeError("Failed")

    manager.subscribe("event1", normal_handler)
    manager.subscribe("event2", failing_handler)

    manager.emit("event1", "first")
    manager.emit("event2", "second")
    manager.emit("event1", "third")

    # Second event will fail
    with pytest.raises(RuntimeError):
        manager.process_events()

    # First event should be processed, third won't be (interrupted)
    assert results == ["first"]
    # Queue should still contain the third event
    assert len(manager.queue) == 1


def test_empty_queue_process():
    """Processing empty queue"""
    manager = EventManager()
    # Should not raise any exception
    manager.process_events()


def test_unsubscribe_from_empty_manager():
    """Unsubscribe when no listeners exist"""
    manager = EventManager()

    def handler(data):
        pass

    # Won't raise ValueError because event_type doesn't exist and will be skipped
    manager.unsubscribe("nonexistent", handler)


def test_multiple_unsubscribe_same_callback():
    """Multiple unsubscribe calls"""
    manager = EventManager()

    def handler(data):
        pass

    manager.subscribe("test_event", handler)
    manager.unsubscribe("test_event", handler)

    # Second unsubscribe should not error (event_type already cleaned up)
    manager.unsubscribe("test_event", handler)


def test_resubscribe_after_unsubscribe():
    """Re-subscribing after unsubscribe"""
    manager = EventManager()
    results = []

    def handler(data):
        results.append(data)

    manager.subscribe("test_event", handler)
    manager.unsubscribe("test_event", handler)
    manager.subscribe("test_event", handler)

    manager.emit("test_event", "data")
    manager.process_events()

    assert results == ["data"]
