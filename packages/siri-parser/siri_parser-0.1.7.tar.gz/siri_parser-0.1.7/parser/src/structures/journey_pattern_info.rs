use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};



#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct JourneyPatternInfo {
    pub journey_pattern_ref: Option<String>,
    pub journey_pattern_name: Option<String>,
    pub vehicle_mode: Option<String>,
    pub route_ref: Option<String>,
    pub published_line_name: String,
    pub direction_name: Option<String>,
}