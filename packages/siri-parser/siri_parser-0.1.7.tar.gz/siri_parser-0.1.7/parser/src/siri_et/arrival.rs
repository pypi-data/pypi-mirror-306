use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::enums::arrival_status::ArrivalStatus;

#[derive(Debug, Default, Clone, Serialize, Deserialize, PartialEq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct Arrival {
    aimed_arrival_time: Option<String>,          // dateTime
    expected_arrival_time: Option<String>,       // dateTime
    arrival_status: Option<ArrivalStatus>,       // onTime, missed, delayed, etc.
    arrival_proximity_text: Option<Vec<String>>, // NLString
    arrival_platform_name: Option<String>,       // NLString
    arrival_stop_assignment: Option<String>,     // structure
    aimed_quay_name: Option<String>,             // NLString
}
