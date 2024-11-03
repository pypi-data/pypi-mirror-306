from pydantic import BaseModel

from mailoxy.dmr import DifficultyEnum


class DivingFish(BaseModel):
    achievements: float
    ds: float
    dxScore: int
    fc: str
    fs: str
    level: str
    level_index: DifficultyEnum
    level_label: str
    ra: int
    rate: str
    song_id: int
    title: str
    type: str
