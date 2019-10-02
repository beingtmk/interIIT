import re
from django import template
from django.conf import settings


register = template.Library()

@register.filter
def sport_url(value):
    sport = value.lower().replace(" ", "_")
    return sport

def sport_url_player(value):
    sport = value.lower().replace(" ", "_")
    return sport

@register.filter
def sport_template(value): # Only one argument.
    sport = value.lower().replace(" ", "_")

    path = "Schedule/sports" + "/" + str(sport) + "/" + str(sport) + ".html"
    return path

@register.filter
def sport_create(value): # Only one argument.
    sport = value.lower().replace(" ", "")
    url = "create_" + str(sport)
    return url

@register.filter
def sport_score(value): # Only one argument.
    sport = value.lower().replace(" ", "")
    url = str(sport) + "_score"
    return url

@register.filter
def get_total_players(events):
    return sum(map(lambda event: event.player_count(), events))

@register.filter
def team_slug(team_name):
    team_name = team_name.split(' ')[-1].lower()
    if team_name == "madras":
        return "iitm"
    elif team_name == "guwahati":
        return "iitg"
    elif team_name == "delhi":
        return "iitd"
    elif team_name == "bombay":
        return "iitb"
    elif team_name == "kharagpur":
        return "iitkgp"
    elif team_name == "kanpur":
        return "iitk"
    elif team_name == "roorkee":
        return "iitr"

@register.filter
def remove_us(value):
    return " ".join(value.split("_"))

@register.filter
def get_slug(value):
    return value.replace(' ', '_')

@register.filter
def concat_events(events):
    event_list = []
    for event in events:
        event_list.append('{} {}'.format(event.event, event.sport))
    return ', '.join(event_list)

# Getting Background image for Sport Specific Page
@register.filter
def sport_background(value): # Only one argument.
    sport = value.lower().replace(" ", "_")

    # path = "Schedule/img/sports/background/" + str(sport) + ".jpg"
    path = "Schedule/img/sports/background/football.jpg"
    return path

# Getting Background image for Sport Specific Page
@register.filter
def sport_scoretable(value): # Only one argument.
    # sport = value.lower().replace(" ", "")

    # path = "Schedule/generic/sports/helper/score/_" + str(sport) + "_score.html"
    # path = "Schedule/img/sports/logo/athletics.png"
    path1 = "Schedule/generic/sports/helper/score/scoretype1.html"
    path2 = "Schedule/generic/sports/helper/score/scoretype2.html"
    sport = value.lower()

    if sport in ['athletics', 'swimming', 'weight lifting']:
        return path1
    else:
        return path2

    return path

# Getting Background image for Sport Specific Page
@register.filter
def sport_logo(value): # Only one argument.
    sport = value.lower().replace(" ", "_")
    path = "Schedule/img/pictograms/" +  sport + ".png"
    return path

# Getting Background image for Sport Specific Page
@register.filter
def sport_match(value): # Only one argument.
    # path = "Schedule/img/sports/logo/" + str(sport) + ".jpg"
    path1 = "Schedule/generic/sports/helper/match/type1.html"
    path2 = "Schedule/generic/sports/helper/match/type2.html"
    sport = value.lower()

    if sport in ['athletics', 'swimming', 'weight lifting']:
        return path1
    else:
        return path2

# get element at index i
@register.filter
def index_title(List, i):
    x = List[int(i)].title
    print(x)
    return x

# match update
@register.filter
def match_update(value):
    sport = value.lower().replace(" ", "")
    path =  sport + "_update"
    return path

# match delete
@register.filter
def match_delete(value):
    sport = value.lower().replace(" ", "")
    path =  sport + "_delete"
    return path

# player_sport
@register.filter
def player_sport(value):
    sport = value.lower().replace(" ", "")
    path =  "player" + sport + "_update"
    return path

# player_sport
@register.filter
def player_sport_delete(value):
    sport = value.lower().replace(" ", "")
    path =  "player" + sport + "_delete"
    return path


@register.filter
def index_brief(List, i):
    return List[int(i)].brief

numeric_test = re.compile("^\d+$")
@register.filter
def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""

    sport = arg.replace(" ", "")
    arg = 'player' + sport + '_set'

    if hasattr(value, str(arg)):
        print('1')
        return getattr(value, arg)
    else:
        print('2')

# Getting Background image for Sport Specific Page
@register.filter
def sport_mod(value): # Only one argument.
    sport = value.upper().replace("_", " ")
    return sport
