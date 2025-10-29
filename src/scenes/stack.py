from typing import TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    from src.scenes.base import Scene

logger = structlog.get_logger(__name__)


class SceneStack:
    """Container for managing scene stack"""

    def __init__(self):
        self._stack: list["Scene"] = []

    def push(self, scene: "Scene"):
        """Push a new scene onto the stack"""
        self._stack.append(scene)
        logger.debug(
            "Scene pushed to stack",
            scene=scene.__class__.__name__,
            stack_size=len(self._stack),
        )

    def pop(self) -> "Scene | None":
        """Pop the current scene from the stack"""
        if not self._stack:
            logger.warning("Cannot pop from empty scene stack")
            return None

        scene = self._stack.pop()
        logger.debug(
            "Scene popped from stack",
            scene=scene.__class__.__name__,
            stack_size=len(self._stack),
        )
        return scene

    def replace(self, scene: "Scene"):
        """Replace the current scene with a new one"""
        if self._stack:
            old_scene = self._stack.pop()
            logger.debug(
                "Scene replaced",
                old=old_scene.__class__.__name__,
                new=scene.__class__.__name__,
            )
        else:
            logger.debug("Scene added to empty stack", scene=scene.__class__.__name__)

        self._stack.append(scene)

    def peek(self) -> "Scene | None":
        """Get the current scene without removing it"""
        return self._stack[-1] if self._stack else None

    def clear(self):
        """Clear all scenes from the stack"""
        count = len(self._stack)
        self._stack.clear()
        logger.debug("Scene stack cleared", cleared_count=count)

    def is_empty(self) -> bool:
        """Check if the stack is empty"""
        return len(self._stack) == 0

    def size(self) -> int:
        """Get the number of scenes in the stack"""
        return len(self._stack)
