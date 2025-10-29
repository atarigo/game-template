from typing import TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    from src.scenes.base import Scene

logger = structlog.get_logger(__name__)


class SceneLifecycle:
    """Coordinator for scene lifecycle events"""

    @staticmethod
    def switch(old_scene: "Scene | None", new_scene: "Scene"):
        """Handle lifecycle for switching scenes"""
        if old_scene:
            logger.info("Scene exiting", scene=old_scene.__class__.__name__)
            old_scene.on_exit()

        logger.info("Scene entering", scene=new_scene.__class__.__name__)
        new_scene.on_enter()

    @staticmethod
    def push(current_scene: "Scene | None", new_scene: "Scene"):
        """Handle lifecycle for pushing a new scene onto stack"""
        if current_scene:
            logger.info("Scene pausing", scene=current_scene.__class__.__name__)
            current_scene.on_pause()

        logger.info("Scene entering", scene=new_scene.__class__.__name__)
        new_scene.on_enter()

    @staticmethod
    def pop(exiting_scene: "Scene", previous_scene: "Scene | None"):
        """Handle lifecycle for popping a scene from stack"""
        logger.info("Scene exiting", scene=exiting_scene.__class__.__name__)
        exiting_scene.on_exit()

        if previous_scene:
            logger.info("Scene resuming", scene=previous_scene.__class__.__name__)
            previous_scene.on_resume()
