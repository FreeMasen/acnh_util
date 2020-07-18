use std::{sync::Arc, str::FromStr};
use tokio::sync::Mutex;
use serde::{Serialize, Deserialize};
use rusqlite::Connection;

lazy_static::lazy_static! {
    static ref CONN: Arc<Mutex<Connection>> = Arc::new(Mutex::new(Connection::open("acnh.sqlite").expect("failed to open sqlite connection")));
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

pub async fn get_fish() -> Result<Vec<Fish>> {
    let conn = CONN.lock().await;
    let mut stmt = conn.prepare("
    SELECT fish.id, name, price, location, shadow, months.month_mask, caught, donated
    FROM fish
      JOIN months 
        ON months.id = fish.id
        AND months.table_name = 'fish'
    ")?;
    let query_res = stmt.query_map(rusqlite::params![], |row| {
        Ok(
            (
                row.get::<_, i32>("id")?,
                row.get::<_, String>("name")?,
                row.get::<_, i32>("price")?,
                row.get::<_, String>("location")?,
                row.get::<_, String>("shadow")?,
                row.get::<_, i32>("month_mask")?,
                row.get::<_, bool>("caught")?,
                row.get::<_, bool>("donated")?,
            )
        )
    }).map_err(|e| Error(format!("Error querying fish: {}", e)))?;
    query_res.map(|r| {
        let row = r.map_err(|e| Error(format!("Error querying fish: {}", e)))?;
        let (id, name, value, location, size_str, months_int, caught, donated) = row;
        let size = FishSize::from_str(&size_str)?;
        let months_active = months_int.into();
        Ok(Fish {
            id,
            name,
            value,
            location,
            size,
            months_active,
            caught,
            donated,
        })
    }).collect()
}

pub async fn get_bugs() -> Result<Vec<Bug>> {
    let conn = CONN.lock().await;
    let mut stmt = conn.prepare("
    SELECT bugs.id, name, location, price, months.month_mask, caught, donated
    FROM bugs
      JOIN months 
        ON months.id = bugs.id
        AND months.table_name = 'bugs'
    ")?;
    let stmt_iter = stmt.query_map(rusqlite::params![], |row| {
        Ok(
            Bug {
                id: row.get("id")?,
                name: row.get("name")?,
                value: row.get("price")?,
                location: row.get("location")?,
                months_active: row.get::<_, i32>("month_mask")?.into(),
                caught: row.get("caught")?,
                donated: row.get("donated")?,
            }
        )
    })?;
    let mut ret = Vec::new();
    for item in stmt_iter {
        let fish = item?;
        ret.push(fish);
    }
    Ok(ret)
}

pub async fn update_fish(fish: Fish) -> Result<()> {
    let conn = CONN.lock().await;
    {
        let mut stmt = conn.prepare_cached("
        UPDATE fish 
        set donated = ?2,
        caught = ?3
        WHERE id = ?1
        ")?;
        stmt.execute(rusqlite::params![fish.id, fish.donated, fish.caught])?;
    }
    Ok(())
}

pub async fn update_bug(bug: Bug) -> Result<()> {
    let conn = CONN.lock().await;
    {
        let mut stmt = conn.prepare_cached("
        UPDATE bugs 
        set bugs.donated = ?2,
        bugs.caught = ?3
        WHERE bugs.id = ?1
        ")?;
        stmt.execute(rusqlite::params![bug.id, bug.donated, bug.caught])?;
    }
    Ok(())
}

pub async fn get_sea_creatures() -> Result<Vec<SeaCreature>> {
    use std::convert::TryInto;
    type PreCreature = (i32, String, i32, String, String, i32, bool, bool);
    let conn = CONN.lock().await;
    let mut stmt = conn.prepare("
    SELECT sea_creatures.id, name, shadow_size, speed, price, months.month_mask, caught, donated
    FROM sea_creatures
      JOIN months 
        ON months.id = sea_creatures.id
        AND months.table_name = 'sea_creatures'
    ")?;
    let stmt_iter = stmt.query_map(rusqlite::params![], |row| {
        Ok(
            (
                row.get::<_, i32>("id")?,
                row.get::<_, String>("name")?,
                row.get::<_, i32>("price")?,
                row.get::<_, String>("shadow_size")?,
                row.get::<_, String>("speed")?,
                row.get::<_, i32>("month_mask")?,
                row.get::<_, bool>("caught")?,
                row.get::<_, bool>("donated")?,
            )
        )
    }).map_err(|e| Error(format!("Error querying sea creatures: {}", e)))?;
    stmt_iter.map(|r: std::result::Result<PreCreature, _>| {
        let row = r.map_err(|e| Error(format!("Error querying fish: {}", e)))?;
        let (id, name, value, size_str, speed_str, months_int, caught, donated) = row;
        let speed = CreatureSpeed::from_str(&speed_str)?;
        let size = ShadowSize::from_str(&size_str)?;
        let months_active: MonthsActive = months_int.try_into()?;
        Ok(SeaCreature {
            id,
            name,
            value,
            size,
            speed,
            months_active,
            caught,
            donated,
        })
    })
    .collect()
}

pub async fn update_creature(creature: SeaCreature) -> Result<()> {
    let conn = CONN.lock().await;
    {
        let mut stmt = conn.prepare_cached("
        UPDATE sea_creatures 
        set donated = ?2,
        caught = ?3
        WHERE id = ?1
        ")?;
        stmt.execute(rusqlite::params![creature.id, creature.donated, creature.caught])?;
    }
    Ok(())
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Fish {
    pub id: i32,
    pub name: String,
    pub value: i32,
    pub location: String,
    pub size: FishSize,
    pub months_active: MonthsActive,
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
            .ok_or_else(|| Error(format!("FishSize must have at least 1 character")))?
            .try_into()?;
        let modifier = if s.len() > 0 {
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
            _ => return Err(Error(format!("Invalid ShadowSize: {}", s)))
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
    pub caught: bool,
    pub donated: bool,
}

#[derive(Debug, Copy, Clone, Serialize, Deserialize)]
pub struct MonthsActive(pub [bool; 12]);

impl std::ops::Deref for MonthsActive {
    type Target = [bool];
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl std::convert::TryFrom<&[bool]> for MonthsActive {
    type Error = Error;
    fn try_from(value: &[bool]) -> std::result::Result<Self, Self::Error> {
        if !value.len() == 12 {
            return Err(Error(format!("slice must be exactly 12 elements to be converted into MonthsActive: {:?} ({})", value, value.len())));
        }
        let mut inner = [false;12];
        for (&value, dest) in value.iter().zip(inner.iter_mut()) {
            *dest = value;
        }
        Ok(MonthsActive(inner))
    }
}

impl From<i32> for MonthsActive {
    fn from(other: i32) -> Self {
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

impl Into<i32> for MonthsActive {
    fn into(self) -> i32 {
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

#[cfg(test)]
mod test {
    use super::*;
    #[test]
    fn round_trip_all_months() {
        test_months(
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
    fn rount_trip_6_months() {
        test_months(
            1 | 1 << 1 | 1 << 2 | 1 << 9 | 1 << 10 | 1 << 11,
            MonthsActive([
                true, true, true, false, false, false, false, false, false, true, true, true,
            ]),
        );
    }

    fn test_months(target: i32, months: MonthsActive) {
        let as_int: i32 = months.into();
        assert_eq!(as_int, target);
        let revert: MonthsActive = as_int.into();
        assert_eq!(revert.0, months.0,);
    }
}
