from dataclasses import dataclass
from faker import Faker
_fake = Faker()

@dataclass
class PersonFactory:
    name: str = _fake.name()
    job: str = _fake.job()
