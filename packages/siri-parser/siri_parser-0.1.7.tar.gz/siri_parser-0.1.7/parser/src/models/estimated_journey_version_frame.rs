use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use super::estimated_vehicle_journey::EstimatedVehicleJourney;

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct EstimatedJourneyVersionFrame {
    pub recorded_at_time: String,
    pub version_ref: Option<String>,
    pub estimated_vehicle_journey: Vec<EstimatedVehicleJourney>,
}
