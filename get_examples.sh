curl http://localhost:8907/fish | jq '{"Fish": .Fish[0:3] }' > fish.json \
&& curl http://localhost:8907/bugs | jq '{"Bugs": .Bugs[0:3]}' > bugs.json \
&& curl http://localhost:8907/sea_creatures | jq '{"SeaCreatures": .SeaCreatures[0:3]}' > sea_creatures.json \
&& curl http://localhost:8907/available/12/6 |  jq '.AvailableFor | {"AvailableFor": { "fish": .fish[0:3], "bugs": .bugs[0:3], "sea_creatures": .sea_creatures[0:3] } }' > available.json