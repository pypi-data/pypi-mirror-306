use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use super::distributor_connection_link::DistributorConnectionLink;



#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct TargetedInterchange {
    pub interchange_code: String,
    pub distributor_vehicle_journey_ref: String,
    pub distributor_connection_link: DistributorConnectionLink,
    pub stay_seated: Option<bool>,
    pub guaranteed: Option<bool>,
    pub maximum_wait_time: Option<String>,
}