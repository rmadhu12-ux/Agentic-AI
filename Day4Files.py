from pathlib import Path
import json
import logging

"""Create a folder data with Path("data").mkdir(exist_ok=True).
Build the path data/notes.txt using the / operator (Path("data") / "notes.txt"), not string concatenation.
Print its .name, .stem, .suffix, and .exists()."""

base = Path("data")
base.mkdir(parents=True, exist_ok=True)

notes_path = base / "notes.txt"

print(notes_path.name)     # notes.txt
print(notes_path.stem)     # notes
print(notes_path.suffix)   # .txt
print(notes_path.exists())


"""2. Write and read a text file

Write 3 lines to data/notes.txt using with open(path, "w", encoding="utf-8") as f:.
Read it back and print the number of lines and each line without the trailing newline.
Then use path.read_text() and path.write_text() and compare. Which is shorter?"""

Lines = ["Lineeee1\n", "Lineeeeeee2\n", "Lineeeeee3\n"]
with open(notes_path, "w") as file:
    file.writelines(Lines)

with open(notes_path, "r") as file:
    contents = file.read()
print(contents)    


#pathlib version
notes_path.write_text("Line A\nLine B\nLine C\n", encoding="utf-8")
text = notes_path.read_text(encoding="utf-8")
print(text.splitlines())   # ['Line A', 'Line B', 'Line C']



"""3. JSON round trip

Save tickets to data/tickets.json with json.dump(tickets, f, indent=2).
Load it back with json.load(f) and confirm the loaded list equals the original (==).
Change one ticket's hours, save again, and open the file to see the change.
Compare json.dumps() and json.dump(). What is the difference? (Hint: one ends in s for "string".)"""


tickets = [
    {"id": 101, "title": "Login fails", "priority": "high", "hours": 5.5},
    {"id": 102, "title": "Report slow", "priority": "medium", "hours": 3.0},
    {"id": 103, "title": "Typo on page", "priority": "low", "hours": -5},
]

json_path = base / "tickets.json"

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(tickets, f, indent=2)

print(json_path.resolve())       # the exact location of the file
print(json_path.stat().st_size)

with open(json_path, "r", encoding="utf-8") as f:
    loaded = json.load(f)

print(loaded == tickets)   # should be True

"""4. CSV """
import csv

csv_path = base / "tickets.csv"
fields = ["id", "title", "priority", "hours"]

# Write
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(tickets)

# Read
with open(csv_path, "r", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print(rows[0])   # look closely at the types
totalhr = 0
for i in range(len(rows)):
    id = int(rows[i]["id"])
    print (type(id))

    hr = float(rows[i]["hours"])
    print (type(hr))

    totalhr += hr

print(totalhr)    

"""Exercise 5: load_json with try/except"""
path = base / "tickets.json"
def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {path}: {e}")
        return None
    finally:
        print("done")

load_json(path)

"""Exercise 6: custom exceptions"""

logger = logging.getLogger(__name__)

REQUIRED = ["id", "title", "priority", "hours"]
PRIORITIES = {"high", "medium", "low"}

tests = [
    {"id": 1, "title": "ok", "priority": "high", "hour": 2.0},
    {"id": 2, "title": "no hours", "priority": "low"},
    {"id": 3, "title": "bad prio", "priority": "urgent", "hours": 1.0},
    {"id": 4, "title": "negative", "priority": "low", "hours": -3},
]
class ValidationError (Exception):
    pass
class ValueError (Exception):
    pass
class InvalidPriority (ValidationError):
    pass
class InvalidHoursError (ValidationError):
    pass
    

def validate_ticket(t):
    for key in REQUIRED:
        if key not in t:
            raise ValidationError(f"missing key: {key}")
# check priority
    if t["priority"] not in PRIORITIES:
        raise InvalidPriority(f"Invali priority: {key}")
# check hours
    if t["hours"] < 0:
        raise InvalidHoursError(f"hours cannot be negative: {t['hours']}")

for t in tests:
    try:
        validate_ticket(t)
        logger.info(f"ticket {t['id']}: valid")
    except ValidationError as e:
        logger.error(f"ticket {t['id']}: invalid - {e}")


"""Exercise 7: logging"""

logging.basicConfig(
    filename="data/app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__) 

logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")

logger.info("loaded %d tickets", len(tickets))

"""Exercise 8: mini pipeline

This combines everything from Day 4. Write process(csv_path, out_path) that:

reads tickets.csv with csv.DictReader
converts id to int and hours to float
validates each row with validate_ticket
logs a warning for each invalid row and skips it
writes the valid rows to a JSON file
logs a summary like processed 4, valid 3, invalid 1"""

def process(csv_path, out_path):
    valid, invalid = [], 0

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                # convert types
                ticket = {
                    "id": int(row["id"]),
                    "title":row["title"],
                    "priority":row["priority"],
                    "hours":float(row["hours"])
                }
                # validate
                validate_ticket(ticket)
                valid.append(ticket)
            except (ValidationError, ValueError, TypeError) as e:
                logger.warning("skipping row %s: %s", row.get("id"), e)
                invalid += 1

    # write valid to out_path as JSON
    logger.info("processed %d, valid %d, invalid %d",
            len(valid) + invalid, len(valid), invalid)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(valid, f, indent=2)

process(base / "tickets.csv", base / "clean_tickets.json")

