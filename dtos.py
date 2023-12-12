from dataclasses import dataclass

@dataclass
class Item:
    topName: str
    name: str
    price_per_unit: float
    link: str
    timeframe: str