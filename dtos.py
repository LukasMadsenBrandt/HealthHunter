from dataclasses import dataclass

@dataclass
class Item:
    topName: str
    name: str
    price_per_unit: float
    link: str
    timeframe: str
    measurement: str

    def __str__(self):
        return f"{self.name} - {self.price_per_unit} kr. {self.measurement} -  {self.timeframe} - {self.link}"