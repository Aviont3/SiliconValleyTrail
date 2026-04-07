# data/events.py

LOCAL_EVENTS = {
    
}

TRAVEL_EVENTS = {
    "Traffic Jam": {
        "description": "A major traffic jam delays you and costs the team energy.",
        "effects": {"chemistry": -10, "day": 1},
    },
    "Productive Ride": {
        "description": "The team uses the trip to brainstorm a new feature.",
        "effects": {"product_progress": 15, "chemistry": 5},
    },
    "Detour Adventure": {
        "description": "A surprising detour leads to a helpful networking opportunity.",
        "effects": {"followers": 200, "money": -50},
    },
    "Roadside Pitch": {
        "description": "You pitch to a passing investor during the journey.",
        "effects": {"money": 500, "followers": 100},
    },
    "Flat Tire": {
        "description": "A flat tire slows you down and cuts into your budget.",
        "effects": {"money": -100, "day": 1, "chemistry": -5},
    },"Viral Tweet": {
        "description": "Your message goes viral and attracts new followers.",
        "effects": {"followers": 1000},
    },
    "Server Crash": {
        "description": "A server outage costs money to recover.",
        "effects": {"money": -500,"product_progress": -5},
    },
    "Team Burnout": {
        "description": "The team is exhausted after a long sprint.",
        "effects": {"chemistry": -10, "product_progress": -10},
    },
    "Hack-a-thon Win": {
        "description": "Your team wins a hackathon and gets funding.",
        "effects": {"money": 2000, "day": 1},
    },
    "AWS Outage": {
        "description": "An outage forces your team to spend money fixing the platform.",
        "effects": {"money": -1000, "product_progress": -10},
    },
    "Tech Conference": {
        "description": "A conference boosts followers and product momentum.",
        "effects": {"followers": 500, "day": 1},
    },
    "Investor Interest": {
        "description": "An investor shows interest in your startup.",
        "effects": {"money": 500},
    },
    "Tech Debt": {
        "description": "Legacy code causes issues and slows progress.",
        "effects": {"product_progress": -15, "chemistry": -5},
    },
    "Viral LinkedIn Post": {
        "description": "Your LinkedIn post goes viral, attracting followers.",
        "effects": {"followers": 800},
    },
    "Security Breach": {
        "description": "A security breach costs money and damages reputation.",
        "effects": {"money": -1500, "followers": -200, "chemistry": -20, "product_progress": -20},
    },
    "Influencer Endorsement": {
        "description": "An influencer endorses your product, boosting followers.",
        "effects": {"followers": 1200},
    },
}
