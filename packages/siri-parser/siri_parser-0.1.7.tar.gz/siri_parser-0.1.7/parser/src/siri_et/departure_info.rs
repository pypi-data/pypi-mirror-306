use crate::enums::{boarding_activity::BoardingActivity, departure_status::DepartureStatus};
use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct DepartureInfo {
    pub aimed_departure_time: Option<String>, // Consider using a proper DateTime type
    pub actual_departure_time: Option<String>,
    pub expected_departure_time: Option<String>,
    pub departure_status: Option<DepartureStatus>,
    pub departure_platform_name: Option<String>,
    pub departure_boarding_activity: Option<BoardingActivity>,
    pub expected_quay_ref: Option<String>,
}
