import csv, sqlite3
FISH = [
    ["Bitterling",           900,"River",                "1",      "All day",                  "x","x","x","-","-","-","-","-","-","-","x","x"],
    ["Pale chub",            200,"River",                "1",      "9 AM - 4 PM",              "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Crucian carp",         160,"River",                "2",      "All day",                  "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Dace",                 240,"River",                "3",      "4 PM - 9 AM",              "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Carp",                 300,"Pond",                 "4",      "All day",                  "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Koi",                 4000,"Pond",                 "4",      "4 PM - 9 AM",              "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Goldfish",            1300,"Pond",                 "1",      "All day",                  "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Pop-eyed goldfish",   1300,"Pond",                 "1",      "9 AM - 4 PM",              "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Ranchu goldfish",     4500,"Pond",                 "2",      "9 AM - 4 PM",              "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Killifish",            300,"Pond",                 "1",      "All day",                  "-","-","-","x","x","x","x","x","-","-","-","-"],
    ["Crawfish",             200,"Pond",                 "2",      "All day",                  "-","-","-","x","x","x","x","x","x","-","-","-"],
    ["Soft-shelled turtle", 3750,"River",                "4",      "4 PM - 9 AM",              "-","-","-","-","-","-","-","x","x","-","-","-"],
    ["Snapping Turtle",     5000,"River",                "4",      "9 PM - 4 AM",              "-","-","-","x","x","x","x","x","x","x","-","-"],
    ["Tadpole",              100,"Pond",                 "1",      "All day",                  "-","-","x","x","x","x","x","-","-","-","-","-"],
    ["Frog",                 120,"Pond",                 "2",      "All day",                  "-","-","-","-","x","x","x","x","-","-","-","-"],
    ["Freshwater goby",      400,"River",                "2",      "4 PM - 9 AM",              "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Loach",                400,"River",                "2",      "All day",                  "-","-","x","x","x","-","-","-","-","-","-","-"],
    ["Catfish",              800,"Pond",                 "4",      "4 PM - 9 AM",              "-","-","-","-","x","x","x","x","x","x","-","-"],
    ["Giant snakehead",     5500,"Pond",                 "4",      "9 AM - 4 PM",              "-","-","-","-","-","x","x","x","-","-","-","-"],
    ["Bluegill",             180,"River",                "2",      "9 AM - 4 PM",              "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Yellow perch",         300,"River",                "3",      "All day",                  "x","x","x","-","-","-","-","-","-","x","x","x"],
    ["Black bass",           400,"River",                "4",      "All day",                  "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Tilapia",              800,"River",                "3",      "All day",                  "-","-","-","-","-","x","x","x","x","x","-","-"],
    ["Pike",                1800,"River",                "5",      "All day",                  "-","-","-","-","-","-","-","-","x","x","x","x"],
    ["Pond smelt",           500,"River",                "2",      "All day",                  "x","x","-","-","-","-","-","-","-","-","-","x"],
    ["Sweetfish",            900,"River",                "3",      "All day",                  "-","-","-","-","-","-","x","x","x","-","-","-"],
    ["Cherry salmon",       1000,"River (Clifftop)",     "3",      "4 PM - 9 AM",              "-","-","x","x","x","x","-","-","x","x","x","-"],
    ["Char",                3800,"River (Clifftop) Pond","3",      "4 PM - 9 AM",              "-","-","x","x","x","x","-","-","x","x","x","-"],
    ["Golden trout",       15000,"River (Clifftop)",     "3",      "4 PM - 9 AM",              "-","-","x","x","x","-","-","-","x","x","x","-"],
    ["Stringfish",         15000,"River (Clifftop)",     "5",      "4 PM - 9 AM",              "x","x","x","-","-","-","-","-","-","-","-","x"],
    ["Salmon",               700,"River (Mouth)",        "4",      "All day",                  "-","-","-","-","-","-","-","-","x","-","-","-"],
    ["King salmon",         1800,"River (Mouth)",        "6",      "All day",                  "-","-","-","-","-","-","-","-","x","-","-","-"],
    ["Mitten crab",         2000,"River",                "2",      "4 PM - 9 AM",              "-","-","-","-","-","-","-","-","x","x","x","-"],
    ["Guppy",               1300,"River",                "1",      "9 AM - 4 PM",              "-","-","-","x","x","x","x","x","x","x","x","-"],
    ["Nibble fish",         1500,"River",                "1",      "9 AM - 4 PM",              "-","-","-","-","x","x","x","x","x","-","-","-"],
    ["Angelfish",           3000,"River",                "2",      "4 PM - 9 AM",              "-","-","-","-","x","x","x","x","x","x","-","-"],
    ["Betta",               2500,"River",                "2",      "9 AM - 4 PM",              "-","-","-","-","x","x","x","x","x","x","-","-"],
    ["Neon tetra",           500,"River",                "1",      "9 AM - 4 PM",              "-","-","-","x","x","x","x","x","x","x","x","-"],
    ["Rainbowfish",          800,"River",                "1",      "9 AM - 4 PM",              "-","-","-","-","x","x","x","x","x","x","-","-"],
    ["Piranha",             2500,"River",                "2",      "9 AM - 4 PM & 9 PM - 4 AM","-","-","-","-","-","x","x","x","x","-","-","-"],
    ["Arowana",            10000,"River",                "4",      "4 PM - 9 AM",              "-","-","-","-","-","x","x","x","x","-","-","-"],
    ["Dorado",             15000,"River",                "5",      "4 AM - 9 PM",              "-","-","-","-","-","x","x","x","x","-","-","-"],
    ["Gar",                 6000,"Pond",                 "5",      "4 PM - 9 AM",              "-","-","-","-","-","x","x","x","x","-","-","-"],
    ["Arapaima",           10000,"River",                "6",      "4 PM - 9 AM",              "-","-","-","-","-","x","x","x","x","-","-","-"],
    ["Saddled bichir",      4000,"River",                "4",      "9 PM - 4 AM",              "-","-","-","-","-","x","x","x","x","-","-","-"],
    ["Sturgeon",           10000,"River (Mouth)",        "6",      "All day",                  "x","x","x","-","-","-","-","-","x","x","x","x"],
    ["Sea butterfly",       1000,"Sea",                  "1",      "All day",                  "x","x","x","-","-","-","-","-","-","-","-","x"],
    ["Sea horse",           1100,"Sea",                  "1",      "All day",                  "-","-","-","x","x","x","x","x","x","x","x","-"],
    ["Clown fish",           650,"Sea",                  "1",      "All day",                  "-","-","-","x","x","x","x","x","x","-","-","-"],
    ["Surgeonfish",         1000,"Sea",                  "2",      "All day",                  "-","-","-","x","x","x","x","x","x","-","-","-"],
    ["Butterfly fish",      1000,"Sea",                  "2",      "All day",                  "-","-","-","x","x","x","x","x","x","-","-","-"],
    ["Napoleonfish",       10000,"Sea",                  "6",      "4 AM - 9 PM",              "-","-","-","-","-","-","x","x","-","-","-","-"],
    ["Zebra turkeyfish",     500,"Sea",                  "3",      "All day",                  "-","-","-","x","x","x","x","x","x","x","x","-"],
    ["Blowfish",            5000,"Sea",                  "3",      "9 PM - 4 AM",              "x","x","-","-","-","-","-","-","-","-","x","x"],
    ["Puffer fish",          250,"Sea",                  "3",      "All day",                  "-","-","-","-","-","-","x","x","x","-","-","-"],
    ["Anchovy",              200,"Sea",                  "2",      "4 AM - 9 PM",              "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Horse mackerel",       150,"Sea",                  "2",      "All day",                  "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Barred knifejaw",     5000,"Sea",                  "3",      "All day",                  "-","-","x","x","x","x","x","x","x","x","x","-"],
    ["Sea bass",             400,"Sea",                  "5",      "All day",                  "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Red snapper",         3000,"Sea",                  "4",      "All day",                  "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Dab",                  300,"Sea",                  "3",      "All day",                  "x","x","x","x","-","-","-","-","-","x","x","x"],
    ["Olive flounder",       800,"Sea",                  "5",      "All day",                  "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Squid",                500,"Sea",                  "3",      "All day",                  "x","x","x","x","x","x","x","x","-","-","-","x"],
    ["Moray eel",           2000,"Sea",                  "Narrow", "All day",                  "-","-","-","-","-","-","-","x","x","x","-","-"],
    ["Ribbon eel",           600,"Sea",                  "Narrow", "All day",                  "-","-","-","-","-","x","x","x","x","x","-","-"],
    ["Tuna",                7000,"Pier",                 "6",      "All day",                  "x","x","x","x","-","-","-","-","-","-","x","x"],
    ["Blue marlin",        10000,"Pier",                 "6",      "All day",                  "x","x","x","x","-","-","x","x","x","-","x","x"],
    ["Giant trevally",      4500,"Pier",                 "5",      "All day",                  "-","-","-","-","x","x","x","x","x","x","-","-"],
    ["Mahi-mahi",           6000,"Pier",                 "5",      "All day",                  "-","-","-","-","x","x","x","x","x","x","-","-"],
    ["Ocean sunfish",       4000,"Sea",                  "6 (Fin)","4 AM - 9 PM",              "-","-","-","-","-","-","x","x","x","-","-","-"],
    ["Ray",                 3000,"Sea",                  "5",      "4 AM - 9 PM",              "-","-","-","-","-","-","-","x","x","x","x","-"],
    ["Saw shark",          12000,"Sea",                  "6 (Fin)","4 PM - 9 AM",              "-","-","-","-","-","x","x","x","x","-","-","-"],
    ["Hammerhead shark",    8000,"Sea",                  "6 (Fin)","4 PM - 9 AM",              "-","-","-","-","-","x","x","x","x","-","-","-"],
    ["Great white shark",  15000,"Sea",                  "6 (Fin)","4 PM - 9 AM",              "-","-","-","-","-","x","x","x","x","-","-","-"],
    ["Whale shark",        13000,"Sea",                  "6 (Fin)","All day",                  "-","-","-","-","-","x","x","x","x","-","-","-"],
    ["Suckerfish",          1500,"Sea",                  "6 (Fin)","All day",                  "-","-","-","-","-","x","x","x","x","-","-","-"],
    ["Football fish",       2500,"Sea",                  "4",      "4 PM - 9 AM",              "x","x","x","-","-","-","-","-","-","-","x","x"],
    ["Oarfish",             9000,"Sea",                  "6",      "All day",                  "x","x","x","x","x","-","-","-","-","-","-","x"],
    ["Barreleye",          15000,"Sea",                  "2",      "9 PM - 4 AM",              "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Coelacanth",         15000,"Sea",                  "6",      "All day",                  "x","x","x","x","x","x","x","x","x","x","x","x"],
]
BUGS = [
    ["Common butterfly",           160,"Flying",                            "4 AM - 7 PM",              "x","x","x","x","x","x","-","-","x","x","x","x"],
    ["Yellow butterfly",           160,"Flying",                            "4 AM - 7 PM",              "-","-","x","x","x","x","-","-","x","x","-","-"],
    ["Tiger butterfly",            240,"Flying",                            "4 AM - 7 PM",              "-","-","x","x","x","x","x","x","x","-","-","-"],
    ["Peacock butterfly",         2500,"Flying by Hybrid Flowers",          "4 AM - 7 PM",              "-","-","x","x","x","x","-","-","-","-","-","-"],
    ["Common bluebottle",          300,"Flying",                            "4 AM - 7 PM",              "-","-","-","x","x","x","x","x","-","-","-","-"],
    ["Paper kite butterfly",      1000,"Flying",                            "8 AM - 7 PM",              "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Great purple emperor",      3000,"Flying",                            "4 AM - 7 PM",              "-","-","-","-","x","x","x","x","-","-","-","-"],
    ["Monarch butterfly",          140,"Flying",                            "4 AM - 5 PM",              "-","-","-","-","-","-","-","-","x","x","x","-"],
    ["Emperor butterfly",         4000,"Flying",                            "5 PM - 8 AM",              "x","x","x","-","-","x","x","x","x","-","-","x"],
    ["Agrias butterfly",          3000,"Flying",                            "8 AM - 5 PM",              "-","-","-","x","x","x","x","x","x","-","-","-"],
    ["Rajah Brooke's birdwing",   2500,"Flying",                            "8 AM - 5 PM",              "x","x","-","x","x","x","x","x","x","-","-","x"],
    ["Queen Alexandra's birdwing",4000,"Flying",                            "8 AM - 4 PM",              "-","-","-","-","x","x","x","x","x","-","-","-"],
    ["Moth",                       130,"Flying by Light",                   "7 PM - 4 AM",              "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Atlas moth",                3000,"On Trees",                          "7 PM - 4 AM",              "-","-","-","x","x","x","x","x","x","-","-","-"],
    ["Madagascan sunset moth",    2500,"Flying",                            "8 AM - 4 PM",              "-","-","-","x","x","x","x","x","x","-","-","-"],
    ["Long locust",                200,"On the Ground",                     "8 AM - 7 PM",              "-","-","-","x","x","x","x","x","x","x","x","-"],
    ["Migratory locust",           600,"On the Ground",                     "8 AM - 7 PM",              "-","-","-","-","-","-","-","x","x","x","x","-"],
    ["Rice grasshopper",           160,"On the Ground",                     "8 AM - 7 PM",              "-","-","-","-","-","-","-","x","x","x","x","-"],
    ["Grasshopper",                160,"On the Ground",                     "8 AM - 5 PM",              "-","-","-","-","-","-","x","x","x","-","-","-"],
    ["Cricket",                    130,"On the Ground",                     "5 PM - 8 AM",              "-","-","-","-","-","-","-","-","x","x","x","-"],
    ["Bell cricket",               430,"On the Ground",                     "5 PM - 8 AM",              "-","-","-","-","-","-","-","-","x","x","-","-"],
    ["Mantis",                     430,"On Flowers",                        "8 AM - 5 PM",              "-","-","x","x","x","x","x","x","x","x","x","-"],
    ["Orchid mantis",             2400,"On Flowers (White)",                "8 AM - 5 PM",              "-","-","x","x","x","x","x","x","x","x","x","-"],
    ["Honeybee",                   200,"Flying",                            "8 AM - 5 PM",              "-","-","x","x","x","x","x","-","-","-","-","-"],
    ["Wasp",                      2500,"Shaking Trees",                     "All day",                  "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Brown cicada",               250,"On Trees",                          "8 AM - 5 PM",              "-","-","-","-","-","-","x","x","-","-","-","-"],
    ["Robust cicada",              300,"On Trees",                          "8 AM - 5 PM",              "-","-","-","-","-","-","x","x","-","-","-","-"],
    ["Giant cicada",               500,"On Trees",                          "8 AM - 5 PM",              "-","-","-","-","-","-","x","x","-","-","-","-"],
    ["Walker cicada",              400,"On Trees",                          "8 AM - 5 PM",              "-","-","-","-","-","-","-","x","x","-","-","-"],
    ["Evening cicada",             550,"On Trees",                          "4 AM - 8 AM & 4 PM - 7 PM","-","-","-","-","-","-","x","x","-","-","-","-"],
    ["Cicada shell",                10,"On Trees",                          "All day",                  "-","-","-","-","-","-","x","x","-","-","-","-"],
    ["Red dragonfly",              180,"Flying",                            "8 AM - 7 PM",              "-","-","-","-","-","-","-","-","x","x","-","-"],
    ["Darner dragonfly",           230,"Flying",                            "8 AM - 5 PM",              "-","-","-","x","x","x","x","x","x","x","-","-"],
    ["Banded dragonfly",          4500,"Flying",                            "8 AM - 5 PM",              "-","-","-","-","x","x","x","x","x","x","-","-"],
    ["Damselfly",                  500,"Flying",                            "All day",                  "x","x","-","-","-","-","-","-","-","-","x","x"],
    ["Firefly",                    300,"Flying",                            "7 PM - 4 AM",              "-","-","-","-","-","x","-","-","-","-","-","-"],
    ["Mole cricket",               500,"Underground",                       "All day",                  "x","x","x","x","x","-","-","-","-","-","x","x"],
    ["Pondskater",                 130,"On Ponds and Rivers",               "8 AM - 7 PM",              "-","-","-","-","x","x","x","x","x","-","-","-"],
    ["Diving beetle",              800,"On Ponds and Rivers",               "8 AM - 7 PM",              "-","-","-","-","x","x","x","x","x","-","-","-"],
    ["Giant water bug",           2000,"On Ponds and Rivers",               "7 PM - 8 AM",              "-","-","-","x","x","x","x","x","x","-","-","-"],
    ["Stinkbug",                   120,"On Flowers",                        "All day",                  "-","-","x","x","x","x","x","x","x","x","-","-"],
    ["Man-faced stink bug",       1000,"On Flowers",                        "7 PM - 8 AM",              "-","-","x","x","x","x","x","x","x","x","-","-"],
    ["Ladybug",                    200,"On Flowers",                        "8 AM - 5 PM",              "-","-","x","x","x","x","-","-","-","x","-","-"],
    ["Tiger beetle",              1500,"On the Ground",                     "All day",                  "-","x","x","x","x","x","x","x","x","x","-","-"],
    ["Jewel beetle",              2400,"On Tree Stumps",                    "All day",                  "-","-","-","x","x","x","x","x","-","-","-","-"],
    ["Violin beetle",              450,"On Tree Stumps",                    "All day",                  "-","-","-","-","x","x","-","-","x","x","x","-"],
    ["Citrus long-horned beetle",  350,"On Tree Stumps",                    "All day",                  "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Rosalia batesi beetle",     3000,"On Tree Stumps",                    "All day",                  "-","-","-","-","x","x","x","x","x","-","-","-"],
    ["Blue weevil beetle",         800,"On Trees (Coconut)",                "All day",                  "-","-","-","-","-","-","x","x","-","-","-","-"],
    ["Dung beetle",               3000,"On the Ground (rolling snowballs)", "All day",                  "x","x","-","-","-","-","-","-","-","-","-","x"],
    ["Earth-boring dung beetle",   300,"On the Ground",                     "All day",                  "-","-","-","-","-","-","x","x","x","-","-","-"],
    ["Scarab beetle",            10000,"On Trees",                          "11 PM - 8 AM",             "-","-","-","-","-","-","x","x","-","-","-","-"],
    ["Drone beetle",               200,"On Trees",                          "All day",                  "-","-","-","-","-","x","x","x","-","-","-","-"],
    ["Goliath beetle",            8000,"On Trees (Coconut)",                "5 PM - 8 AM",              "-","-","-","-","-","x","x","x","x","-","-","-"],
    ["Saw stag",                  2000,"On Trees",                          "All day",                  "-","-","-","-","-","-","x","x","-","-","-","-"],
    ["Miyama stag",               1000,"On Trees",                          "All day",                  "-","-","-","-","-","-","x","x","-","-","-","-"],
    ["Giant stag",               10000,"On Trees",                          "11 PM - 8 AM",             "-","-","-","-","-","-","x","x","-","-","-","-"],
    ["Rainbow stag",              6000,"On Trees",                          "7 PM - 8 AM",              "-","-","-","-","-","x","x","x","x","-","-","-"],
    ["Cyclommatus stag",          8000,"On Trees (Coconut)",                "5 PM - 8 AM",              "-","-","-","-","-","-","x","x","-","-","-","-"],
    ["Golden stag",              12000,"On Trees (Coconut)",                "5 PM - 8 AM",              "-","-","-","-","-","-","x","x","-","-","-","-"],
    ["Giraffe stag",             12000,"On Trees (Coconut)",                "5 PM - 8 AM",              "-","-","-","-","-","-","x","x","-","-","-","-"],
    ["Horned dynastid",           1350,"On Trees",                          "5 PM - 8 AM",              "-","-","-","-","-","-","x","x","-","-","-","-"],
    ["Horned atlas",              8000,"On Trees (Coconut)",                "5 PM - 8 AM",              "-","-","-","-","-","-","x","x","-","-","-","-"],
    ["Horned elephant",           8000,"On Trees (Coconut)",                "5 PM - 8 AM",              "-","-","-","-","-","-","x","x","-","-","-","-"],
    ["Horned hercules",          12000,"On Trees (Coconut)",                "5 PM - 8 AM",              "-","-","-","-","-","-","x","x","-","-","-","-"],
    ["Walking stick",              600,"On Trees",                          "4 AM - 8 AM & 5 PM - 7 PM","-","-","-","-","-","-","x","x","x","x","x","-"],
    ["Walking leaf",               600,"Under Trees Disguised as Leaves",   "All day",                  "-","-","-","-","-","-","x","x","x","-","-","-"],
    ["Bagworm",                    600,"Shaking Trees",                     "All day",                  "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Ant",                         80,"On rotten food",                    "All day",                  "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Hermit crab",               1000,"Beach disguised as Shells",         "7 PM - 8 AM",              "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Wharf roach",                200,"On Beach Rocks",                    "All day",                  "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Fly",                         60,"On Trash Items",                    "All day",                  "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Mosquito",                   130,"Flying",                            "5 PM - 4 AM",              "-","-","-","-","-","x","x","x","x","-","-","-"],
    ["Flea",                        70,"Villager's Heads",                  "All day",                  "-","-","-","x","x","x","x","x","x","x","x","-"],
    ["Snail",                      250,"On Rocks and Bushes (Rain)",        "All day",                  "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Pill bug",                   250,"Hitting Rocks",                     "11 PM - 4 PM",             "x","x","x","x","x","x","-","-","x","x","x","x"],
    ["Centipede",                  300,"Hitting Rocks",                     "4 PM - 11 PM",             "x","x","x","x","x","x","-","-","x","x","x","x"],
    ["Spider",                     600,"Shaking Trees",                     "7 PM - 8 AM",              "x","x","x","x","x","x","x","x","x","x","x","x"],
    ["Tarantula",                 8000,"On the Ground",                     "7 PM - 4 AM",              "x","x","x","x","-","-","-","-","-","-","x","x"],
    ["Scorpion",                  8000,"On the Ground",                     "7 PM - 4 AM",              "-","-","-","-","x","x","x","x","x","x","-","-"],
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
    ['Seaweed',               600,'Large', 'Stationary','All day',              'x','x','x','x','x','x','x','-','-','x','x','x'],
    ['Sea grapes',            900,'Small', 'Stationary','All day',              '-','-','-','-','-','x','x','x','x','-','-','-'],
    ['Sea cucumber',          500,'Medium','Very slow', 'All day',              'x','x','x','x','-','-','-','-','-','-','x','x'],
    ['Sea pig',             10000,'Small', 'Very fast', '4pm - 9am',            'x','x','-','-','-','-','-','-','-','-','x','x'],
    ['Sea star',              500,'Small', 'Very slow', 'All day',              'x','x','x','x','x','x','x','x','x','x','x','x'],
    ['Sea urchin',           1700,'Small', 'Slow',      'All day',              '-','-','-','-','x','x','x','x','x','-','-','-'],
    ['Slate pencil urchin',  2000,'Medium','Medium',    '4pm - 9am',            '-','-','-','-','x','x','x','x','x','-','-','-'],
    ['Sea anemone',           500,'Large', 'Stationary','All day',              'x','x','x','x','x','x','x','x','x','x','x','x'],
    ['Moon jellyfish',        600,'Small', 'Very slow', 'All day',              '-','-','-','-','-','-','x','x','x','-','-','-'],
    ['Sea slug',              600,'Tiny',  'Very slow', 'All day',              'x','x','x','x','x','x','x','x','x','x','x','x'],
    ['Pearl oyster',         2800,'Small', 'Medium',    'All day',              'x','x','x','x','x','x','x','x','x','x','x','x'],
    ['Mussel',               1500,'Small', 'Slow',      'All day',              '-','-','-','-','-','x','x','x','x','x','x','x'],
    ['Oyster',               1100,'Small', 'Slow',      'All day',              'x','x','-','-','-','-','-','-','x','x','x','x'],
    ['Scallop',              1200,'Medium','Slow',      'All day',              'x','x','x','x','x','x','x','x','x','x','x','x'],
    ['Whelk',                1000,'Small', 'Slow',      'All day',              'x','x','x','x','x','x','x','x','x','x','x','x'],
    ['Turban shell',         1000,'Small', 'Slow',      'All day',              '-','-','x','x','x','-','-','-','x','x','x','x'],
    ['Abalone',              2000,'Medium','Medium',    '4pm - 9am',            'x','-','-','-','-','x','x','x','x','x','x','x'],
    ['Gigas giant clam',    15000,'Huge',  'Very fast', 'All day',              '-','-','-','-','x','x','x','x','x','-','-','-'],
    ['Chambered nautilus',   1800,'Medium','Medium',    '4pm - 9am',            '-','-','x','x','x','x','-','-','x','x','x','-'],
    ['Octopus',              1200,'Medium','Slow',      'All day',              'x','x','x','x','x','x','x','x','x','x','x','x'],
    ['Umbrella octopus',     6000,'Small', 'Fast',      'All day',              '-','-','x','x','x','-','-','-','x','x','x','-'],
    ['Vampire squid',       10000,'Medium','Very fast', '4pm - 9am',            '-','-','-','-','x','x','x','x','-','-','-','-'],
    ['Firefly squid',        1400,'Tiny',  'Slow',      '9pm - 4am',            '-','-','x','x','x','x','-','-','-','-','-','-'],
    ['Gazami crab',          2200,'Medium','Medium',    'All day',              '-','-','-','-','-','x','x','x','x','x','x','-'],
    ['Dungeness crab',       1900,'Medium','Medium',    'All day',              'x','x','x','x','x','-','-','-','-','-','x','x'],
    ['Snow crab',            6000,'Large', 'Fast',      'All day',              'x','x','x','x','-','-','-','-','-','-','x','x'],
    ['Red king crab',        8000,'Large', 'Very fast', 'All day',              'x','x','x','-','-','-','-','-','-','-','x','x'],
    ['Acorn barnacle',        600,'Tiny',  'Stationary','All day',              'x','x','x','x','x','x','x','x','x','x','x','x'],
    ['Spider crab',         12000,'Huge',  'Very fast', 'All day',              '-','-','x','x','-','-','-','-','-','-','-','-'],
    ['Tiger prawn',          3000,'Small', 'Medium',    '4pm - 9am',            '-','-','-','-','-','x','x','x','x','-','-','-'],
    ['Sweet shrimp',         1400,'Small', 'Slow',      '4pm - 9am',            'x','x','-','-','-','-','-','-','x','x','x','x'],
    ['Mantis shrimp',        2500,'Small', 'Medium',    '4pm - 9am',            'x','x','x','x','x','x','x','x','x','x','x','x'],
    ['Spiny lobster',        5000,'Large', 'Fast',      '9pm - 4am',            '-','-','-','-','-','-','-','-','-','x','x','x'],
    ['Lobster',              4500,'Large', 'Fast',      'All day',              'x','-','-','x','x','x','-','-','-','-','-','x'],
    ['Giant isopod',        12000,'Medium','Very fast', '9am - 4pm & 9pm - 4am','-','-','-','-','-','-','x','x','x','x','-','-'],
    ['Horseshoe Crab',       2500,'Medium','Medium',    '9pm - 4am',            '-','-','-','-','-','-','x','x','x','-','-','-'],
    ['Sea pineapple',        1500,'Small', 'Slow',      'All day',              '-','-','-','x','x','x','x','x','-','-','-','-'],
    ['Spotted garden eel',   1100,'Small', 'Slow',      '4am - 9pm',            '-','-','-','-','x','x','x','x','x','x','-','-'],
    ['Flatworm',              700,'Tiny',  'Very slow', '4pm - 9am',            '-','-','-','-','-','-','-','x','x','-','-','-'],
    ['Venus flower basket',  5000,'Medium','Fast',      'All day',              'x','x','-','-','-','-','-','-','-','x','x','x']
]

conn = sqlite3.connect("acnh.sqlite")
cur = conn.cursor()
conn.execute('CREATE TABLE fish          (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT, price INTEGER,    location TEXT, shadow TEXT, start_time1 INTEGER NULL, end_time1 INTEGER NULL, start_time2 INTEGER NULL, end_time2 INTEGER NULL, caught BOOL, donated BOOL)')
conn.execute('CREATE TABLE bugs          (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT, price INTEGER,    location TEXT,              start_time1 INTEGER NULL, end_time1 INTEGER NULL, start_time2 INTEGER NULL, end_time2 INTEGER NULL, caught BOOL, donated BOOL)')
conn.execute('CREATE TABLE sea_creatures (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT, price INTEGER, shadow_size INTEGER,  speed TEXT, start_time1 INTEGER NULL, end_time1 INTEGER NULL, start_time2 INTEGER NULL, end_time2 INTEGER NULL, caught BOOL, donated BOOL)')
conn.execute('CREATE TABLE months        (table_name TEXT, id INTEGER, month_mask INTEGER)')
INSERT_FISH =      'INSERT INTO fish          (name, price, location,   shadow, start_time1, end_time1, start_time2, end_time2, caught, donated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
INSERT_BUGS =      'INSERT INTO bugs          (name, price, location,           start_time1, end_time1, start_time2, end_time2, caught, donated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
INSERT_CREATURES = 'INSERT INTO sea_creatures (name, price, shadow_size, speed, start_time1, end_time1, start_time2, end_time2, caught, donated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
def times(val):
    if val == 'All day':
        return [None, None, None, None]
    if '&' in val:
        parts = val.split('&')
        return time_pair(parts[0]) + time_pair(parts[1])
    else:
        return time_pair(val) + [None, None]


def time_pair(val):
    parts = val.split(' - ')
    return [time_part(parts[0]), time_part(parts[1])]

def time_part(val):
    n = int(val.strip()[0])
    if 'PM' in val:
        n += 12
    return n

ACTIVITIES = [
    ('fish',          4,      FISH,      INSERT_FISH),
    ('bugs',          3,      BUGS,      INSERT_BUGS),
    ('sea_creatures', 4, CREATURES, INSERT_CREATURES),
]

for (table, time_idx, rows, insert) in ACTIVITIES:
    print(f'inserting into {table}')
    
    for row in rows:
        params = row[:time_idx]
        t = times(row[time_idx])
        params.append(t[0])
        params.append(t[1])
        params.append(t[2])
        params.append(t[3])
        params.append(False)
        params.append(False)
        l = len(row)
        
        month_mask = 0
        for (i, check) in enumerate(row[-12:]):
            idx = time_idx + 4 + i
            if check == 'x':
                month_mask |= MONTHS[i]
        values = ','.join('?' * len(params))
        print(params)
        cur.execute(insert, params)
        cur.execute(f'INSERT INTO months VALUES (?1, ?2, ?3)', [table, cur.lastrowid, month_mask])

conn.commit()
conn.close()