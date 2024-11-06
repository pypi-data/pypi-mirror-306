use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::enums::boarding_activity::BoardingActivity;




#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct Boarding {
    arrival_boarding_activity: Option<BoardingActivity>,
    departure_boarding_activity: Option<BoardingActivity>
}