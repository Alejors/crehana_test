from sqlalchemy import and_
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql.sqltypes import String, Integer, DateTime, Float
from datetime import datetime


def _convert_value(value: str, column_type):
    if isinstance(column_type, String):
        return value
    elif isinstance(column_type, Integer):
        return int(value)
    elif isinstance(column_type, Float):
        return float(value)
    elif column_type.__class__.__name__.lower() in {"boolean", "bool", "tinyint"}:
        return value.lower() in {"true", "1", "yes"}
    elif isinstance(column_type, DateTime):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Invalid datetime format")
    return value


def parse_filters(filters: dict[str, str], model: DeclarativeMeta):
    conditions = []

    for raw_key, raw_value in filters.items():
        if "__" in raw_key:
            field, op = raw_key.split("__", 1)
        else:
            field, op = raw_key, "eq"

        column = getattr(model, field, None)
        if column is None:
            continue

        column_type = column.type
        try:
            if op == "in":
                raw_items = raw_value.split(",")
                value = [
                    _convert_value(item.strip(), column_type) for item in raw_items
                ]
            else:
                value = _convert_value(raw_value, column_type)
        except Exception:
            continue

        if op == "eq":
            conditions.append(column == value)
        elif op == "like":
            conditions.append(column.like(f"%{value}%"))
        elif op == "in":
            conditions.append(column.in_(value))
        elif op == "gte":
            conditions.append(column >= value)
        elif op == "lte":
            conditions.append(column <= value)
        elif op == "gt":
            conditions.append(column > value)
        elif op == "lt":
            conditions.append(column < value)

    return and_(*conditions) if conditions else True
