from copy import deepcopy
from typing import Any


_EVENTS = [
    {
        "id": 1,
        "name": "My Event",
        "title": "Django Workshop",
        "description": "Практический воркшоп по Django",
        "category": "Education",
        "location": "Baku",
        "status": "Active",
    },
    {
        "id": 2,
        "name": "Tech Event",
        "title": "Python Conference",
        "description": "Конференция для Python-разработчиков",
        "category": "Technology",
        "location": "Baku",
        "status": "Active",
    },
    {
        "id": 3,
        "name": "Sport Event",
        "title": "Baku Football Cup",
        "description": "Любительский футбольный турнир",
        "category": "Sport",
        "location": "Baku",
        "status": "Active",
    },
    {
        "id": 4,
        "name": "Coding Event",
        "title": "Web Development Meetup",
        "description": "Встреча веб-разработчиков",
        "category": "Technology",
        "location": "Ganja",
        "status": "Active",
    },
    {
        "id": 5,
        "name": "Education Event",
        "title": "English Speaking Club",
        "description": "Практика разговорного английского языка",
        "category": "Education",
        "location": "Baku",
        "status": "Active",
    },
    {
        "id": 6,
        "name": "Sport Event",
        "title": "Marathon Baku",
        "description": "Городской марафон для участников всех уровней",
        "category": "Sport",
        "location": "Baku",
        "status": "Closed",
    },
    {
        "id": 7,
        "name": "Tech Event",
        "title": "AI & Machine Learning",
        "description": "Введение в искусственный интеллект и машинное обучение",
        "category": "Technology",
        "location": "Sumqayit",
        "status": "Active",
    },
    {
        "id": 8,
        "name": "Education Event",
        "title": "Django Advanced Workshop",
        "description": "Продвинутый курс по разработке на Django",
        "category": "Education",
        "location": "Baku",
        "status": "Closed",
    },
    {
        "id": 9,
        "name": "Sport Event",
        "title": "Basketball Tournament",
        "description": "Любительский турнир по баскетболу",
        "category": "Sport",
        "location": "Ganja",
        "status": "Active",
    },
    {
        "id": 10,
        "name": "Tech Event",
        "title": "Frontend Development Meetup",
        "description": "Практическая встреча по React и современному frontend",
        "category": "Technology",
        "location": "Baku",
        "status": "Closed",
    },
]

_next_id = 2


def list_events() -> list[dict[str, Any]]:
    return deepcopy(_EVENTS)

def active_events() -> list[dict[str, Any]]:
    return [
        event
        for event in _EVENTS
        if event["status"] == "Active"
    ]
def close_events() -> list[dict[str, Any]]:
    return [
        event
        for event in _EVENTS
        if event["status"] == "Closed"
    ]

def get_event(event_id: int) -> dict[str, Any] | None:
    for event in _EVENTS:
        if event["id"] == event_id:
            return deepcopy(event)
    return None


def create_event(
        *,
        name: str,
        title: str,
        description: str,
        category: str,
        location: str,
) -> dict[str, Any]:
    global _next_id
    event = {
        "id": _next_id,
        "name": name.strip(),
        "title": title.strip(),
        "description": description.strip(),
        "category": category.strip(),
        "location": location.strip(),
        "status": "Active",
    }
    _EVENTS.append(event)
    _next_id += 1
    return deepcopy(event)

def update_event(
        event_id: int,
        *,
        name: str,
        title: str,
        description: str,
        category: str,
        location: str,
        status: str,
) -> dict[str, Any] | None:
    for event in _EVENTS:
        if event["id"] == event_id:
            event["name"] = name.strip()
            event["title"] = title.strip()
            event["description"] = description.strip()
            event["category"] = category.strip()
            event["location"] = location.strip()
            event["status"] = status.strip()

            return deepcopy(event)

    return None


def close_event(event_id: int) -> dict[str, Any] | None:
    for event in _EVENTS:
        if event["id"] == event_id:

            if event["status"] == "Active":
                event["status"] = "Closed"

            return deepcopy(event)
    return None


def delete_event(event_id: int) -> bool:
    global _EVENTS

    before = len(_EVENTS)
    _EVENTS = [
        event
        for event in _EVENTS
        if event["id"] != event_id
    ]
    return before != len(_EVENTS)