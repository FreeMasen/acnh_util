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
    "Fish":[
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
            "caught":false,
            "donated":false
        }
    ]
}
```

#### GET /bugs

##### Response Body Example

```json
{
    "Bugs":[
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
    ]
}
```

#### GET /sea_creatures

##### Response Body Example

```json
{
    "SeaCreatures":[
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
    ]
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
