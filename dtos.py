from dataclasses import dataclass

@dataclass
class Item:
    topName: str
    name: str
    pricePerUnit: float
    link: str
    timeframe: str
    measurement: str

    def __str__(self):
        return f"{self.name} - {self.pricePerUnit} kr. {self.measurement} -  {self.timeframe} - {self.link}"

@dataclass
class User:
    name: str
    email: str
    password: str
    username: str
    location: str # coordinates

    def __str__(self):
        return f"{self.name} - {self.email} - {self.username}"