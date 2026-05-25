import re

class Result:
    def __init__(self, line, event):
        parts = re.split(r'\s{2,}', line.strip())
        if len(parts) >= 3:
            self.event = event
            self.place, self.athlete = self._parse_place_and_athlete(parts[0])
            self.team = parts[1]
            self.mark = parts[2]
        else:
            raise ValueError(f"Line does not contain enough parts to parse: {line}")

    def needs_award(self):
        return self.place.isdigit() and int(self.place) <= 6

    def _parse_place_and_athlete(self, place_athlete_str):
        match = re.match(r'\s*(\d+|--)\s(\S+, \S+)', place_athlete_str)
        if match:
            place = match.group(1)
            athlete = match.group(2) if match.group(2) else ""
            return place, athlete
        else:
            raise ValueError(f"Could not parse place and athlete from string: {place_athlete_str}")      

    def __str__(self):
        return f"{self.event} - {self.place} - {self.athlete} - {self.team} - {self.mark}"
    
