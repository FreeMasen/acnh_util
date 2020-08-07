curl http://localhost:8080/1/fish | jq '{"Fish": .Fish }' > fish.json \
&& curl http://localhost:8080/1/bugs | jq '{"Bugs": .Bugs}' > bugs.json \
&& curl http://localhost:8080/1/sea_creatures | jq '{"SeaCreatures": .SeaCreatures}' > sea_creatures.json \
&& curl http://localhost:8080/1/available/12/6 |  jq '.AvailableFor | {"AvailableFor": { "fish": .fish[0:3], "bugs": .bugs[0:3], "sea_creatures": .sea_creatures[0:3] } }' > available.json