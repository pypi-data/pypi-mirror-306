use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use super::journey_info::JourneyInfo;

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct MonitoredFeederArrivalCancellation{
    pub recorded_at_time: String,
    pub item_ref: Option<String>,
    pub interchange_ref: Option<String>,
    pub connection_link_ref: Option<String>,
    pub stop_point_ref: Option<String>,
    pub order: Option<u32>,
    pub strop_point_name: Option<String>,
    //#[serde(flatten)]
    pub journey_info: Option<JourneyInfo>,
    pub reason: Option<String>
}