
from collections import defaultdict
tickets = [
    {"id": 101, "title": "Login fails", "priority": "high", "hours": 5.5, "assignee": "Asha"},
    {"id": 102, "title": "Report slow", "priority": "medium", "hours": 3.0, "assignee": "Ravi"},
    {"id": 103, "title": "Typo on page", "priority": "low", "hours": 0.5, "assignee": "Asha"},
    {"id": 104, "title": "Payment error", "priority": "high", "hours": 8.0, "assignee": "Meena"},
    {"id": 105, "title": "Export broken", "priority": "medium", "hours": 4.0, "assignee": "Ravi"},
]

letters = list("abcdefghij")

""" 1. List comprehension (basic)
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
final =[]
for i in nums:
    if i % 2 == 0:
        final.append(i*i)
print(final)"""      

""" 2. List comprehension on dictionaries
final =[]
for ticket in tickets:
    if ticket["priority"]== "high":
        final.append(ticket["title"])
print(final) """

"""3. Dict comprehension
final = {}
for ticket in tickets:
    final[ticket["id"]] = ticket["hours"]
print(final) """

"""#the first 3 items
print(letters[0:3])

#the last 3 items
print(letters[-3:])"""

#every second item
#loop
"""newletters = []
for i in range(len(letters)-1):
    if i %2 == 0:
        newletters.append(letters[i])
print(newletters)

#slicing
print(letters[::2])"""

#the list reversed
"""print(letters[::-1])"""

#items from index 2 up to (not including) index 7
"""print(letters[2:7])"""

"""#Sorting with key
sortedTickets = sorted(tickets, key = lambda t: t["hours"],  reverse= True)
for t in sortedTickets:
    print(f"{t["id"]}: {t["hours"]}")

#Sorting with key
sortedTickets = sorted(tickets, key = lambda t: (t["assignee"], t["hours"]))
print(sortedTickets)

#Sets
team_a = {"Asha", "Ravi", "Meena", "John"}
team_b = {"Ravi", "Priya", "John", "Sam"}

team_c = team_a | team_b
team_c = team_a & team_b #intersection
team_c = team_a ^ team_b #in exactly one
print(team_c)"""

""" 7. Removing duplicates, keeping order
Given emails = ["a@x.com", "b@x.com", "a@x.com", "c@x.com", "b@x.com"], 
remove duplicates but keep the original order. Don't use set() alone, 
since it loses order. Hint: a loop with a "seen" set, or dict.fromkeys.
Expected: ['a@x.com', 'b@x.com', 'c@x.com']

emails = ["a@x.com", "b@x.com", "a@x.com", "c@x.com", "b@x.com"]
final = []
for e in emails:
    if e not in final:
        final.append(e)
print (final) """

"""Count how many tickets each assignee has, 
using a plain dictionary and .get() (no libraries). 
Then redo it with collections.Counter and compare.
Expected: {'Asha': 2, 'Ravi': 2, 'Meena': 1}

counts = {}
for ticket in tickets:
    name = ticket["assignee"]
    counts[name] = counts.get(name, 0) + 1
print(counts)"""

"""9. Grouping with setdefault or defaultdict
Group ticket titles by priority.
Expected: {'high': ['Login fails', 'Payment error'], 'medium': [...], 'low': [...]}"""

#Shortcut
"""grouped = defaultdict(list)
for ticket in tickets:
    grouped[ticket["priority"]].append(ticket["title"])
print(grouped)"""

#long method
"""grouped = {}
for ticket in tickets:
    p = ticket["priority"]    
    if p not in grouped:
        grouped[p] = []
        grouped[p].append(ticket["title"])
    else:
        grouped[p].append(ticket["title"])
print(grouped)     """

"""10. f-strings and formatting
Print a neat table from tickets, with aligned columns:

ID   Title            Priority   Hours
101  Login fails      high        5.5"""

"""Use f-string width and alignment such as {title:<15} and {hours:>6.1f}.
Finish with a line showing total hours, 
formatted with a thousands separator and 2 decimals, for example Total: 21.00 hours."""

for t in tickets:
    print(f"{t['id']:<5}{t['priority']:<16}{t['hours']:<10}")