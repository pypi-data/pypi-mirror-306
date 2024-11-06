use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::enums::boarding_activity::BoardingActivity;

use super::targeted_interchange::TargetedInterchange;



#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct DatedCall {
    pub stop_point_ref: Option<String>,
    pub order: Option<u32>,
    pub stop_point_name: Option<String>,
    pub destination_display: Option<String>,
    pub aimed_arrival_time: Option<String>,
    pub arrival_platform: Option<String>,
    pub aimed_quay_name: Option<String>,
    pub aimed_departure_time: Option<String>,
    pub departure_platform_name: Option<String>,
    pub departure_boarding_activity: Option<BoardingActivity>,
    pub aimed_headway_interval: Option<u32>,
    pub targeted_interchange:  Option<TargetedInterchange>,
}