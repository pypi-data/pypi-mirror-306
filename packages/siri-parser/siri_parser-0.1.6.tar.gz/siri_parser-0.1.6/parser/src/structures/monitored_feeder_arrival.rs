use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use super::feeder_journey::FeederJourney;

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct MonitoredFeederArrival {
    pub recorded_at_time: String,
    pub item_identifier: Option<String>,
    pub interchange_ref: Option<String>,
    pub connection_link_ref: Option<String>,
    pub stop_point_ref: Option<String>,
    pub order: Option<u32>,
    pub strop_point_name: Option<String>,
    pub clear_down_ref: Option<String>,
    pub feeder_journey: FeederJourney,
    pub vehicle_at_stop: Option<bool>,
    pub aimed_arrival_time: Option<String>,
    pub expected_arrival_time: Option<String>,
    pub arrival_platform_time: Option<String>,
    pub number_of_transfer_passengers: Option<u32>,
}