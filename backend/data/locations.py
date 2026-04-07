LOCATIONS = [
    "New York, NY",        # Start 🏁 (finance + media hub)
    "Philadelphia, PA",
    "Washington, DC",
    "Raleigh, NC",        # Research Triangle
    "Atlanta, GA",
    "Austin, TX",         # Startup boom city
    "Denver, CO",
    "Boulder, CO",        # Tech/startup scene
    "Salt Lake City, UT", # Silicon Slopes
    "Palo Alto, CA",      # VC + startups
    "San Francisco, CA"   # End 🚀
]


LOCATION_EFFECTS = {
    "Austin, TX": {"followers": +20},
    "Palo Alto, CA": {"money": +1000},
    "Denver, CO": {"morale": +10},
}
ROUTES = [
    {"from": "New York, NY", "to": "Philadelphia, PA", "miles": 95},
    {"from": "Philadelphia, PA", "to": "Washington, DC", "miles": 140},
    {"from": "Washington, DC", "to": "Raleigh, NC", "miles": 270},
    {"from": "Raleigh, NC", "to": "Atlanta, GA", "miles": 400},
    {"from": "Atlanta, GA", "to": "Austin, TX", "miles": 500},
    {"from": "Austin, TX", "to": "Denver, CO", "miles": 500},
    {"from": "Denver, CO", "to": "Boulder, CO", "miles": 30},
    {"from": "Boulder, CO", "to": "Salt Lake City, UT", "miles": 470},
    {"from": "Salt Lake City, UT", "to": "Palo Alto, CA", "miles": 740},
    {"from": "Palo Alto, CA", "to": "San Francisco, CA", "miles": 35},
]