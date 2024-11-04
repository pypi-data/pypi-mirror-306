from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from itertools import product


from weiqi.group import Group
from weiqi.position import Position
from weiqi.figure import Stone

TState = TypeVar("TState")
TFigure = TypeVar("TFigure")


class BaseBoard(ABC, Generic[TState, TFigure]):
    def __init__(self, size: int, figures: dict[Position, TFigure | None]):
        self._size = size
        self._figures = figures

        if not self._validate_available_size():
            raise ValueError("Not available size.")
        if not self._validate_positions():
            raise ValueError("Invalid positions.")
        if not self._is_square_board():
            raise ValueError("Board must be square.")
        if not self._validate_figures():
            raise ValueError("Invalid figures.")

    @property
    def figures(self) -> dict[Position, TFigure | None]:
        return self._figures

    @property
    def size(self) -> int:
        return self._size

    def _is_square_board(self) -> bool:
        return len(self.figures) == self._size**2

    def _validate_positions(self) -> bool:
        return all(
            position.x < self._size and position.y < self._size
            for position in self.figures.keys()
        )

    def position_in_bounds(self, position: Position) -> bool:
        return 0 <= position.x < self._size and 0 <= position.y < self._size

    @abstractmethod
    def _validate_available_size(self) -> bool: ...

    @abstractmethod
    def _validate_figures(self) -> bool: ...

    @staticmethod
    @abstractmethod
    def generate_empty_board(size: int) -> "BaseBoard[TState, TFigure]": ...

    @property
    @abstractmethod
    def state(self) -> TState: ...

    @staticmethod
    @abstractmethod
    def from_state(state: TState) -> "BaseBoard[TState, TFigure]": ...

    @abstractmethod
    def place_figure(self, position: Position, figure: TFigure) -> None: ...


class Board(BaseBoard[list[list[int]], Stone]):
    def __init__(self, size: int, figures: dict[Position, Stone | None]):
        super().__init__(size, figures)

        for group in self._find_groups_without_liberties():
            self.__remove_group(group)

    def _find_groups_without_liberties(self) -> list[Group]:
        return [
            self._group_at_position(position)
            for position in self._get_not_empty_positions()
            if not self._group_at_position(position).liberties
        ]

    def _get_not_empty_positions(self) -> list[Position]:
        return [
            position
            for position, stone in self.figures.items()
            if stone is not None
        ]

    def _validate_figures(self) -> bool:
        return all(
            isinstance(stone, (Stone, type(None)))
            for stone in self.figures.values()
        )

    def _validate_available_size(self) -> bool:
        valid_sizes = {5, 6, 7, 8, 9, 11, 13, 15, 17, 19}
        return self.size in valid_sizes

    def _get_neighbors(self, position: Position) -> list[Position]:
        return [
            position + delta
            for delta in [
                Position(0, 1),
                Position(0, -1),
                Position(1, 0),
                Position(-1, 0),
            ]
            if self.position_in_bounds(position + delta)
        ]

    def __remove_group(self, group: Group):
        for position in group.stones:
            self.figures[position] = None

    def _group_at_position(self, position: Position) -> Group:
        color = self.figures.get(position, None)
        if color is None:
            raise ValueError("Position is empty.")

        def bfs(queue: list[Position], visited: set[Position], group: Group):
            while queue:
                pos = queue.pop(0)
                if pos in visited:
                    continue
                visited.add(pos)

                if self.figures.get(pos) == color:
                    group.stones.add(pos)
                    queue.extend(
                        neighbor
                        for neighbor in self._get_neighbors(pos)
                        if neighbor not in visited
                    )
                elif self.figures.get(pos) is None:
                    group.liberties.add(pos)
            return group

        group = Group(stones=set(), liberties=set())
        return bfs([position], set(), group)

    @staticmethod
    def generate_empty_board(size: int) -> "Board":
        figures: dict[Position, Stone | None] = {
            Position(x, y): None for x, y in product(range(size), range(size))
        }
        return Board(size, figures)

    @property
    def state(self) -> list[list[int]]:
        state = [[-1] * self.size for _ in range(self.size)]
        for position, stone in self.figures.items():
            state[position.x][position.y] = (
                1
                if stone == Stone.BLACK
                else 0 if stone == Stone.WHITE else -1
            )
        return state

    @staticmethod
    def from_state(state: list[list[int]]) -> "BaseBoard":
        stones = {
            Position(x, y): (
                Stone.BLACK
                if cell == 1
                else Stone.WHITE if cell == 0 else None
            )
            for x, row in enumerate(state)
            for y, cell in enumerate(row)
        }
        return Board(len(state), stones)

    def place_figure(self, position: Position, figure: Stone) -> None:
        if not self.position_in_bounds(position):
            raise ValueError("Position out of bounds.")
        if self.figures.get(position) is not None:
            raise ValueError("Intersection occupied by existing stone.")

        self.figures[position] = figure

        try:
            neighboring_enemy_groups = [
                self._group_at_position(neighbor)
                for neighbor in self._get_neighbors(position)
                if self.figures.get(neighbor) not in {None, figure}
            ]

            for group in neighboring_enemy_groups:
                if not group.liberties:
                    self.__remove_group(group)

            new_group = self._group_at_position(position)
        except ValueError as e:
            self.figures[position] = None
            raise e

        if not new_group.liberties:
            self.figures[position] = None
            raise ValueError("New group has zero liberties (suicide)")
