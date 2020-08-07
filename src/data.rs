use rusqlite::Connection;
use serde::{Deserialize, Serialize};
use std::{str::FromStr, sync::Arc};
use tokio::sync::Mutex;

lazy_static::lazy_static! {

    static ref CONN: Arc<Mutex<Connection>> = Arc::new(Mutex::new(Connection::open(
        std::env::var("ACNH_DATABASE").unwrap_or_else(|_| "acnh.sqlite".to_string())
    ).expect("failed to open sqlite connection")));
}

pub type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

#[derive(Debug)]
pub struct Error(String);

impl std::fmt::Display for Error {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl std::error::Error for Error {}

pub async fn get_fish(user_id: i32) -> Result<Vec<Fish>> {
    let conn = CONN.lock().await;
    let mut stmt = conn.prepare("
    SELECT fish.id, name, price, location, shadow, available_months, available_hours, user_status.caught, user_status.donated
    FROM fish
    JOIN user_status
    ON fish.id = user_status.creature_id
    AND user_status.creature_table = 'fish'
    AND user_status.user_id = ?")?;
    let stmt_res = stmt
        .query_and_then(rusqlite::params![user_id], row_to_fish)
        .map_err(|e| Error(format!("Error querying fish: {}", e)))?;
    stmt_res.collect()
}

pub async fn get_bugs(user_id: i32) -> Result<Vec<Bug>> {
    let conn = CONN.lock().await;
    let mut stmt = conn.prepare("
    SELECT bugs.id, name, location, price, available_months, available_hours, user_status.caught, user_status.donated
    FROM bugs
    JOIN user_status
    ON bugs.id = user_status.creature_id
    AND user_status.creature_table = 'bugs'
    AND user_status.user_id = ?",
    )?;
    let stmt_iter = stmt
        .query_and_then(rusqlite::params![user_id], row_to_bug)
        .map_err(|e| Error(format!("failed to get bugs: {}", e)))?;
    stmt_iter.collect()
}

pub async fn get_sea_creatures(user_id: i32) -> Result<Vec<SeaCreature>> {
    let conn = CONN.lock().await;
    let mut stmt = conn.prepare("
    SELECT sea_creatures.id, name, shadow_size, speed, price, available_months, available_hours, user_status.caught, user_status.donated
    FROM sea_creatures
    JOIN user_status
    ON sea_creatures.id = user_status.creature_id
    AND user_status.creature_table = 'sea_creatures'
    AND user_status.user_id = ?")?;
    let stmt_iter = stmt
        .query_and_then(rusqlite::params![user_id], row_to_sea_creature)
        .map_err(|e| Error(format!("Error querying sea creatures: {}", e)))?;
    stmt_iter.collect()
}

pub async fn get_users() -> Result<Vec<User>> {
    let conn = CONN.lock().await;
    let mut stmt = conn.prepare("SELECT id, name FROM users")?;
    let iter = stmt.query_and_then(rusqlite::params![], |r| {
        Ok(User {
            user_id: r.get("id")?,
            name: r.get("name")?
        })
    })
    .map_err(|e| Error(format!("Error querying sea creatures: {}", e)))?;
    iter.collect()
}

pub async fn update_fish(user_id: i32, id: i32, caught: bool, donated: bool) -> Result<()> {
    let conn = CONN.lock().await;
    {
        let mut stmt = conn.prepare_cached(
            "
        UPDATE user_status 
        set donated = ?2,
        caught = ?3
        WHERE creature_id = ?1
        AND user_id = ?4
        AND creature_table = 'fish'
        ",
        )?;
        stmt.execute(rusqlite::params![id, donated, caught, user_id])?;
    }
    Ok(())
}

pub async fn update_bug(user_id: i32, id: i32, caught: bool, donated: bool) -> Result<()> {
    let conn = CONN.lock().await;
    {
        let mut stmt = conn.prepare_cached(
            "
        UPDATE user_status 
        set donated = ?2,
        caught = ?3
        WHERE creature_id = ?1
        AND user_id = ?4
        AND creature_table = 'bugs'
        ",
        )?;
        stmt.execute(rusqlite::params![id, donated, caught, user_id])?;
    }
    Ok(())
}

pub async fn update_creature(user_id: i32, creature_id: i32, caught: bool, donated: bool) -> Result<()> {
    let conn = CONN.lock().await;
    {
        let mut stmt = conn.prepare_cached(
            "
        UPDATE user_status 
        set donated = ?2,
        caught = ?3
        WHERE creature_id = ?1
        AND user_id = ?4
        AND creature_table = 'sea_creatures'
        ",
        )?;
        stmt.execute(rusqlite::params![
            creature_id,
            donated,
            caught,
            user_id
        ])?;
    }
    Ok(())
}

/// Get a full list of fish, bugs and sea creatures that are
/// available at the current hour in the current month
pub async fn available_for(user_id: i32, hour: u32, month: u32) -> Result<Available> {
    println!("hour: {}, month: {}", hour, month);
    // Typical hours are 0 indexed, our hour mask is 1 indexed so we always
    // need to add 1 (eg midnight == 1, 11pm == 24)
    // let hour = hour + 1;
    let c = CONN.lock().await;
    let fish_stmt = c.prepare("
    SELECT fish.id, name, price, location, shadow, available_months, available_hours, caught, donated
    FROM fish
        JOIN user_status
        ON fish.id = user_status.creature_id
        AND user_status.creature_table = 'fish'
        AND user_status.user_id = ?3
    WHERE available_hours & ?1 > 0
    AND available_months & ?2 > 0
    
    ")?;
    let fish = execute_and_return(hour, month, user_id, fish_stmt, row_to_fish)?;
    let bugs_stmt = c.prepare(
        "
    SELECT bugs.id, name, location, price, available_months, available_hours, caught, donated
    FROM bugs
        JOIN user_status
        ON bugs.id = user_status.creature_id
        AND user_status.creature_table = 'bugs'
        AND user_status.user_id = ?3
    WHERE available_hours & ?1 > 0
    AND available_months & ?2 > 0
    ",
    )?;
    let bugs = execute_and_return(hour, month, user_id, bugs_stmt, row_to_bug)?;
    let sea_stmt = c.prepare("
    SELECT sea_creatures.id, name, shadow_size, speed, price, available_months, available_hours, caught, donated
    FROM sea_creatures
        JOIN user_status
        ON sea_creatures.id = user_status.creature_id
        AND user_status.creature_table = 'sea_creatures'
        AND user_status.user_id = ?3
    WHERE available_hours & ?1 > 0
    AND available_months & ?2 > 0
    ")?;
    let sea_creatures = execute_and_return(hour, month, user_id, sea_stmt, row_to_sea_creature)?;

    Ok(Available {
        fish,
        bugs,
        sea_creatures,
    })
}

fn execute_and_return<T, F>(
    hour: u32,
    month: u32,
    usr_id: i32,
    mut stmt: rusqlite::Statement,
    f: F,
) -> Result<Vec<T>>
where
    F: Fn(&rusqlite::Row) -> Result<T>,
{
    use rusqlite::params;
    let hour = 1 << hour;
    let month = 1 << (month - 1);
    println!("shifted: hour {}, month {}", hour, month);
    let stmt_iter = stmt
        .query_and_then(params![hour, month, usr_id], f)
        .map_err(|e| Error(format!("{}", e)))?;
    stmt_iter.collect()
}

fn row_to_fish(row: &rusqlite::Row) -> Result<Fish> {
    let id = row.get::<_, i32>("id")?;
    let name = row.get::<_, String>("name")?;
    let value = row.get::<_, i32>("price")?;
    let location = row.get::<_, String>("location")?;
    let shadow = row.get::<_, String>("shadow")?;
    let month_mask = row.get::<_, u32>("available_months")?;
    let hour_mask = row.get::<_, u32>("available_hours")?;
    let caught = row.get::<_, bool>("caught")?;
    let donated = row.get::<_, bool>("donated")?;
    let size = FishSize::from_str(&shadow)?;
    let months_active = month_mask.into();
    let hours_active = hour_mask.into();
    Ok(Fish {
        id,
        name,
        value,
        location,
        size,
        months_active,
        hours_active,
        caught,
        donated,
    })
}

fn row_to_bug(row: &rusqlite::Row) -> Result<Bug> {
    Ok(Bug {
        id: row.get("id")?,
        name: row.get("name")?,
        value: row.get("price")?,
        location: row.get("location")?,
        months_active: row.get::<_, u32>("available_months")?.into(),
        hours_active: row.get::<_, u32>("available_hours")?.into(),
        caught: row.get("caught")?,
        donated: row.get("donated")?,
    })
}

fn row_to_sea_creature(row: &rusqlite::Row) -> Result<SeaCreature> {
    let id = row.get::<_, i32>("id")?;
    let name = row.get::<_, String>("name")?;
    let value = row.get::<_, i32>("price")?;
    let shadow_size = row.get::<_, String>("shadow_size")?;
    let speed = row.get::<_, String>("speed")?;
    let month_mask = row.get::<_, u32>("available_months")?;
    let hours_mask = row.get::<_, u32>("available_hours")?;
    let caught = row.get::<_, bool>("caught")?;
    let donated = row.get::<_, bool>("donated")?;
    let speed = CreatureSpeed::from_str(&speed)?;
    let size = ShadowSize::from_str(&shadow_size)?;
    let months_active: MonthsActive = month_mask.into();
    let hours_active = hours_mask.into();
    Ok(SeaCreature {
        id,
        name,
        value,
        size,
        speed,
        months_active,
        hours_active,
        caught,
        donated,
    })
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Fish {
    pub id: i32,
    pub name: String,
    pub value: i32,
    pub location: String,
    pub size: FishSize,
    pub months_active: MonthsActive,
    pub hours_active: HoursActive,
    pub caught: bool,
    pub donated: bool,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct FishSize {
    size: ShadowSize,
    modifier: Option<String>,
}

impl std::string::ToString for FishSize {
    fn to_string(&self) -> String {
        let n: i32 = self.size.into();
        let mut ret = n.to_string();
        if let Some(modifier) = &self.modifier {
            ret.push_str(modifier);
        }
        ret
    }
}

impl std::str::FromStr for FishSize {
    type Err = Error;
    fn from_str(s: &str) -> std::result::Result<Self, Self::Err> {
        use std::convert::TryInto;
        let s = s.trim();
        let size = s
            .chars()
            .next()
            .ok_or_else(|| Error(format!("FishSize must have at least 1 character: {:?}", s)))?
            .try_into()?;
        let modifier = if !s.is_empty() {
            Some(s[1..].to_string())
        } else {
            None
        };
        Ok(Self { size, modifier })
    }
}

#[derive(Debug, Copy, Clone, Serialize, Deserialize)]
#[repr(u8)]
pub enum ShadowSize {
    Small = 1,
    Medium,
    Large,
    ExtraLarge,
    Gargantuan,
    Humongous,
}

impl std::convert::TryFrom<char> for ShadowSize {
    type Error = Error;
    fn try_from(c: char) -> std::result::Result<Self, Error> {
        if !c.is_digit(10) {
            return Err(Error(format!("Shadow size must be a number: {:?}", c)));
        }
        Ok(match c {
            '1' => Self::Small,
            '2' => Self::Medium,
            '3' => Self::Large,
            '4' => Self::ExtraLarge,
            '5' => Self::Gargantuan,
            '6' => Self::Humongous,
            _ => return Err(Error(format!("Shadow size out of range {}", c))),
        })
    }
}

impl std::convert::TryFrom<i32> for ShadowSize {
    type Error = Error;
    fn try_from(c: i32) -> std::result::Result<Self, Error> {
        Ok(match c {
            1 => Self::Small,
            2 => Self::Medium,
            3 => Self::Large,
            4 => Self::ExtraLarge,
            5 => Self::Gargantuan,
            6 => Self::Humongous,
            _ => return Err(Error(format!("Shadow size out of range {}", c))),
        })
    }
}

impl FromStr for ShadowSize {
    type Err = Error;
    fn from_str(s: &str) -> std::result::Result<Self, Self::Err> {
        let inner = match s {
            "Tiny" => ShadowSize::Small,
            "Small" => ShadowSize::Medium,
            "Medium" => ShadowSize::Large,
            "Large" => ShadowSize::ExtraLarge,
            "Huge" => ShadowSize::Gargantuan,
            _ => return Err(Error(format!("Invalid ShadowSize: {}", s))),
        };
        Ok(inner)
    }
}

impl Into<i32> for ShadowSize {
    fn into(self) -> i32 {
        match self {
            Self::Small => 1,
            Self::Medium => 2,
            Self::Large => 3,
            Self::ExtraLarge => 4,
            Self::Gargantuan => 5,
            Self::Humongous => 6,
        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Bug {
    pub id: i32,
    pub name: String,
    pub value: i32,
    pub location: String,
    pub months_active: MonthsActive,
    pub hours_active: HoursActive,
    pub caught: bool,
    pub donated: bool,
}

#[derive(Debug, Copy, Clone, Serialize, Deserialize, PartialEq)]
pub struct MonthsActive(pub [bool; 12]);
#[derive(Debug, Copy, Clone, Serialize, Deserialize, PartialEq)]
pub struct HoursActive(pub [bool; 24]);

impl std::ops::Deref for MonthsActive {
    type Target = [bool];
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}
impl std::ops::Deref for HoursActive {
    type Target = [bool];
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl std::convert::TryFrom<&[bool]> for MonthsActive {
    type Error = Error;
    fn try_from(value: &[bool]) -> std::result::Result<Self, Self::Error> {
        if !value.len() == 12 {
            return Err(Error(format!(
                "slice must be exactly 12 elements to be converted into MonthsActive: {:?} ({})",
                value,
                value.len()
            )));
        }
        let mut inner = [false; 12];
        for (&value, dest) in value.iter().zip(inner.iter_mut()) {
            *dest = value;
        }
        Ok(MonthsActive(inner))
    }
}

impl From<u32> for MonthsActive {
    fn from(other: u32) -> Self {
        Self([
            other & 1 > 0,
            other & 1 << 1 > 0,
            other & 1 << 2 > 0,
            other & 1 << 3 > 0,
            other & 1 << 4 > 0,
            other & 1 << 5 > 0,
            other & 1 << 6 > 0,
            other & 1 << 7 > 0,
            other & 1 << 8 > 0,
            other & 1 << 9 > 0,
            other & 1 << 10 > 0,
            other & 1 << 11 > 0,
        ])
    }
}
impl From<u32> for HoursActive {
    fn from(other: u32) -> Self {
        Self([
            other & 1 > 0,
            other & 1 << 1 > 0,
            other & 1 << 2 > 0,
            other & 1 << 3 > 0,
            other & 1 << 4 > 0,
            other & 1 << 5 > 0,
            other & 1 << 6 > 0,
            other & 1 << 7 > 0,
            other & 1 << 8 > 0,
            other & 1 << 9 > 0,
            other & 1 << 10 > 0,
            other & 1 << 11 > 0,
            other & 1 << 12 > 0,
            other & 1 << 13 > 0,
            other & 1 << 14 > 0,
            other & 1 << 15 > 0,
            other & 1 << 16 > 0,
            other & 1 << 17 > 0,
            other & 1 << 18 > 0,
            other & 1 << 19 > 0,
            other & 1 << 20 > 0,
            other & 1 << 21 > 0,
            other & 1 << 22 > 0,
            other & 1 << 23 > 0,
        ])
    }
}

impl From<[bool; 12]> for MonthsActive {
    fn from(other: [bool; 12]) -> Self {
        Self(other)
    }
}

impl Into<[bool; 12]> for MonthsActive {
    fn into(self) -> [bool; 12] {
        self.0
    }
}

impl Into<u32> for MonthsActive {
    fn into(self) -> u32 {
        let mut ret = 0;
        for (i, &b) in self.0.iter().enumerate() {
            if b {
                ret |= 1 << i;
            }
        }
        ret
    }
}
impl Into<u32> for HoursActive {
    fn into(self) -> u32 {
        let mut ret = 0;
        for (i, &b) in self.0.iter().enumerate() {
            if b {
                ret |= 1 << i;
            }
        }
        ret
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SeaCreature {
    pub id: i32,
    pub name: String,
    pub value: i32,
    pub size: ShadowSize,
    pub speed: CreatureSpeed,
    pub months_active: MonthsActive,
    pub hours_active: HoursActive,
    pub caught: bool,
    pub donated: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum CreatureSpeed {
    Stationary,
    VerySlow,
    Slow,
    Medium,
    Fast,
    VeryFast,
}

impl FromStr for CreatureSpeed {
    type Err = Error;
    fn from_str(s: &str) -> std::result::Result<Self, Self::Err> {
        let inner = match s {
            "Stationary" => CreatureSpeed::Stationary,
            "Very slow" => CreatureSpeed::VerySlow,
            "Slow" => CreatureSpeed::Slow,
            "Medium" => CreatureSpeed::Medium,
            "Fast" => CreatureSpeed::Fast,
            "Very fast" => CreatureSpeed::VeryFast,
            _ => return Err(Error(format!("Unknown Creature Size: {:?}", s))),
        };
        Ok(inner)
    }
}

#[derive(Debug, Serialize)]
pub struct Available {
    fish: Vec<Fish>,
    bugs: Vec<Bug>,
    sea_creatures: Vec<SeaCreature>,
}
#[cfg(test)]
mod test {
    use super::*;
    #[test]
    fn round_trip_all_months() {
        run_test(
            1 | 1 << 1
                | 1 << 2
                | 1 << 3
                | 1 << 4
                | 1 << 5
                | 1 << 6
                | 1 << 7
                | 1 << 8
                | 1 << 9
                | 1 << 10
                | 1 << 11,
            MonthsActive([true; 12]),
        );
    }
    #[test]
    fn round_trip_6_months() {
        run_test(
            1 | 1 << 1 | 1 << 2 | 1 << 9 | 1 << 10 | 1 << 11,
            MonthsActive([
                true, true, true, false, false, false, false, false, false, true, true, true,
            ]),
        );
    }

    #[test]
    fn all_hours() {
        run_test(
            (0..24).fold(0, |acc, v| acc | 1 << v),
            HoursActive([true; 24]),
        )
    }

    #[test]
    fn all_even_hours() {
        let mut t = 0;
        let mut a = [false; 24];
        for (i, v) in a.iter_mut().enumerate() {
            if i % 2 == 0 {
                t |= 1 << i;
                *v = true;
            }
        }
        run_test(t, HoursActive(a));
    }

    #[test]
    fn all_odd_hours() {
        let mut t = 0;
        let mut a = [false; 24];
        for (i, v) in a.iter_mut().enumerate() {
            if i % 2 != 0 {
                t |= 1 << i;
                *v = true;
            }
        }
        run_test(t, HoursActive(a));
    }

    #[test]
    fn nine_am_to_four_pm() {
        let mut t = 0;
        let mut a = [false; 24];
        for (i, v) in a[9..12 + 4].iter_mut().enumerate() {
            t |= 1 << (i + 9);
            *v = true
        }
        run_test(t, HoursActive(a));
    }
    #[test]
    fn four_pm_to_nine_am() {
        let mut t = 0;
        let mut a = [false; 24];
        for (i, v) in a[0..9].iter_mut().enumerate() {
            t |= 1 << i;
            *v = true;
        }
        for (i, v) in a[12 + 4..12 + 12].iter_mut().enumerate() {
            t |= 1 << (i + 12 + 4);
            *v = true;
        }
        run_test(t, HoursActive(a));
    }

    fn run_test<T>(target: u32, t: T)
    where
        T: Into<u32> + From<u32> + PartialEq + std::fmt::Debug + Copy,
    {
        let as_int: u32 = t.into();
        assert_eq!(as_int, target);
        let revert: T = as_int.into();
        assert_eq!(revert, t)
    }
}

#[derive(Serialize, Debug)]
pub struct User {
    pub user_id: i32,
    pub name: String,
}
