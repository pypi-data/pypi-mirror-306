use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::enums::vehicle_mode::VehicleMode;

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct JourneyPatternInfo {
    pub journey_pattern_ref: Option<String>, // Optional identifier for the journey pattern
    pub journey_pattern_name: Option<String>, // Optional name or number of the journey presented to the public
    pub vehicle_mode: Option<VehicleMode>,    // Optional transport mode for the journey
    pub route_ref: Option<String>,            // Optional identifier for the route followed
    pub published_line_name: String,          // Mandatory name of the line
    pub direction_name: Option<String>,
}
