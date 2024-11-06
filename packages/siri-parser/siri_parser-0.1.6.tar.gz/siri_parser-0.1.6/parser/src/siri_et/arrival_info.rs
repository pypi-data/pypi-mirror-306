use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::enums::{arrival_status::ArrivalStatus, boarding_activity::BoardingActivity};

use super::stop_assigment::StopAssignment;

#[derive(Debug, Clone,  Serialize, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct ArrivalInfo {
    pub aimed_arrival_time: Option<String>, // Consider using a proper DateTime type
    pub actual_arrival_time: Option<String>,
    pub expected_arrival_time: Option<String>,
    pub arrival_status: Option<ArrivalStatus>,
    pub arrival_proximity_text: Vec<String>,
    pub arrival_platform_name: Option<String>,
    pub arrival_boarding_activity: Option<BoardingActivity>,
    pub arrival_stop_assignment: Option<StopAssignment>,
}
