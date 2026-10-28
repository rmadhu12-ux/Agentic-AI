

raw = {"id": "101", "title": "Login fails", "priority": "high", "hours": "5.5"}

from pathlib import Path
from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic import ValidationError
from typing import Literal
import csv
import json
import logging



base = Path("data")

#not Pydantic
#
@dataclass
class Ticket:
    id: int
    title: str
    priority: str
    hours: float

"""def total_hours(hours: list[float]) -> float:
    return sum(hours)

t = total_hours("abc")"""

t= Ticket(101, "Login fails", "high", 5.5)
t1= Ticket("101", "Login fails", "high", 5.5)
print(t)
#complain? (NO error, because dataclasses don't validate or convert.)
print(t1.id)


#"101" became an int and "5.5" a float automatically. 
# That is the conversion step you wrote in process in day 4.
class TicketModel(BaseModel):
    id: int
    title: str
    priority: str
    hours: float

t = TicketModel(**raw)
print(t)
print(type(t.id), type(t.hours)) #type conversion happens automatically.

try:
    TicketModel(id = "abc", title = "x", priority = "high", hours = -1)
except ValidationError as e:
    print(e)

class TicketModel2(BaseModel):
    id: int
    title: str
    priority: Literal["high", "medium", "low"]
    hours: float = Field(ge = 0)

try:
    t = TicketModel2(id="1", title="x", priority="urgent", hours=-3)
    print(t.model_dump())
    print(t.model_dump_json())
except ValidationError as e:
    print(e.error_count())
    print(e)

logging.basicConfig(
    filename="data/day5.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

def process_v2(csv_path, out_path):
    valid, invalid = [], 0

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                ticket = TicketModel2(**row)            # TicketModel2 converts and validates
                valid.append(ticket.model_dump())              # a plain dict, via model_dump()
            except ValidationError as e:                   # Pydantic's ValidationError
                logger.warning("skipping row %s: %s", row.get("id"), e)
                invalid += 1

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(valid, f, indent=2)

    logger.info("processed %d, valid %d, invalid %d",
                len(valid) + invalid, len(valid), invalid)
    
process_v2(base / "tickets.csv", base / "clean_tickets.json")









