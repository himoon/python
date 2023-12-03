from __future__ import annotations

from enum import Enum


class Boundary(str, Enum):
    HADM_AREA = f"/boundary/hadmarea.geojson"
    STATS_AREA = f"/boundary/statsarea.geojson"
    USER_AREA = f"/boundary/userarea.geojson"

    def __str__(self) -> str:
        return self.value
