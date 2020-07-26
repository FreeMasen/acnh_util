import csv, sqlite3
FISH = [
    {'name': "Bitterling",          'price':  900,'location': "River",                'size': "1",        'hours': "All day",                  'months':["x","x","x","-","-","-","-","-","-","-","x","x"]},
    {'name': "Pale chub",           'price':  200,'location': "River",                'size': "1",        'hours': "9 AM - 4 PM",              'months':["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Crucian carp",        'price':  160,'location': "River",                'size': "2",        'hours': "All day",                  'months':["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Dace",                'price':  240,'location': "River",                'size': "3",        'hours': "4 PM - 9 AM",              'months':["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Carp",                'price':  300,'location': "Pond",                 'size': "4",        'hours': "All day",                  'months':["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Koi",                 'price': 4000,'location': "Pond",                 'size': "4",        'hours': "4 PM - 9 AM",              'months':["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Goldfish",            'price': 1300,'location': "Pond",                 'size': "1",        'hours': "All day",                  'months':["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Pop-eyed goldfish",   'price': 1300,'location': "Pond",                 'size': "1",        'hours': "9 AM - 4 PM",              'months':["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Ranchu goldfish",     'price': 4500,'location': "Pond",                 'size': "2",        'hours': "9 AM - 4 PM",              'months':["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Killifish",           'price':  300,'location': "Pond",                 'size': "1",        'hours': "All day",                  'months':["-","-","-","x","x","x","x","x","-","-","-","-"]},
    {'name': "Crawfish",            'price':  200,'location': "Pond",                 'size': "2",        'hours': "All day",                  'months':["-","-","-","x","x","x","x","x","x","-","-","-"]},
    {'name': "Soft-shelled turtle", 'price': 3750,'location': "River",                'size': "4",        'hours': "4 PM - 9 AM",              'months':["-","-","-","-","-","-","-","x","x","-","-","-"]},
    {'name': "Snapping Turtle",     'price': 5000,'location': "River",                'size': "4",        'hours': "9 PM - 4 AM",              'months':["-","-","-","x","x","x","x","x","x","x","-","-"]},
    {'name': "Tadpole",             'price':  100,'location': "Pond",                 'size': "1",        'hours': "All day",                  'months':["-","-","x","x","x","x","x","-","-","-","-","-"]},
    {'name': "Frog",                'price':  120,'location': "Pond",                 'size': "2",        'hours': "All day",                  'months':["-","-","-","-","x","x","x","x","-","-","-","-"]},
    {'name': "Freshwater goby",     'price':  400,'location': "River",                'size': "2",        'hours': "4 PM - 9 AM",              'months':["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Loach",               'price':  400,'location': "River",                'size': "2",        'hours': "All day",                  'months':["-","-","x","x","x","-","-","-","-","-","-","-"]},
    {'name': "Catfish",             'price':  800,'location': "Pond",                 'size': "4",        'hours': "4 PM - 9 AM",              'months':["-","-","-","-","x","x","x","x","x","x","-","-"]},
    {'name': "Giant snakehead",     'price': 5500,'location': "Pond",                 'size': "4",        'hours': "9 AM - 4 PM",              'months':["-","-","-","-","-","x","x","x","-","-","-","-"]},
    {'name': "Bluegill",            'price':  180,'location': "River",                'size': "2",        'hours': "9 AM - 4 PM",              'months':["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Yellow perch",        'price':  300,'location': "River",                'size': "3",        'hours': "All day",                  'months':["x","x","x","-","-","-","-","-","-","x","x","x"]},
    {'name': "Black bass",          'price':  400,'location': "River",                'size': "4",        'hours': "All day",                  'months':["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Tilapia",             'price':  800,'location': "River",                'size': "3",        'hours': "All day",                  'months':["-","-","-","-","-","x","x","x","x","x","-","-"]},
    {'name': "Pike",                'price': 1800,'location': "River",                'size': "5",        'hours': "All day",                  'months':["-","-","-","-","-","-","-","-","x","x","x","x"]},
    {'name': "Pond smelt",          'price':  500,'location': "River",                'size': "2",        'hours': "All day",                  'months':["x","x","-","-","-","-","-","-","-","-","-","x"]},
    {'name': "Sweetfish",           'price':  900,'location': "River",                'size': "3",        'hours': "All day",                  'months':["-","-","-","-","-","-","x","x","x","-","-","-"]},
    {'name': "Cherry salmon",       'price': 1000,'location': "River (Clifftop)",     'size': "3",        'hours': "4 PM - 9 AM",              'months':["-","-","x","x","x","x","-","-","x","x","x","-"]},
    {'name': "Char",                'price': 3800,'location': "River (Clifftop) Pond",'size': "3",        'hours': "4 PM - 9 AM",              'months':["-","-","x","x","x","x","-","-","x","x","x","-"]},
    {'name': "Golden trout",        'price':15000,'location': "River (Clifftop)",     'size': "3",        'hours': "4 PM - 9 AM",              'months':["-","-","x","x","x","-","-","-","x","x","x","-"]},
    {'name': "Stringfish",          'price':15000,'location': "River (Clifftop)",     'size': "5",        'hours': "4 PM - 9 AM",              'months':["x","x","x","-","-","-","-","-","-","-","-","x"]},
    {'name': "Salmon",              'price':  700,'location': "River (Mouth)",        'size': "4",        'hours': "All day",                  'months':["-","-","-","-","-","-","-","-","x","-","-","-"]},
    {'name': "King salmon",         'price': 1800,'location': "River (Mouth)",        'size': "6",        'hours': "All day",                  'months':["-","-","-","-","-","-","-","-","x","-","-","-"]},
    {'name': "Mitten crab",         'price': 2000,'location': "River",                'size': "2",        'hours': "4 PM - 9 AM",              'months':["-","-","-","-","-","-","-","-","x","x","x","-"]},
    {'name': "Guppy",               'price': 1300,'location': "River",                'size': "1",        'hours': "9 AM - 4 PM",              'months':["-","-","-","x","x","x","x","x","x","x","x","-"]},
    {'name': "Nibble fish",         'price': 1500,'location': "River",                'size': "1",        'hours': "9 AM - 4 PM",              'months':["-","-","-","-","x","x","x","x","x","-","-","-"]},
    {'name': "Angelfish",           'price': 3000,'location': "River",                'size': "2",        'hours': "4 PM - 9 AM",              'months':["-","-","-","-","x","x","x","x","x","x","-","-"]},
    {'name': "Betta",               'price': 2500,'location': "River",                'size': "2",        'hours': "9 AM - 4 PM",              'months':["-","-","-","-","x","x","x","x","x","x","-","-"]},
    {'name': "Neon tetra",          'price':  500,'location': "River",                'size': "1",        'hours': "9 AM - 4 PM",              'months':["-","-","-","x","x","x","x","x","x","x","x","-"]},
    {'name': "Rainbowfish",         'price':  800,'location': "River",                'size': "1",        'hours': "9 AM - 4 PM",              'months':["-","-","-","-","x","x","x","x","x","x","-","-"]},
    {'name': "Piranha",             'price': 2500,'location': "River",                'size': "2",        'hours': "9 AM - 4 PM & 9 PM - 4 AM",'months':["-","-","-","-","-","x","x","x","x","-","-","-"]},
    {'name': "Arowana",             'price':10000,'location': "River",                'size': "4",        'hours': "4 PM - 9 AM",              'months':["-","-","-","-","-","x","x","x","x","-","-","-"]},
    {'name': "Dorado",              'price':15000,'location': "River",                'size': "5",        'hours': "4 AM - 9 PM",              'months':["-","-","-","-","-","x","x","x","x","-","-","-"]},
    {'name': "Gar",                 'price': 6000,'location': "Pond",                 'size': "5",        'hours': "4 PM - 9 AM",              'months':["-","-","-","-","-","x","x","x","x","-","-","-"]},
    {'name': "Arapaima",            'price':10000,'location': "River",                'size': "6",        'hours': "4 PM - 9 AM",              'months':["-","-","-","-","-","x","x","x","x","-","-","-"]},
    {'name': "Saddled bichir",      'price': 4000,'location': "River",                'size': "4",        'hours': "9 PM - 4 AM",              'months':["-","-","-","-","-","x","x","x","x","-","-","-"]},
    {'name': "Sturgeon",            'price':10000,'location': "River (Mouth)",        'size': "6",        'hours': "All day",                  'months':["x","x","x","-","-","-","-","-","x","x","x","x"]},
    {'name': "Sea butterfly",       'price': 1000,'location': "Sea",                  'size': "1",        'hours': "All day",                  'months':["x","x","x","-","-","-","-","-","-","-","-","x"]},
    {'name': "Sea horse",           'price': 1100,'location': "Sea",                  'size': "1",        'hours': "All day",                  'months':["-","-","-","x","x","x","x","x","x","x","x","-"]},
    {'name': "Clown fish",          'price':  650,'location': "Sea",                  'size': "1",        'hours': "All day",                  'months':["-","-","-","x","x","x","x","x","x","-","-","-"]},
    {'name': "Surgeonfish",         'price': 1000,'location': "Sea",                  'size': "2",        'hours': "All day",                  'months':["-","-","-","x","x","x","x","x","x","-","-","-"]},
    {'name': "Butterfly fish",      'price': 1000,'location': "Sea",                  'size': "2",        'hours': "All day",                  'months':["-","-","-","x","x","x","x","x","x","-","-","-"]},
    {'name': "Napoleonfish",        'price':10000,'location': "Sea",                  'size': "6",        'hours': "4 AM - 9 PM",              'months':["-","-","-","-","-","-","x","x","-","-","-","-"]},
    {'name': "Zebra turkeyfish",    'price':  500,'location': "Sea",                  'size': "3",        'hours': "All day",                  'months':["-","-","-","x","x","x","x","x","x","x","x","-"]},
    {'name': "Blowfish",            'price': 5000,'location': "Sea",                  'size': "3",        'hours': "9 PM - 4 AM",              'months':["x","x","-","-","-","-","-","-","-","-","x","x"]},
    {'name': "Puffer fish",         'price':  250,'location': "Sea",                  'size': "3",        'hours': "All day",                  'months':["-","-","-","-","-","-","x","x","x","-","-","-"]},
    {'name': "Anchovy",             'price':  200,'location': "Sea",                  'size': "2",        'hours': "4 AM - 9 PM",              'months':["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Horse mackerel",      'price':  150,'location': "Sea",                  'size': "2",        'hours': "All day",                  'months':["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Barred knifejaw",     'price': 5000,'location': "Sea",                  'size': "3",        'hours': "All day",                  'months':["-","-","x","x","x","x","x","x","x","x","x","-"]},
    {'name': "Sea bass",            'price':  400,'location': "Sea",                  'size': "5",        'hours': "All day",                  'months':["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Red snapper",         'price': 3000,'location': "Sea",                  'size': "4",        'hours': "All day",                  'months':["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Dab",                 'price':  300,'location': "Sea",                  'size': "3",        'hours': "All day",                  'months':["x","x","x","x","-","-","-","-","-","x","x","x"]},
    {'name': "Olive flounder",      'price':  800,'location': "Sea",                  'size': "5",        'hours': "All day",                  'months':["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Squid",               'price':  500,'location': "Sea",                  'size': "3",        'hours': "All day",                  'months':["x","x","x","x","x","x","x","x","-","-","-","x"]},
    {'name': "Moray eel",           'price': 2000,'location': "Sea",                  'size': "5 Narrow", 'hours': "All day",                  'months':["-","-","-","-","-","-","-","x","x","x","-","-"]},
    {'name': "Ribbon eel",          'price':  600,'location': "Sea",                  'size': "5 Narrow", 'hours': "All day",                  'months':["-","-","-","-","-","x","x","x","x","x","-","-"]},
    {'name': "Tuna",                'price': 7000,'location': "Pier",                 'size': "6",        'hours': "All day",                  'months':["x","x","x","x","-","-","-","-","-","-","x","x"]},
    {'name': "Blue marlin",         'price':10000,'location': "Pier",                 'size': "6",        'hours': "All day",                  'months':["x","x","x","x","-","-","x","x","x","-","x","x"]},
    {'name': "Giant trevally",      'price': 4500,'location': "Pier",                 'size': "5",        'hours': "All day",                  'months':["-","-","-","-","x","x","x","x","x","x","-","-"]},
    {'name': "Mahi-mahi",           'price': 6000,'location': "Pier",                 'size': "5",        'hours': "All day",                  'months':["-","-","-","-","x","x","x","x","x","x","-","-"]},
    {'name': "Ocean sunfish",       'price': 4000,'location': "Sea",                  'size': "6 (Fin)",  'hours': "4 AM - 9 PM",              'months':["-","-","-","-","-","-","x","x","x","-","-","-"]},
    {'name': "Ray",                 'price': 3000,'location': "Sea",                  'size': "5",        'hours': "4 AM - 9 PM",              'months':["-","-","-","-","-","-","-","x","x","x","x","-"]},
    {'name': "Saw shark",           'price':12000,'location': "Sea",                  'size': "6 (Fin)",  'hours': "4 PM - 9 AM",              'months':["-","-","-","-","-","x","x","x","x","-","-","-"]},
    {'name': "Hammerhead shark",    'price': 8000,'location': "Sea",                  'size': "6 (Fin)",  'hours': "4 PM - 9 AM",              'months':["-","-","-","-","-","x","x","x","x","-","-","-"]},
    {'name': "Great white shark",   'price':15000,'location': "Sea",                  'size': "6 (Fin)",  'hours': "4 PM - 9 AM",              'months':["-","-","-","-","-","x","x","x","x","-","-","-"]},
    {'name': "Whale shark",         'price':13000,'location': "Sea",                  'size': "6 (Fin)",  'hours': "All day",                  'months':["-","-","-","-","-","x","x","x","x","-","-","-"]},
    {'name': "Suckerfish",          'price': 1500,'location': "Sea",                  'size': "6 (Fin)",  'hours': "All day",                  'months':["-","-","-","-","-","x","x","x","x","-","-","-"]},
    {'name': "Football fish",       'price': 2500,'location': "Sea",                  'size': "4",        'hours': "4 PM - 9 AM",              'months':["x","x","x","-","-","-","-","-","-","-","x","x"]},
    {'name': "Oarfish",             'price': 9000,'location': "Sea",                  'size': "6",        'hours': "All day",                  'months':["x","x","x","x","x","-","-","-","-","-","-","x"]},
    {'name': "Barreleye",           'price':15000,'location': "Sea",                  'size': "2",        'hours': "9 PM - 4 AM",              'months':["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Coelacanth",          'price':15000,'location': "Sea",                  'size': "6",        'hours': "All day",                  'months':["x","x","x","x","x","x","x","x","x","x","x","x"]},
]
BUGS = [
    {'name': "Common butterfly",          'price':  160, 'location': "Flying",                            'hours': "4 AM - 7 PM",              'months': ["x","x","x","x","x","x","-","-","x","x","x","x"]},
    {'name': "Yellow butterfly",          'price':  160, 'location': "Flying",                            'hours': "4 AM - 7 PM",              'months': ["-","-","x","x","x","x","-","-","x","x","-","-"]},
    {'name': "Tiger butterfly",           'price':  240, 'location': "Flying",                            'hours': "4 AM - 7 PM",              'months': ["-","-","x","x","x","x","x","x","x","-","-","-"]},
    {'name': "Peacock butterfly",         'price': 2500, 'location': "Flying by Hybrid Flowers",          'hours': "4 AM - 7 PM",              'months': ["-","-","x","x","x","x","-","-","-","-","-","-"]},
    {'name': "Common bluebottle",         'price':  300, 'location': "Flying",                            'hours': "4 AM - 7 PM",              'months': ["-","-","-","x","x","x","x","x","-","-","-","-"]},
    {'name': "Paper kite butterfly",      'price': 1000, 'location': "Flying",                            'hours': "8 AM - 7 PM",              'months': ["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Great purple emperor",      'price': 3000, 'location': "Flying",                            'hours': "4 AM - 7 PM",              'months': ["-","-","-","-","x","x","x","x","-","-","-","-"]},
    {'name': "Monarch butterfly",         'price':  140, 'location': "Flying",                            'hours': "4 AM - 5 PM",              'months': ["-","-","-","-","-","-","-","-","x","x","x","-"]},
    {'name': "Emperor butterfly",         'price': 4000, 'location': "Flying",                            'hours': "5 PM - 8 AM",              'months': ["x","x","x","-","-","x","x","x","x","-","-","x"]},
    {'name': "Agrias butterfly",          'price': 3000, 'location': "Flying",                            'hours': "8 AM - 5 PM",              'months': ["-","-","-","x","x","x","x","x","x","-","-","-"]},
    {'name': "Rajah Brooke's birdwing",   'price': 2500, 'location': "Flying",                            'hours': "8 AM - 5 PM",              'months': ["x","x","-","x","x","x","x","x","x","-","-","x"]},
    {'name': "Queen Alexandra's birdwing",'price': 4000, 'location': "Flying",                            'hours': "8 AM - 4 PM",              'months': ["-","-","-","-","x","x","x","x","x","-","-","-"]},
    {'name': "Moth",                      'price':  130, 'location': "Flying by Light",                   'hours': "7 PM - 4 AM",              'months': ["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Atlas moth",                'price': 3000, 'location': "On Trees",                          'hours': "7 PM - 4 AM",              'months': ["-","-","-","x","x","x","x","x","x","-","-","-"]},
    {'name': "Madagascan sunset moth",    'price': 2500, 'location': "Flying",                            'hours': "8 AM - 4 PM",              'months': ["-","-","-","x","x","x","x","x","x","-","-","-"]},
    {'name': "Long locust",               'price':  200, 'location': "On the Ground",                     'hours': "8 AM - 7 PM",              'months': ["-","-","-","x","x","x","x","x","x","x","x","-"]},
    {'name': "Migratory locust",          'price':  600, 'location': "On the Ground",                     'hours': "8 AM - 7 PM",              'months': ["-","-","-","-","-","-","-","x","x","x","x","-"]},
    {'name': "Rice grasshopper",          'price':  160, 'location': "On the Ground",                     'hours': "8 AM - 7 PM",              'months': ["-","-","-","-","-","-","-","x","x","x","x","-"]},
    {'name': "Grasshopper",               'price':  160, 'location': "On the Ground",                     'hours': "8 AM - 5 PM",              'months': ["-","-","-","-","-","-","x","x","x","-","-","-"]},
    {'name': "Cricket",                   'price':  130, 'location': "On the Ground",                     'hours': "5 PM - 8 AM",              'months': ["-","-","-","-","-","-","-","-","x","x","x","-"]},
    {'name': "Bell cricket",              'price':  430, 'location': "On the Ground",                     'hours': "5 PM - 8 AM",              'months': ["-","-","-","-","-","-","-","-","x","x","-","-"]},
    {'name': "Mantis",                    'price':  430, 'location': "On Flowers",                        'hours': "8 AM - 5 PM",              'months': ["-","-","x","x","x","x","x","x","x","x","x","-"]},
    {'name': "Orchid mantis",             'price': 2400, 'location': "On Flowers (White)",                'hours': "8 AM - 5 PM",              'months': ["-","-","x","x","x","x","x","x","x","x","x","-"]},
    {'name': "Honeybee",                  'price':  200, 'location': "Flying",                            'hours': "8 AM - 5 PM",              'months': ["-","-","x","x","x","x","x","-","-","-","-","-"]},
    {'name': "Wasp",                      'price': 2500, 'location': "Shaking Trees",                     'hours': "All day",                  'months': ["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Brown cicada",              'price':  250, 'location': "On Trees",                          'hours': "8 AM - 5 PM",              'months': ["-","-","-","-","-","-","x","x","-","-","-","-"]},
    {'name': "Robust cicada",             'price':  300, 'location': "On Trees",                          'hours': "8 AM - 5 PM",              'months': ["-","-","-","-","-","-","x","x","-","-","-","-"]},
    {'name': "Giant cicada",              'price':  500, 'location': "On Trees",                          'hours': "8 AM - 5 PM",              'months': ["-","-","-","-","-","-","x","x","-","-","-","-"]},
    {'name': "Walker cicada",             'price':  400, 'location': "On Trees",                          'hours': "8 AM - 5 PM",              'months': ["-","-","-","-","-","-","-","x","x","-","-","-"]},
    {'name': "Evening cicada",            'price':  550, 'location': "On Trees",                          'hours': "4 AM - 8 AM & 4 PM - 7 PM",'months': ["-","-","-","-","-","-","x","x","-","-","-","-"]},
    {'name': "Cicada shell",              'price':   10, 'location': "On Trees",                          'hours': "All day",                  'months': ["-","-","-","-","-","-","x","x","-","-","-","-"]},
    {'name': "Red dragonfly",             'price':  180, 'location': "Flying",                            'hours': "8 AM - 7 PM",              'months': ["-","-","-","-","-","-","-","-","x","x","-","-"]},
    {'name': "Darner dragonfly",          'price':  230, 'location': "Flying",                            'hours': "8 AM - 5 PM",              'months': ["-","-","-","x","x","x","x","x","x","x","-","-"]},
    {'name': "Banded dragonfly",          'price': 4500, 'location': "Flying",                            'hours': "8 AM - 5 PM",              'months': ["-","-","-","-","x","x","x","x","x","x","-","-"]},
    {'name': "Damselfly",                 'price':  500, 'location': "Flying",                            'hours': "All day",                  'months': ["x","x","-","-","-","-","-","-","-","-","x","x"]},
    {'name': "Firefly",                   'price':  300, 'location': "Flying",                            'hours': "7 PM - 4 AM",              'months': ["-","-","-","-","-","x","-","-","-","-","-","-"]},
    {'name': "Mole cricket",              'price':  500, 'location': "Underground",                       'hours': "All day",                  'months': ["x","x","x","x","x","-","-","-","-","-","x","x"]},
    {'name': "Pondskater",                'price':  130, 'location': "On Ponds and Rivers",               'hours': "8 AM - 7 PM",              'months': ["-","-","-","-","x","x","x","x","x","-","-","-"]},
    {'name': "Diving beetle",             'price':  800, 'location': "On Ponds and Rivers",               'hours': "8 AM - 7 PM",              'months': ["-","-","-","-","x","x","x","x","x","-","-","-"]},
    {'name': "Giant water bug",           'price': 2000, 'location': "On Ponds and Rivers",               'hours': "7 PM - 8 AM",              'months': ["-","-","-","x","x","x","x","x","x","-","-","-"]},
    {'name': "Stinkbug",                  'price':  120, 'location': "On Flowers",                        'hours': "All day",                  'months': ["-","-","x","x","x","x","x","x","x","x","-","-"]},
    {'name': "Man-faced stink bug",       'price': 1000, 'location': "On Flowers",                        'hours': "7 PM - 8 AM",              'months': ["-","-","x","x","x","x","x","x","x","x","-","-"]},
    {'name': "Ladybug",                   'price':  200, 'location': "On Flowers",                        'hours': "8 AM - 5 PM",              'months': ["-","-","x","x","x","x","-","-","-","x","-","-"]},
    {'name': "Tiger beetle",              'price': 1500, 'location': "On the Ground",                     'hours': "All day",                  'months': ["-","x","x","x","x","x","x","x","x","x","-","-"]},
    {'name': "Jewel beetle",              'price': 2400, 'location': "On Tree Stumps",                    'hours': "All day",                  'months': ["-","-","-","x","x","x","x","x","-","-","-","-"]},
    {'name': "Violin beetle",             'price':  450, 'location': "On Tree Stumps",                    'hours': "All day",                  'months': ["-","-","-","-","x","x","-","-","x","x","x","-"]},
    {'name': "Citrus long-horned beetle", 'price':  350, 'location': "On Tree Stumps",                    'hours': "All day",                  'months': ["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Rosalia batesi beetle",     'price': 3000, 'location': "On Tree Stumps",                    'hours': "All day",                  'months': ["-","-","-","-","x","x","x","x","x","-","-","-"]},
    {'name': "Blue weevil beetle",        'price':  800, 'location': "On Trees (Coconut)",                'hours': "All day",                  'months': ["-","-","-","-","-","-","x","x","-","-","-","-"]},
    {'name': "Dung beetle",               'price': 3000, 'location': "On the Ground (rolling snowballs)", 'hours': "All day",                  'months': ["x","x","-","-","-","-","-","-","-","-","-","x"]},
    {'name': "Earth-boring dung beetle",  'price':  300, 'location': "On the Ground",                     'hours': "All day",                  'months': ["-","-","-","-","-","-","x","x","x","-","-","-"]},
    {'name': "Scarab beetle",            'price': 10000, 'location': "On Trees",                          'hours': "11 PM - 8 AM",             'months': ["-","-","-","-","-","-","x","x","-","-","-","-"]},
    {'name': "Drone beetle",              'price':  200, 'location': "On Trees",                          'hours': "All day",                  'months': ["-","-","-","-","-","x","x","x","-","-","-","-"]},
    {'name': "Goliath beetle",            'price': 8000, 'location': "On Trees (Coconut)",                'hours': "5 PM - 8 AM",              'months': ["-","-","-","-","-","x","x","x","x","-","-","-"]},
    {'name': "Saw stag",                  'price': 2000, 'location': "On Trees",                          'hours': "All day",                  'months': ["-","-","-","-","-","-","x","x","-","-","-","-"]},
    {'name': "Miyama stag",               'price': 1000, 'location': "On Trees",                          'hours': "All day",                  'months': ["-","-","-","-","-","-","x","x","-","-","-","-"]},
    {'name': "Giant stag",               'price': 10000, 'location': "On Trees",                          'hours': "11 PM - 8 AM",             'months': ["-","-","-","-","-","-","x","x","-","-","-","-"]},
    {'name': "Rainbow stag",              'price': 6000, 'location': "On Trees",                          'hours': "7 PM - 8 AM",              'months': ["-","-","-","-","-","x","x","x","x","-","-","-"]},
    {'name': "Cyclommatus stag",          'price': 8000, 'location': "On Trees (Coconut)",                'hours': "5 PM - 8 AM",              'months': ["-","-","-","-","-","-","x","x","-","-","-","-"]},
    {'name': "Golden stag",              'price': 12000, 'location': "On Trees (Coconut)",                'hours': "5 PM - 8 AM",              'months': ["-","-","-","-","-","-","x","x","-","-","-","-"]},
    {'name': "Giraffe stag",             'price': 12000, 'location': "On Trees (Coconut)",                'hours': "5 PM - 8 AM",              'months': ["-","-","-","-","-","-","x","x","-","-","-","-"]},
    {'name': "Horned dynastid",           'price': 1350, 'location': "On Trees",                          'hours': "5 PM - 8 AM",              'months': ["-","-","-","-","-","-","x","x","-","-","-","-"]},
    {'name': "Horned atlas",              'price': 8000, 'location': "On Trees (Coconut)",                'hours': "5 PM - 8 AM",              'months': ["-","-","-","-","-","-","x","x","-","-","-","-"]},
    {'name': "Horned elephant",           'price': 8000, 'location': "On Trees (Coconut)",                'hours': "5 PM - 8 AM",              'months': ["-","-","-","-","-","-","x","x","-","-","-","-"]},
    {'name': "Horned hercules",          'price': 12000, 'location': "On Trees (Coconut)",                'hours': "5 PM - 8 AM",              'months': ["-","-","-","-","-","-","x","x","-","-","-","-"]},
    {'name': "Walking stick",             'price':  600, 'location': "On Trees",                          'hours': "4 AM - 8 AM & 5 PM - 7 PM",'months': ["-","-","-","-","-","-","x","x","x","x","x","-"]},
    {'name': "Walking leaf",              'price':  600, 'location': "Under Trees Disguised as Leaves",   'hours': "All day",                  'months': ["-","-","-","-","-","-","x","x","x","-","-","-"]},
    {'name': "Bagworm",                   'price':  600, 'location': "Shaking Trees",                     'hours': "All day",                  'months': ["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Ant",                       'price':   80, 'location': "On rotten food",                    'hours': "All day",                  'months': ["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Hermit crab",               'price': 1000, 'location': "Beach disguised as Shells",         'hours': "7 PM - 8 AM",              'months': ["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Wharf roach",               'price':  200, 'location': "On Beach Rocks",                    'hours': "All day",                  'months': ["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Fly",                       'price':   60, 'location': "On Trash Items",                    'hours': "All day",                  'months': ["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Mosquito",                  'price':  130, 'location': "Flying",                            'hours': "5 PM - 4 AM",              'months': ["-","-","-","-","-","x","x","x","x","-","-","-"]},
    {'name': "Flea",                      'price':   70, 'location': "Villager's Heads",                  'hours': "All day",                  'months': ["-","-","-","x","x","x","x","x","x","x","x","-"]},
    {'name': "Snail",                     'price':  250, 'location': "On Rocks and Bushes (Rain)",        'hours': "All day",                  'months': ["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Pill bug",                  'price':  250, 'location': "Hitting Rocks",                     'hours': "11 PM - 4 PM",             'months': ["x","x","x","x","x","x","-","-","x","x","x","x"]},
    {'name': "Centipede",                 'price':  300, 'location': "Hitting Rocks",                     'hours': "4 PM - 11 PM",             'months': ["x","x","x","x","x","x","-","-","x","x","x","x"]},
    {'name': "Spider",                    'price':  600, 'location': "Shaking Trees",                     'hours': "7 PM - 8 AM",              'months': ["x","x","x","x","x","x","x","x","x","x","x","x"]},
    {'name': "Tarantula",                 'price': 8000, 'location': "On the Ground",                     'hours': "7 PM - 4 AM",              'months': ["x","x","x","x","-","-","-","-","-","-","x","x"]},
    {'name': "Scorpion",                  'price': 8000, 'location': "On the Ground",                     'hours': "7 PM - 4 AM",              'months': ["-","-","-","-","x","x","x","x","x","x","-","-"]},
]
MONTHS = [
    1,
    1 << 1,
    1 << 2,
    1 << 3,
    1 << 4,
    1 << 5,
    1 << 6,
    1 << 7,
    1 << 8,
    1 << 9,
    1 << 10,
    1 << 11,
]

CREATURES = [
    {'name': 'Seaweed',             'price':   600, 'size': 'Large', 'speed':  'Stationary','hours': 'All day',              'months': ['x','x','x','x','x','x','x','-','-','x','x','x']},
    {'name': 'Sea grapes',          'price':   900, 'size': 'Small', 'speed':  'Stationary','hours': 'All day',              'months': ['-','-','-','-','-','x','x','x','x','-','-','-']},
    {'name': 'Sea cucumber',        'price':   500, 'size': 'Medium', 'speed': 'Very slow', 'hours': 'All day',              'months': ['x','x','x','x','-','-','-','-','-','-','x','x']},
    {'name': 'Sea pig',             'price': 10000, 'size': 'Small', 'speed':  'Very fast', 'hours': '4pm - 9am',            'months': ['x','x','-','-','-','-','-','-','-','-','x','x']},
    {'name': 'Sea star',            'price':   500, 'size': 'Small', 'speed':  'Very slow', 'hours': 'All day',              'months': ['x','x','x','x','x','x','x','x','x','x','x','x']},
    {'name': 'Sea urchin',          'price':  1700, 'size': 'Small', 'speed':  'Slow',      'hours': 'All day',              'months': ['-','-','-','-','x','x','x','x','x','-','-','-']},
    {'name': 'Slate pencil urchin', 'price':  2000, 'size': 'Medium', 'speed': 'Medium',    'hours': '4pm - 9am',            'months': ['-','-','-','-','x','x','x','x','x','-','-','-']},
    {'name': 'Sea anemone',         'price':   500, 'size': 'Large', 'speed':  'Stationary','hours': 'All day',              'months': ['x','x','x','x','x','x','x','x','x','x','x','x']},
    {'name': 'Moon jellyfish',      'price':   600, 'size': 'Small', 'speed':  'Very slow', 'hours': 'All day',              'months': ['-','-','-','-','-','-','x','x','x','-','-','-']},
    {'name': 'Sea slug',            'price':   600, 'size': 'Tiny', 'speed':   'Very slow', 'hours': 'All day',              'months': ['x','x','x','x','x','x','x','x','x','x','x','x']},
    {'name': 'Pearl oyster',        'price':  2800, 'size': 'Small', 'speed':  'Medium',    'hours': 'All day',              'months': ['x','x','x','x','x','x','x','x','x','x','x','x']},
    {'name': 'Mussel',              'price':  1500, 'size': 'Small', 'speed':  'Slow',      'hours': 'All day',              'months': ['-','-','-','-','-','x','x','x','x','x','x','x']},
    {'name': 'Oyster',              'price':  1100, 'size': 'Small', 'speed':  'Slow',      'hours': 'All day',              'months': ['x','x','-','-','-','-','-','-','x','x','x','x']},
    {'name': 'Scallop',             'price':  1200, 'size': 'Medium', 'speed': 'Slow',      'hours': 'All day',              'months': ['x','x','x','x','x','x','x','x','x','x','x','x']},
    {'name': 'Whelk',               'price':  1000, 'size': 'Small', 'speed':  'Slow',      'hours': 'All day',              'months': ['x','x','x','x','x','x','x','x','x','x','x','x']},
    {'name': 'Turban shell',        'price':  1000, 'size': 'Small', 'speed':  'Slow',      'hours': 'All day',              'months': ['-','-','x','x','x','-','-','-','x','x','x','x']},
    {'name': 'Abalone',             'price':  2000, 'size': 'Medium', 'speed': 'Medium',    'hours': '4pm - 9am',            'months': ['x','-','-','-','-','x','x','x','x','x','x','x']},
    {'name': 'Gigas giant clam',    'price': 15000, 'size': 'Huge', 'speed':   'Very fast', 'hours': 'All day',              'months': ['-','-','-','-','x','x','x','x','x','-','-','-']},
    {'name': 'Chambered nautilus',  'price':  1800, 'size': 'Medium', 'speed': 'Medium',    'hours': '4pm - 9am',            'months': ['-','-','x','x','x','x','-','-','x','x','x','-']},
    {'name': 'Octopus',             'price':  1200, 'size': 'Medium', 'speed': 'Slow',      'hours': 'All day',              'months': ['x','x','x','x','x','x','x','x','x','x','x','x']},
    {'name': 'Umbrella octopus',    'price':  6000, 'size': 'Small', 'speed':  'Fast',      'hours': 'All day',              'months': ['-','-','x','x','x','-','-','-','x','x','x','-']},
    {'name': 'Vampire squid',       'price': 10000, 'size': 'Medium', 'speed': 'Very fast', 'hours': '4pm - 9am',            'months': ['-','-','-','-','x','x','x','x','-','-','-','-']},
    {'name': 'Firefly squid',       'price':  1400, 'size': 'Tiny', 'speed':   'Slow',      'hours': '9pm - 4am',            'months': ['-','-','x','x','x','x','-','-','-','-','-','-']},
    {'name': 'Gazami crab',         'price':  2200, 'size': 'Medium', 'speed': 'Medium',    'hours': 'All day',              'months': ['-','-','-','-','-','x','x','x','x','x','x','-']},
    {'name': 'Dungeness crab',      'price':  1900, 'size': 'Medium', 'speed': 'Medium',    'hours': 'All day',              'months': ['x','x','x','x','x','-','-','-','-','-','x','x']},
    {'name': 'Snow crab',           'price':  6000, 'size': 'Large', 'speed':  'Fast',      'hours': 'All day',              'months': ['x','x','x','x','-','-','-','-','-','-','x','x']},
    {'name': 'Red king crab',       'price':  8000, 'size': 'Large', 'speed':  'Very fast', 'hours': 'All day',              'months': ['x','x','x','-','-','-','-','-','-','-','x','x']},
    {'name': 'Acorn barnacle',      'price':   600, 'size': 'Tiny', 'speed':   'Stationary','hours': 'All day',              'months': ['x','x','x','x','x','x','x','x','x','x','x','x']},
    {'name': 'Spider crab',         'price': 12000, 'size': 'Huge', 'speed':   'Very fast', 'hours': 'All day',              'months': ['-','-','x','x','-','-','-','-','-','-','-','-']},
    {'name': 'Tiger prawn',         'price':  3000, 'size': 'Small', 'speed':  'Medium',    'hours': '4pm - 9am',            'months': ['-','-','-','-','-','x','x','x','x','-','-','-']},
    {'name': 'Sweet shrimp',        'price':  1400, 'size': 'Small', 'speed':  'Slow',      'hours': '4pm - 9am',            'months': ['x','x','-','-','-','-','-','-','x','x','x','x']},
    {'name': 'Mantis shrimp',       'price':  2500, 'size': 'Small', 'speed':  'Medium',    'hours': '4pm - 9am',            'months': ['x','x','x','x','x','x','x','x','x','x','x','x']},
    {'name': 'Spiny lobster',       'price':  5000, 'size': 'Large', 'speed':  'Fast',      'hours': '9pm - 4am',            'months': ['-','-','-','-','-','-','-','-','-','x','x','x']},
    {'name': 'Lobster',             'price':  4500, 'size': 'Large', 'speed':  'Fast',      'hours': 'All day',              'months': ['x','-','-','x','x','x','-','-','-','-','-','x']},
    {'name': 'Giant isopod',        'price': 12000, 'size': 'Medium', 'speed': 'Very fast', 'hours': '9am - 4pm & 9pm - 4am','months': ['-','-','-','-','-','-','x','x','x','x','-','-']},
    {'name': 'Horseshoe Crab',      'price':  2500, 'size': 'Medium', 'speed': 'Medium',    'hours': '9pm - 4am',            'months': ['-','-','-','-','-','-','x','x','x','-','-','-']},
    {'name': 'Sea pineapple',       'price':  1500, 'size': 'Small', 'speed':  'Slow',      'hours': 'All day',              'months': ['-','-','-','x','x','x','x','x','-','-','-','-']},
    {'name': 'Spotted garden eel',  'price':  1100, 'size': 'Small', 'speed':  'Slow',      'hours': '4am - 9pm',            'months': ['-','-','-','-','x','x','x','x','x','x','-','-']},
    {'name': 'Flatworm',            'price':   700, 'size': 'Tiny', 'speed':   'Very slow', 'hours': '4pm - 9am',            'months': ['-','-','-','-','-','-','-','x','x','-','-','-']},
    {'name': 'Venus flower basket', 'price':  5000, 'size': 'Medium', 'speed': 'Fast',      'hours': 'All day',              'months': ['x','x','-','-','-','-','-','-','-','x','x','x']}
]

conn = sqlite3.connect("acnh.sqlite")
cur = conn.cursor()
conn.execute('CREATE TABLE fish          (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT, price INTEGER, location TEXT,        shadow TEXT, available_hours INTEGER, available_months INTEGER, caught BOOL, donated BOOL)')
conn.execute('CREATE TABLE bugs          (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT, price INTEGER, location TEXT,                     available_hours INTEGER, available_months INTEGER, caught BOOL, donated BOOL)')
conn.execute('CREATE TABLE sea_creatures (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT, price INTEGER, shadow_size INTEGER,  speed TEXT,  available_hours INTEGER, available_months INTEGER, caught BOOL, donated BOOL)')
INSERT_FISH =      'INSERT INTO fish          (name, price, available_hours, available_months, location,   shadow,  caught, donated) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
INSERT_BUGS =      'INSERT INTO bugs          (name, price, available_hours, available_months, location,            caught, donated) VALUES (?, ?, ?, ?, ?, ?, ?)'
INSERT_CREATURES = 'INSERT INTO sea_creatures (name, price, available_hours, available_months, shadow_size, speed,  caught, donated) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'

def times(val):
    if val == 'All day':
        return 4294967295 # u32 max
    if '&' in val:
        parts = val.split('&')
        return time_pair(parts[0]) | time_pair(parts[1])
    else:
        return time_pair(val)

# Convert a time pair (eg 4 PM - 8 AM) into a
# bit mask of the available hours
#   23  22  21  20  19  18  17  16  15  14  13  12  11  10   9   8   7   6   5   4   2   2   1   0
# | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
def time_pair(val):
    parts = val.split(' - ')
    start = time_part(parts[0])
    end = time_part(parts[1])
    ret = 0
    # If start is > than end it wraps around midnight
    # Here will will need to include from the start of this
    # pair until midnight
    # and then also include midnight until the end
    if start > end:
        for i in range(start+1, 25):
            ret |= 1 << i
        for i in range(1, end+1):
            ret |= 1 << i
    else:
        for i in range(start+1, end+1):
            ret |= 1 << i
    return ret

def time_part(val):
    n = int(val.strip()[0])
    if 'PM' in val and n != 12:
        n += 12
    elif 'AM' in val and n == 12:
        n = 0
    return n

ACTIVITIES = [
    ('fish',               FISH,      INSERT_FISH),
    ('bugs',               BUGS,      INSERT_BUGS),
    ('sea_creatures', CREATURES, INSERT_CREATURES),
]

def parse_months(months):
    month_mask = 0
    for (i, check) in enumerate(months):
        if check == 'x':
            month_mask |= MONTHS[i]
    return month_mask

def params_for(table, d):
    # all inserts start with these
    params = [
        d['name'],
        d['price'],
        times(d['hours']),
        parse_months(d['months']),
    ]
    # the 3 tables have varing different fields
    if table == 'fish':
        params.append(d['location'])
        params.append(d['size'])
    elif table == 'bugs':
        params.append(d['location'])
    elif table == 'sea_creatures':
        params.append(d['size'])
        params.append(d['speed'])
    # All insert statements end with caught and donated
    # which will default to false
    params.append(False)
    params.append(False)
    return params


for (table, rows, insert) in ACTIVITIES:
    print(f'inserting into {table}')
    
    for row in rows:
        params = params_for(table, row)
        values = ','.join('?' * len(params))
        print(params)
        cur.execute(insert, params)

conn.commit()
conn.close()