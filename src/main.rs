use warp::{body::json, fs::dir, get, log, path, post, Filter};
mod data;

mod status {
    use warp::http::StatusCode;
    pub const OK: StatusCode = StatusCode::OK;
    pub const INTERNAL_SERVER_ERROR: StatusCode = StatusCode::INTERNAL_SERVER_ERROR;
    pub const NOT_FOUND: StatusCode = StatusCode::NOT_FOUND;
}
#[tokio::main]
async fn main() {
    pretty_env_logger::init();
    let fish_list = get().and(path("fish")).and_then(|| async {
        match data::get_fish().await {
            Ok(fish) => reply_with_status(Response::Fish(fish)),
            Err(e) => reply_with_status(Response::Error(format!("Unable to get fish: {}", e))),
        }
    });
    let bug_list = get().and(path("bugs")).and_then(|| async {
        match data::get_bugs().await {
            Ok(bugs) => reply_with_status(Response::Bugs(bugs)),
            Err(e) => reply_with_status(Response::Error(format!("Unable to get fish: {}", e))),
        }
    });
    let sea_creature_list = get().and(path("sea_creatures")).and_then(|| async {
        match data::get_sea_creatures().await {
            Ok(creatures) => reply_with_status(Response::SeaCreatures(creatures)),
            Err(e) => reply_with_status(Response::Error(format!(
                "Unable to get sea creatures: {}",
                e
            ))),
        }
    });
    let update_fish = post()
        .and(warp::path!("update" / "fish"))
        .and(json())
        .and_then(|f: data::Fish| async {
            match data::update_fish(f).await {
                Ok(_) => reply_with_status(Response::FishUpdated),
                Err(e) => reply_with_status(Response::Error(format!("Error updating fish: {}", e))),
            }
        });
    let update_bug = post()
        .and(warp::path!("update" / "bug"))
        .and(json())
        .and_then(|b: data::Bug| async {
            match data::update_bug(b).await {
                Ok(_) => reply_with_status(Response::BugUpdated),
                Err(e) => reply_with_status(Response::Error(format!("Error updating bug: {}", e))),
            }
        });
    let update_sea_creatures = post()
        .and(warp::path!("update" / "sea_creature"))
        .and(json())
        .and_then(|s: data::SeaCreature| async {
            match data::update_creature(s).await {
                Ok(_) => reply_with_status(Response::SeaCreatureUpdated),
                Err(e) => reply_with_status(Response::Error(format!(
                    "Error updating sea creature: {}",
                    e
                ))),
            }
        });
    let available = get()
        .and(path!("available" / u32 / u32))
        .and_then(|hour, month| async move {
            match data::available_for(hour, month).await {
                Ok(b) => reply_with_status(Response::AvailableFor(b)),
                Err(e) => {
                    reply_with_status(Response::Error(format!("Error getting available: {}", e)))
                }
            }
        });
    let catch_all = warp::any().and_then(|| async { reply_with_status(Response::NotFound) });
    let p = std::env::var("ACNH_DIR").unwrap_or_else(|_| "public".to_string());
    let routes = dir(p)
        .or(fish_list)
        .or(bug_list)
        .or(sea_creature_list)
        .or(available)
        .or(update_fish)
        .or(update_bug)
        .or(update_sea_creatures)
        .or(catch_all);
    let port = std::env::var("ACHN_PORT")
        .map(|v| v.parse().unwrap_or(8907))
        .unwrap_or(8907);
    warp::serve(routes.with(log("acnh_util")))
        .run(([0, 0, 0, 0], port))
        .await;
}

fn reply_with_status(body: Response) -> Result<impl warp::Reply, std::convert::Infallible> {
    let inner = warp::reply::json(&body);
    let status = match &body {
        Response::Error(_) => status::INTERNAL_SERVER_ERROR,
        Response::NotFound => status::NOT_FOUND,
        _ => status::OK,
    };
    Ok(warp::reply::with_status(inner, status))
}

#[derive(serde::Serialize, Debug)]
pub enum Response {
    Fish(Vec<data::Fish>),
    Bugs(Vec<data::Bug>),
    SeaCreatures(Vec<data::SeaCreature>),
    AvailableFor(data::Available),
    FishUpdated,
    BugUpdated,
    SeaCreatureUpdated,
    Error(String),
    NotFound,
}
