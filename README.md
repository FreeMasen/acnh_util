# Animal Crossing New Horizon

## Contributing

### Seeding the database

You should be able to seed the database by running the following.

```sh$
python3 ./seed.py
```

### Building

To run the server, you will need to have the rust tool chain installed
you can get that setup by running the following on a unix like system.

```sh$
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

For windows, it would require visiting https://rustup.rs

Once that is complete, you can run the server with the following in the project directory.

```sh$
cargo run
```

The server will be listening on http://0.0.0.0:8907

### Endpoints

#### GET /fish

##### Response Body Example

```json
{
  "Fish": [
    {
      "id": 1,
      "name": "Bitterling",
      "value": 900,
      "location": "River",
      "size": {
        "size": "Small",
        "modifier": ""
      },
      "months_active": [
        true,
        true,
        true,
        false,
        false,
        false,
        false,
        false,
        false,
        false,
        true,
        true
      ],
      "hours_active": [
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true
      ],
      "caught": false,
      "donated": false
    },
    {
      "id": 2,
      "name": "Pale chub",
      "value": 200,
      "location": "River",
      "size": {
        "size": "Small",
        "modifier": ""
      },
      "months_active": [
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true
      ],
      "hours_active": [
        false,
        false,
        false,
        false,
        false,
        false,
        false,
        false,
        false,
        false,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        false,
        false,
        false,
        false,
        false,
        false,
        false
      ],
      "caught": false,
      "donated": false
    },
    {
      "id": 3,
      "name": "Crucian carp",
      "value": 160,
      "location": "River",
      "size": {
        "size": "Medium",
        "modifier": ""
      },
      "months_active": [
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true
      ],
      "hours_active": [
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true
      ],
      "caught": false,
      "donated": false
    }
  ]
}
```

#### GET /bugs

##### Response Body Example

```json
{
  "Bugs": [
    {
      "id": 1,
      "name": "Common butterfly",
      "value": 160,
      "location": "Flying",
      "months_active": [
        true,
        true,
        true,
        true,
        true,
        true,
        false,
        false,
        true,
        true,
        true,
        true
      ],
      "hours_active": [
        false,
        false,
        false,
        false,
        false,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        false,
        false,
        false,
        false
      ],
      "caught": false,
      "donated": false
    },
    {
      "id": 2,
      "name": "Yellow butterfly",
      "value": 160,
      "location": "Flying",
      "months_active": [
        false,
        false,
        true,
        true,
        true,
        true,
        false,
        false,
        true,
        true,
        false,
        false
      ],
      "hours_active": [
        false,
        false,
        false,
        false,
        false,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        false,
        false,
        false,
        false
      ],
      "caught": false,
      "donated": false
    },
    {
      "id": 3,
      "name": "Tiger butterfly",
      "value": 240,
      "location": "Flying",
      "months_active": [
        false,
        false,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        false,
        false,
        false
      ],
      "hours_active": [
        false,
        false,
        false,
        false,
        false,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        false,
        false,
        false,
        false
      ],
      "caught": false,
      "donated": false
    }
  ]
}
```

#### GET /sea_creatures

##### Response Body Example

```json
{
  "SeaCreatures": [
    {
      "id": 1,
      "name": "Seaweed",
      "value": 600,
      "size": "ExtraLarge",
      "speed": "Stationary",
      "months_active": [
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        false,
        false,
        true,
        true,
        true
      ],
      "hours_active": [
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true
      ],
      "caught": false,
      "donated": false
    },
    {
      "id": 2,
      "name": "Sea grapes",
      "value": 900,
      "size": "Medium",
      "speed": "Stationary",
      "months_active": [
        false,
        false,
        false,
        false,
        false,
        true,
        true,
        true,
        true,
        false,
        false,
        false
      ],
      "hours_active": [
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true
      ],
      "caught": false,
      "donated": false
    },
    {
      "id": 3,
      "name": "Sea cucumber",
      "value": 500,
      "size": "Large",
      "speed": "VerySlow",
      "months_active": [
        true,
        true,
        true,
        true,
        false,
        false,
        false,
        false,
        false,
        false,
        true,
        true
      ],
      "hours_active": [
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true,
        true
      ],
      "caught": false,
      "donated": false
    }
  ]
}
```

#### GET /available/:hour/:month

##### Request Example

```js
let now = new Date();
let hour = now.getHours();
// JS Date::getMonth returns a 0 index month
let month = now.getMonth() + 1;
fetch(`/available/${hour}/${month}`)
    .then(r => r.json())
    .then(available => {
        //...
    })
```

##### Response Body Example

```json
{
  "AvailableFor": {
    "fish": [
      {
        "id": 2,
        "name": "Pale chub",
        "value": 200,
        "location": "River",
        "size": {
          "size": "Small",
          "modifier": ""
        },
        "months_active": [
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true
        ],
        "hours_active": [
          false,
          false,
          false,
          false,
          false,
          false,
          false,
          false,
          false,
          false,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          false,
          false,
          false,
          false,
          false,
          false,
          false
        ],
        "caught": false,
        "donated": false
      },
      {
        "id": 3,
        "name": "Crucian carp",
        "value": 160,
        "location": "River",
        "size": {
          "size": "Medium",
          "modifier": ""
        },
        "months_active": [
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true
        ],
        "hours_active": [
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true
        ],
        "caught": false,
        "donated": false
      },
      {
        "id": 5,
        "name": "Carp",
        "value": 300,
        "location": "Pond",
        "size": {
          "size": "ExtraLarge",
          "modifier": ""
        },
        "months_active": [
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true
        ],
        "hours_active": [
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true
        ],
        "caught": false,
        "donated": false
      }
    ],
    "bugs": [
      {
        "id": 3,
        "name": "Tiger butterfly",
        "value": 240,
        "location": "Flying",
        "months_active": [
          false,
          false,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          false,
          false,
          false
        ],
        "hours_active": [
          false,
          false,
          false,
          false,
          false,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          false,
          false,
          false,
          false
        ],
        "caught": false,
        "donated": false
      },
      {
        "id": 5,
        "name": "Common bluebottle",
        "value": 300,
        "location": "Flying",
        "months_active": [
          false,
          false,
          false,
          true,
          true,
          true,
          true,
          true,
          false,
          false,
          false,
          false
        ],
        "hours_active": [
          false,
          false,
          false,
          false,
          false,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          false,
          false,
          false,
          false
        ],
        "caught": false,
        "donated": false
      },
      {
        "id": 6,
        "name": "Paper kite butterfly",
        "value": 1000,
        "location": "Flying",
        "months_active": [
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true
        ],
        "hours_active": [
          false,
          false,
          false,
          false,
          false,
          false,
          false,
          false,
          false,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          false,
          false,
          false,
          false
        ],
        "caught": false,
        "donated": false
      }
    ],
    "sea_creatures": [
      {
        "id": 1,
        "name": "Seaweed",
        "value": 600,
        "size": "ExtraLarge",
        "speed": "Stationary",
        "months_active": [
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          false,
          false,
          true,
          true,
          true
        ],
        "hours_active": [
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true
        ],
        "caught": false,
        "donated": false
      },
      {
        "id": 2,
        "name": "Sea grapes",
        "value": 900,
        "size": "Medium",
        "speed": "Stationary",
        "months_active": [
          false,
          false,
          false,
          false,
          false,
          true,
          true,
          true,
          true,
          false,
          false,
          false
        ],
        "hours_active": [
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true
        ],
        "caught": false,
        "donated": false
      },
      {
        "id": 5,
        "name": "Sea star",
        "value": 500,
        "size": "Medium",
        "speed": "VerySlow",
        "months_active": [
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true
        ],
        "hours_active": [
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true,
          true
        ],
        "caught": false,
        "donated": false
      }
    ]
  }
}
```

#### POST /update/fish

##### Request Body Example

```json
{
    "id":80,
    "name": "Coelacanth",
    "value":15000,
    "location":"Sea",
    "size": {
        "size":"Humongous",
        "modifier":""
    },
    "months_active":[
        true,true,true,true,true,true,true,true,true,true,true,true
    ],
    "caught":true,
    "donated":false
}
```

#### POST /update/bug

##### Request Body Example

```json
{
    "id":80,
    "name":"Scorpion",
    "value":8000,
    "location":"On the Ground",
    "months_active": [
        false,false,false,false,true,true,true,true,true,true,false,false
    ],
    "caught": false,
    "donated":false
}
```

#### POST /update/sea_creature

##### Request Body Example

```json
{
    "id":39,
    "name":"Flatworm",
    "value":700,
    "size":"Small",
    "speed":"VerySlow",
    "months_active": [
        false,false,false,false,false,false,false,true,true,false,false,false
    ],
    "caught":false,
    "donated":false
}
```
