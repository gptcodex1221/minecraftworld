#!/usr/bin/env python3
"""CLI helper for selecting custom places from Google Maps links.

This script lets users build their own place list from Google Maps URLs and then
select one of those places for downstream Minecraft workflows.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

PLACES_FILE = Path("places.json")


class GoogleMapsParseError(ValueError):
    """Raised when coordinates cannot be extracted from a Google Maps URL."""


def parse_google_maps_url(url: str) -> tuple[float, float]:
    """Extract latitude and longitude from a Google Maps URL.

    Supported patterns:
      * .../@<lat>,<lon>,...
      * ...?q=<lat>,<lon>
      * ...?query=<lat>,<lon>
      * plain "<lat>,<lon>" input
    """

    cleaned = url.strip()
    if not cleaned:
        raise GoogleMapsParseError("Пустая ссылка.")

    plain_coords = re.fullmatch(r"\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*", cleaned)
    if plain_coords:
        return float(plain_coords.group(1)), float(plain_coords.group(2))

    parsed = urlparse(cleaned)
    decoded_path = unquote(parsed.path)

    at_match = re.search(r"@(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)", decoded_path)
    if at_match:
        return float(at_match.group(1)), float(at_match.group(2))

    query = parse_qs(parsed.query)
    for key in ("q", "query"):
        if key in query and query[key]:
            value = query[key][0]
            query_match = re.search(r"(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)", value)
            if query_match:
                return float(query_match.group(1)), float(query_match.group(2))

    raise GoogleMapsParseError("Не удалось извлечь координаты из ссылки Google Maps.")


def minecraft_coords(lat: float, lon: float) -> tuple[int, int]:
    """Convert geo coordinates to coarse Minecraft X/Z coordinates."""

    scale = 1000
    return int(round(lon * scale)), int(round(lat * scale))


def load_places(path: Path = PLACES_FILE) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError("Файл мест повреждён: ожидается список.")
    return data


def save_places(places: list[dict[str, Any]], path: Path = PLACES_FILE) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(places, file, ensure_ascii=False, indent=2)


def add_place(places: list[dict[str, Any]]) -> None:
    name = input("Название места: ").strip()
    if not name:
        print("Название не может быть пустым.")
        return

    link = input("Ссылка Google Maps (или lat,lon): ").strip()
    try:
        lat, lon = parse_google_maps_url(link)
    except GoogleMapsParseError as error:
        print(f"Ошибка: {error}")
        return

    x, z = minecraft_coords(lat, lon)
    place = {"name": name, "lat": lat, "lon": lon, "x": x, "z": z, "source": link}
    places.append(place)
    print(f"Добавлено: {name} -> lat={lat:.6f}, lon={lon:.6f}, Minecraft: x={x}, z={z}")


def choose_place(places: list[dict[str, Any]]) -> None:
    if not places:
        print("Пока нет мест. Сначала добавьте хотя бы одно.")
        return

    print("\nДоступные места:")
    for index, place in enumerate(places, start=1):
        print(f"{index}. {place['name']} (lat={place['lat']:.6f}, lon={place['lon']:.6f})")

    selected_raw = input("Выберите номер места: ").strip()
    if not selected_raw.isdigit():
        print("Введите номер из списка.")
        return

    selected = int(selected_raw)
    if not 1 <= selected <= len(places):
        print("Такого номера нет.")
        return

    place = places[selected - 1]
    print("\nВы выбрали:")
    print(f"Название: {place['name']}")
    print(f"Координаты Google Maps: {place['lat']:.6f}, {place['lon']:.6f}")
    print(f"Координаты Minecraft: x={place['x']}, z={place['z']}")


def main() -> None:
    places = load_places()

    while True:
        print("\n=== Minecraft Places Builder ===")
        print("1. Добавить своё место из Google Maps")
        print("2. Выбрать место")
        print("3. Сохранить и выйти")

        action = input("Выберите действие: ").strip()

        if action == "1":
            add_place(places)
        elif action == "2":
            choose_place(places)
        elif action == "3":
            save_places(places)
            print(f"Сохранено мест: {len(places)} в {PLACES_FILE}")
            break
        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()
