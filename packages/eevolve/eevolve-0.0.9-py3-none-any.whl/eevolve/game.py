import math
import sys
from typing import Iterable

import numpy
import pygame

from eevolve.agent import Agent
from eevolve.board import Board
from eevolve.generator import PositionGenerator, ColorGenerator
from eevolve.task import Task, FrameEndTask, CollisionTask, AgentTask, BoardTask, PairTask
from eevolve.loader import Loader
from eevolve.constants import TOP_LEFT, LOWEST_TASK_PRIORITY, HIGHEST_TASK_PRIORITY


class Game:
    def __init__(self,
                 display_size: tuple[float | int, float | int],
                 screen_size: tuple[float | int, float | int],
                 window_caption: str,
                 display_background: str | pygame.Surface | numpy.ndarray,
                 board_sectors_number: int,
                 draw_sectors: bool = False,
                 reset_on: bool = True,
                 fps_limit: int = 300):
        self._task_priorities = LOWEST_TASK_PRIORITY - HIGHEST_TASK_PRIORITY + 1

        self._display = pygame.Surface(display_size)
        self._screen = pygame.display.set_mode(screen_size)
        self._clock = pygame.Clock()

        self._display_size = display_size
        self._screen_size = screen_size
        self._window_caption = window_caption

        self._agents_list = []
        self._tasks: list[list[Task]] = [[] for _ in range(self._task_priorities)]

        self._delta_time = 0.0
        self._time = 0.0

        self._background = Loader.load_surface(display_background, display_size)
        self._board = Board(
            (math.ceil(self.display_size[0] / board_sectors_number),
             math.ceil(self.display_size[1] / board_sectors_number)),
            board_sectors_number)
        self._sectors_number = board_sectors_number
        self._sector_rects = []
        self._sector_colors = []

        self._to_draw_sectors = draw_sectors

        self._game_running = True
        self._blit_function = None

        self._reset_on = reset_on
        self._fps_limit = fps_limit

        for agent in self._agents_list:
            self._board.add_agent(agent)

    def _init_internal_tasks(self) -> None:
        self.add_task(FrameEndTask(self._timer, priority=HIGHEST_TASK_PRIORITY))
        self.add_task(FrameEndTask(self._board.check_collision, priority=HIGHEST_TASK_PRIORITY))
        self.add_task(FrameEndTask(self._board.check_sector_pairs, priority=HIGHEST_TASK_PRIORITY))
        self.add_task(FrameEndTask(self._check_dead, priority=LOWEST_TASK_PRIORITY))
        self.add_task(FrameEndTask(self._draw, priority=LOWEST_TASK_PRIORITY))
        self.add_task(FrameEndTask(self._update_display, priority=LOWEST_TASK_PRIORITY))

    def _draw(self) -> None:
        self._display.blit(self._background, TOP_LEFT)

        for agent in self._board.agents:
            agent.draw(self._display)

        if self._to_draw_sectors:
            self._draw_sectors()

    def _do_tasks(self) -> None:
        to_remove = []

        # print(f"time: {self._time / 1000.0} " + "-" * 64)

        for priority in range(self._task_priorities):
            for task in self._tasks[priority]:
                task.timer += self._delta_time

                if task.timer >= task.period:
                    # print(task)

                    if isinstance(task, CollisionTask):
                        for collision_pair in self._board.collided:
                            task(collision_pair)
                    elif isinstance(task, AgentTask):
                        for agent in self._board.agents:
                            task(agent)
                    elif isinstance(task, BoardTask):
                        task(self._board)
                    elif isinstance(task, PairTask):
                        for pair in self._board.sector_pairs:
                            task(pair)
                    elif isinstance(task, FrameEndTask):
                        task()
                    else:
                        task()
                else:
                    continue

                if task.is_dead:
                    to_remove.append(task)
                task.timer = 0

        self.remove_tasks(to_remove)

    def _draw_sectors(self) -> None:
        if len(self._sector_rects) == 0:
            width, height = self._board.sector_size

            for i in range(self._sectors_number):
                for j in range(self._sectors_number):
                    self._sector_rects.append(pygame.Rect((i * width, j * height), (width, height)))

            for color in ColorGenerator.random(self._sectors_number ** 2):
                self._sector_colors.append(color)

        for i, row in enumerate(self._board.agents_board):
            for j, sector in enumerate(row):
                index = i * self._sectors_number + j
                color = self._sector_colors[index]

                pygame.draw.rect(self._display, color, self._sector_rects[index], width=1)

                for agent in sector:
                    pygame.draw.rect(self._display, color, agent.rect, width=1)

    def _check_dead(self) -> None:
        self._board.check_dead()

        for agent in self._board.dead:
            self._board.remove_agent(agent)

    def _update_display(self) -> None:
        self._blit_function()
        self._clock.tick(self._fps_limit)
        pygame.display.update()

    def _timer(self) -> None:
        self._delta_time = self._clock.get_time()
        self._time += self._delta_time

    def run(self) -> None:
        self._init_internal_tasks()

        if self._display_size != self._screen_size:
            self._blit_function = lambda: self._screen.blit(
                pygame.transform.scale(self._display, self._screen_size), TOP_LEFT)
        else:
            self._blit_function = lambda: self._screen.blit(self._display, TOP_LEFT)

        pygame.display.set_caption(self._window_caption)

        while self._game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self._to_draw_sectors = not self._to_draw_sectors

            self._do_tasks()

    def add_task(self, task: Task) -> None:
        if not isinstance(task, Task):
            raise ValueError("Argument must be instance of Task")

        self._tasks[task.priority].append(task)

    def add_tasks(self, tasks: Iterable[Task]) -> None:
        for task in tasks:
            self.add_task(task)

    def remove_task(self, task: Task) -> None:
        if task not in self._tasks:
            print(f"[WARNING] Trying to remove {task} which not in tasks list!")
            return

        self._tasks[task.priority].remove(task)

    def remove_tasks(self, tasks: Iterable[Task]) -> None:
        for task in tasks:
            self.remove_task(task)

    def add_agents(self, copies_number: int, agent_generator: Iterable[Agent],
                   position_generator: Iterable[tuple[int | float, int | float] | numpy.ndarray] = None) -> None:
        if position_generator is None:
            position_generator = PositionGenerator.uniform(self, copies_number)

        for agent, position in zip(agent_generator, position_generator):
            agent.move_to(position)
            self._board.add_agent(agent)

    def add_agent(self, agent: Agent) -> None:
        self._board.add_agent(agent)

    @property
    def display_size(self) -> tuple[float | int, float | int]:
        return self._display_size

    @property
    def screen_size(self) -> tuple[float | int, float | int]:
        return self._screen_size

    @property
    def sectors_number(self) -> int:
        return self._sectors_number

    @property
    def window_caption(self) -> str:
        return self._window_caption

    @property
    def display_background(self) -> pygame.Surface | None:
        return self._background

    @display_background.setter
    def display_background(self, display_background: str | pygame.Surface | numpy.ndarray) -> None:
        self._background = Loader.load_surface(display_background, self._display_size)

    @property
    def board(self) -> Board | None:
        return self._board

    @property
    def collided_agents(self):
        return self._board.collided

    @property
    def agents(self) -> Iterable[Agent]:
        return self._board.agents
