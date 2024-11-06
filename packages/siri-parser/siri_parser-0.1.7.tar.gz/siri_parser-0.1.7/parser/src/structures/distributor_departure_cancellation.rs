use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use super::distribuor_info::DistributorInfo;



#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct DistributorDepartureCancellation {
    pub recorded_at_time: String,
    pub distributor_info: Option<DistributorInfo>,
    pub reason: Option<String>
}
