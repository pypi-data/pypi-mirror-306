use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct FramedVehicleJourneyRef {
    pub data_frame_ref: Option<String>,
    pub dated_vehicle_journey_ref: Option<String>,
}
