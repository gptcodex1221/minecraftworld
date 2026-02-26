#!/usr/bin/env python3
"""CLI-программа для генерации плана постройки реальных мест в Minecraft."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class PlaceTemplate:
    name: str
    size_meters: Tuple[int, int, int]
    material: str
    details: List[str]


PLACES: Dict[str, PlaceTemplate] = {
    "1": PlaceTemplate(
        name="Эйфелева башня (Париж)",
        size_meters=(125, 330, 125),
        material="smooth_stone",
        details=[
            "4 опоры по углам основания",
            "Площадка на высоте ~57 м",
            "Площадка на высоте ~115 м",
            "Антенна на вершине",
        ],
    ),
    "2": PlaceTemplate(
        name="Статуя Свободы (Нью-Йорк)",
        size_meters=(47, 93, 47),
        material="oxidized_copper",
        details=[
            "Прямоугольный пьедестал",
            "Факел справа",
            "Корона с 7 лучами",
        ],
    ),
    "3": PlaceTemplate(
        name="Биг-Бен и Вестминстер (Лондон)",
        size_meters=(85, 96, 48),
        material="sandstone",
        details=[
            "Высокая башня с часами",
            "Основной корпус вдоль реки",
            "Четыре циферблата",
        ],
    ),
    "4": PlaceTemplate(
        name="Колизей (Рим)",
        size_meters=(188, 48, 156),
        material="light_gray_concrete",
        details=[
            "Овальный периметр",
            "Много арок по кругу",
            "Центральная арена",
        ],
    ),
}


def scaled(value: int, scale: float) -> int:
    return max(1, int(round(value * scale)))


def build_plan(place: PlaceTemplate, scale: float) -> Dict[str, object]:
    x, y, z = place.size_meters
    sx, sy, sz = scaled(x, scale), scaled(y, scale), scaled(z, scale)
    volume = sx * sy * sz

    commands = [
        f"/fill ~0 ~0 ~0 ~{sx} ~0 ~{sz} minecraft:{place.material}",
        f"/fill ~0 ~1 ~0 ~{sx} ~{sy} ~{sz} minecraft:air hollow",
    ]

    return {
        "name": place.name,
        "dimensions": (sx, sy, sz),
        "volume": volume,
        "commands": commands,
        "details": place.details,
    }


def choose_place() -> PlaceTemplate:
    print("Выбери место для постройки в Minecraft:\n")
    for key, place in PLACES.items():
        x, y, z = place.size_meters
        print(f"{key}. {place.name} — {x}м x {y}м x {z}м")

    while True:
        choice = input("\nВведи номер места: ").strip()
        if choice in PLACES:
            return PLACES[choice]
        print("Неверный выбор. Попробуй снова.")


def choose_scale() -> float:
    print("\nМасштаб (сколько блоков на 1 метр):")
    print("1. 1:1 (1 блок = 1 метр)")
    print("2. 1:2 (1 блок = 2 метра)")
    print("3. 2:1 (2 блока = 1 метр)")

    mapping = {"1": 1.0, "2": 0.5, "3": 2.0}
    while True:
        choice = input("Выбери масштаб: ").strip()
        if choice in mapping:
            return mapping[choice]
        print("Неверный выбор масштаба.")


def main() -> None:
    print("=== Генератор реальных мест для Minecraft ===")
    place = choose_place()
    scale = choose_scale()
    plan = build_plan(place, scale)

    x, y, z = plan["dimensions"]
    print("\n--- План постройки ---")
    print(f"Место: {plan['name']}")
    print(f"Размер в блоках: {x} x {y} x {z}")
    print(f"Примерный объём: {plan['volume']} блоков")

    print("\nКлючевые элементы:")
    for detail in plan["details"]:
        print(f"- {detail}")

    print("\nСтартовые команды:")
    for command in plan["commands"]:
        print(command)

    print("\nСовет: строй на плоской карте (superflat), чтобы проще выдерживать масштаб.")


if __name__ == "__main__":
    main()
