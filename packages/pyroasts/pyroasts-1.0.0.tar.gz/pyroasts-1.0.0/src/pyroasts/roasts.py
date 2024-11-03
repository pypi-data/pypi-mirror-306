"""Random used to select random roasts. Importing roasts from helper file."""
import random
from .helper import generic_roasts, names, roast_templates

def personal_roast(name: str, severity: int) -> str:
    """Returns a personalized roast given a name and severity level."""
    name = name.lower().capitalize()
    roasts = {
        1: f"{name}, you're like a Monday morning — nobody likes you, we put up with you.",
        2: f"{name}, if you were any more average, you'd be a mean.",
        3: f"{name}, I'd explain how awful you are, but it's more fun to watch you figure it out.",
        4: f"{name}, you're the reason we can't have nice things.",
        5: f"{name}, even your reflection is disappointed when it sees you.",
        6: f"Wow, {name}, you must be so confident to leave your house looking like that.",
        7: f"{name}, do you have a therapist? Like, I’m worried about you.",
        8: f"{name}, you have to log off.",
        9: f"{name}, touch grass"
    }
    # return a default roast if severity value not found in dictionary.
    return roasts.get(severity, f"{name}, you're so bland that even a salt shaker thinks you're boring.")
    
def skill_roast(skill: str, sarcasm_level: int) -> str:
    """Returns a roast for an inputted skill and degree of sarcasm"""
    if sarcasm_level == 2:
        skill = skill.lower().capitalize()
    else:
        skill = skill.lower()
    roasts = {
        1: f"Your {skill} skills are like a WiFi signal in the middle of nowhere — nonexistent.",
        2: f"{skill}... You're joking right?",
        3: f"I've seen toddlers with better {skill} skills than you... and they can't even talk.",
        4: f"{skill}? Maybe you should learn how to read first.",
        5: f"{skill}? I’m too busy to pretend that I care.",
        6: f"{skill}? That makes me almost care about you."
    }
    # return a default roast if sarcasm_level not found in dictionary.
    return roasts.get(sarcasm_level, f"Your {skill} skills are a whole new level of disappointment.")

def comparison_roast(thing1: str, thing2: str) -> str:
    """Returns a roast for choosing one thing over another."""
    # Handle empty strings
    if not thing1 and not thing2:
        return "Are you really comparing nothing to nothing? That's a new low."

    thing1 = thing1.lower().capitalize() if thing1 else "Nothing"
    thing2 = thing2.lower() if thing2 else "Nothing"
    
    roasts = [
        f"{thing1} instead of {thing2}? I'd rather sit on a cactus.",
        f"{thing1} over {thing2}? I'd rather star in a documentary called 'How Far Can the Human Body be Stretched'.",
        f"{thing1} over {thing2}? I'd rather step on a LEGO.",
        f"{thing1} instead of {thing2}? Did anybody ask?",
        f"{thing1} over {thing2}? Are your parents siblings?"
    ]
    # return a randomly selected roast from the list.
    return random.choice(roasts)

def advice_roast(topic: str, sarcasm_level: int) -> str:
    """Returns a roast that gives sarcastic advice based on given topic and sarcasm level."""
    topic = topic.lower()
    roasts = {
        1: f"Trying to learn {topic}? Just keep doing the bare minimum, I'm sure it'll work out... somehow.",
        2: f"Your attempt at {topic} is so inspiring, it's a shame nobody's watching.",
        3: f"Maybe if you spent half as much time on {topic} as you do scrolling on social media, you'd actually get somewhere."
    }
    # return a default roast if sarcasm_level not found in dictionary.
    return roasts.get(sarcasm_level, f"You call that effort in {topic}? I've seen potatoes put in more work.")

def get_roast():
    """Get a single random roast from the list of roasts"""
    return random.choice(generic_roasts)

def get_n_names(n=2):
    """Get a list of n random insulting names from the list of insulting names"""
    return [name.lower() for name in random.sample(names, min(n, len(names)))]

def get_roast_template():
    """Get a single random roast template from the list of roast templates"""
    return random.choice(roast_templates)