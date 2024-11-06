from __future__ import annotations
import json
from typing import Callable, Iterable, Iterator, Optional, TypedDict
from typing_extensions import Self

from kojo.item import Item


def apply(iterable: Iterable[Item], *processes: Process) -> Iterator[Item]:
    for item in iterable:
        processed_item = apply_on_item(item, *processes)
        if processed_item is not None:
            yield processed_item


def apply_on_item(item: Optional[Item], *processes: Process) -> Optional[Item]:
    for process in processes:
        for step in process.steps:
            if item is None:
                return None
            item = step(item)
    return item


FilterStepFunction = Callable[[Item], bool]

MapStepFunction = Callable[[Item], Item]


class MapStep:
    def __init__(self, fn: MapStepFunction):
        self.fn: MapStepFunction = fn

    def __call__(self, item: Item) -> Item:
        return self.fn(item)


class FilterStep:
    def __init__(self, fn: FilterStepFunction):
        self.fn: FilterStepFunction = fn

    def __call__(self, item: Item) -> Optional[Item]:
        keep = self.fn(item)
        return item if keep else None


class Process:
    def __init__(self) -> None:
        self.steps: list[FilterStep | MapStep] = []

    def map(self, fn: MapStepFunction) -> Self:
        self.steps.append(MapStep(fn))
        return self

    def filter(self, fn: FilterStepFunction) -> Self:
        self.steps.append(FilterStep(fn))
        return self

    def __call__(self, iterable: Iterable[Item]) -> Iterator[Item]:
        return apply(iterable, self)

    def __iadd__(self, fn: MapStepFunction) -> Self:
        return self.map(fn)

    def __imul__(self, fn: FilterStepFunction) -> Self:
        return self.filter(fn)


class StepMeta(TypedDict):
    type: str
    module: str
    name: str
    description: Optional[str]


class StepEncoder(json.JSONEncoder):

    def default(self, step: FilterStep | MapStep) -> StepMeta:
        name: str
        desc: Optional[str]

        if hasattr(step.fn, "__qualname__"):
            name = step.fn.__qualname__
            ix = name.find(".<locals>.")
            if ix > -1:
                name = name[ix + 10 :]
            desc = step.fn.__doc__
        elif hasattr(step.fn, "__call__"):
            name = step.fn.__class__.__name__
            desc = step.fn.__call__.__doc__
            if desc is None:
                desc = step.fn.__class__.__doc__
            if desc is None:
                desc = step.fn.__doc__

        if desc is not None:
            desc = desc.strip()

        return {
            "type": type(step).__name__,
            "module": step.fn.__module__,
            "name": name,
            "description": desc,
        }


class ProcessEncoder(json.JSONEncoder):

    def default(self, process: Process) -> list[StepMeta]:
        child_encoder = StepEncoder()
        return [child_encoder.default(step) for step in process.steps]
