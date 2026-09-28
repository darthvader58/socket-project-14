import csv

FIELDS = [
    "event_id", "state", "year", "month_name", "event_type", "cz_type",
    "cz_name", "injuries_direct", "injuries_indirect", "deaths_direct",
    "deaths_indirect", "damage_property", "damage_crops", "tor_f_scale",
]

def load_storm_data(path):
    with open(path, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        next(reader)
        records = []
        for row in reader:
            if not row:
                continue
            if len(row) != 14:
                raise ValueError(f"Expected 14 fields, got {len(row)}")
            records.append(dict(zip(FIELDS, row)))
    return records

def is_prime(number):
    if number < 2:
        return False
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True

def next_prime(number):
    candidate = number + 1
    while not is_prime(candidate):
        candidate += 1
    return candidate

def calculate_hash(event_id, table_size, ring_size):
    position = int(event_id) % table_size
    return position, position % ring_size

class LocalTable:
    def __init__(self):
        self.data = {}

    def store(self, position, record):
        event_id = int(record["event_id"])
        self.data.setdefault(position, {})[event_id] = record

    def count(self):
        return sum(len(records) for records in self.data.values())
