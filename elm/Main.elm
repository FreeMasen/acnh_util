import Html exposing (..)
import Http
import Json.Decode exposing (Decoder, field, string, int, list)
type alias User = 
    { id : Int
    , name : String
    }
type DownloadModel
    = User user
    | Fish fish
    | Bugs bugs
    | SeaCreatures sea_creatures


type Msg 
    = DownloadComplete
    

main = Browser.element 
    {
        init = init
    }


init : () -> (DownloadModel, Cmd Msg)
init = _ =
    (
        Loading
        , Http.get
            { url = "/users"
            , expect Http.expectJson
            }
    )

userDecoder : Decoder String
userDecoder =
    field "" list