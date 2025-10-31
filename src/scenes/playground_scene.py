import numpy as np
import pygame

from src.plugins.client import GameEvent
from src.plugins.event import EventManager
from src.plugins.scene import SceneBase


def draw_function(
    screen,
    func,
    x_range: tuple[float, float],
):
    width, height = screen.get_size()
    x_min, x_max = x_range
    y_range = None
    offset_x, offset_y = (50, 30)
    color = ((255, 0, 0),)
    margin = 0.25

    # 自動計算 y 範圍
    if y_range is None:
        x_samples = np.linspace(x_min, x_max, 100)
        y_values = []
        for x in x_samples:
            try:
                y_values.append(func(x))
            except Exception:
                pass
        if y_values:
            y_min = min(y_values)
            y_max = max(y_values)
            padding = (y_max - y_min) * 0.1
            y_range = (y_min - padding, y_max + padding)
        else:
            y_range = (-10, 10)

    y_min, y_max = y_range

    # 計算內邊距（讓座標軸與邊界有距離）
    x_margin = (x_max - x_min) * margin
    y_margin = (y_max - y_min) * margin

    # 擴展顯示範圍
    display_x_min = x_min - x_margin
    display_x_max = x_max + x_margin
    display_y_min = y_min - y_margin
    display_y_max = y_max + y_margin

    # 座標轉換函數（使用擴展後的範圍）
    def world_to_screen(x, y):
        px = (
            int((x - display_x_min) / (display_x_max - display_x_min) * width)
            + offset_x
        )
        py = (
            int(height - (y - display_y_min) / (display_y_max - display_y_min) * height)
            + offset_y
        )
        return px, py

    # 1. 繪製背景（繪圖區域）
    plot_rect = pygame.Rect(offset_x, offset_y, width, height)
    pygame.draw.rect(screen, (255, 255, 255), plot_rect)

    # 2. 繪製網格線
    grid_color = (220, 220, 220)

    # 垂直網格線 (x 軸方向)
    x_step = (x_max - x_min) / 10
    for i in range(11):
        x = x_min + i * x_step
        px, _ = world_to_screen(x, 0)
        pygame.draw.line(screen, grid_color, (px, offset_y), (px, offset_y + height), 1)

    # 水平網格線 (y 軸方向)
    y_step = (y_max - y_min) / 10
    for i in range(11):
        y = y_min + i * y_step
        _, py = world_to_screen(0, y)
        pygame.draw.line(screen, grid_color, (offset_x, py), (offset_x + width, py), 1)

    # 3. 繪製座標軸
    axis_color = (0, 0, 0)

    # X 軸 (y=0 的位置)
    if display_y_min <= 0 <= display_y_max:
        _, y_axis_pos = world_to_screen(0, 0)
        pygame.draw.line(
            screen,
            axis_color,
            (offset_x, y_axis_pos),
            (offset_x + width, y_axis_pos),
            2,
        )

    # Y 軸 (x=0 的位置)
    if display_x_min <= 0 <= display_x_max:
        x_axis_pos, _ = world_to_screen(0, 0)
        pygame.draw.line(
            screen,
            axis_color,
            (x_axis_pos, offset_y),
            (x_axis_pos, offset_y + height),
            2,
        )

    # 4. 繪製座標值標記
    font = pygame.font.Font(None, 20)

    # X 軸標記
    for i in range(11):
        x = x_min + i * x_step
        px, py = world_to_screen(x, 0)

        # 確保標記在螢幕內
        if display_y_min <= 0 <= display_y_max:
            mark_y = py
        else:
            mark_y = offset_y + height - 10

        # 繪製刻度線
        pygame.draw.line(screen, axis_color, (px, mark_y - 5), (px, mark_y + 5), 2)

        # 繪製數字
        text = font.render(f"{x:.1f}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(px, mark_y + 15))
        screen.blit(text, text_rect)

    # Y 軸標記
    for i in range(11):
        y = y_min + i * y_step
        px, py = world_to_screen(0, y)

        # 確保標記在螢幕內
        if display_x_min <= 0 <= display_x_max:
            mark_x = px
        else:
            mark_x = offset_x + 30

        # 繪製刻度線
        pygame.draw.line(screen, axis_color, (mark_x - 5, py), (mark_x + 5, py), 2)

        # 繪製數字
        text = font.render(f"{y:.1f}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(mark_x - 20, py))
        screen.blit(text, text_rect)

    # 5. 繪製函數曲線
    points = []
    for px in range(width):
        x = display_x_min + (display_x_max - display_x_min) * px / width
        try:
            y = func(x)
            if display_y_min <= y <= display_y_max:
                plot_x, plot_y = world_to_screen(x, y)
                points.append((plot_x, plot_y))
            else:
                if len(points) > 1:
                    pygame.draw.lines(screen, color, False, points, 2)
                points = []
        except Exception:
            if len(points) > 1:
                pygame.draw.lines(screen, color, False, points, 2)
            points = []

    if len(points) > 1:
        pygame.draw.lines(screen, color, False, points, 2)

    # 6. 繪製邊框
    pygame.draw.rect(screen, (0, 0, 0), plot_rect, 2)


def speed_func(agility: float) -> float:
    import math

    base_speed = 1.2  # 基礎 1 pixel

    if agility < 10:
        agility = 10  # 最低10

    # 調整係數來控制最大速度
    multiplier = 4.0  # 控制最大加成幅度
    divisor = 80  # 控制邊際遞減速度

    bonus = multiplier * math.log(1 + (agility - 10) / divisor)

    return base_speed + bonus


class PlaygroundScene(SceneBase):
    def __init__(self, events: EventManager):
        super().__init__(events=events)

    def onkeydown(self, keydown: pygame.event.Event):
        if keydown.key == pygame.K_ESCAPE:
            self.events.emit(GameEvent.Quitting)

    def update(self, dt: float):
        pass

    def draw(self, screen: pygame.Surface):
        draw_function(screen, speed_func, x_range=(10, 1000))
