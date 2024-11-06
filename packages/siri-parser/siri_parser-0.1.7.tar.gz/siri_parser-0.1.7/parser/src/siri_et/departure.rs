use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::enums::{boarding_activity::BoardingActivity, departure_status::DepartureStatus};

#[derive(Debug, Default, Clone, Serialize, Deserialize, PartialEq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct Departure {
    aimed_departure_time: Option<String>,      // dateTime
    expected_departure_time: Option<String>,   // dateTime
    departure_status: Option<DepartureStatus>, // onTime, early, delayed, etc.
    departure_platform_name: Option<String>,   // NLString
    departure_boarding_activity: Option<BoardingActivity>, // boarding, noBoarding, etc.
}
