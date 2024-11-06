use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::enums::vehicle_mode::VehicleMode;



#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct JourneyInfo {
    pub line_ref: Option<String>,
    pub direction_ref: Option<String>,
    pub journey_pattern_ref: Option<String>,
    pub journey_pattern_name: Option<String>,
    pub vehicle_mode: Option<VehicleMode>,
    pub route_ref: Option<String>,
    pub published_line_name: Option<String>,
    pub group_of_lines_ref: Option<String>,
    pub direction_name: Option<String>,
    pub reason: Option<String>,
}