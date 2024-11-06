use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};



#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct AffectedVehicleJourney {
    vehicle_journey_ref: String,
}