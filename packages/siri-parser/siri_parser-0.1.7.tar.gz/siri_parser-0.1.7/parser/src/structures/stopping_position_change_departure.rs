use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::siri_sm::location_structure::LocationStructure;

use super::distribuor_info::DistributorInfo;



#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct StoppingPositionChangeDeparture {
    pub recorded_at_time: String,
    pub distributor_info: Option<DistributorInfo>,
    pub change_note: Option<String>,
    pub new_location: Option<LocationStructure>
}
