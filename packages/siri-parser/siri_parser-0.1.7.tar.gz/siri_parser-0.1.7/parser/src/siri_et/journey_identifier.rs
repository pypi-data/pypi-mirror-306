use super::dated_vehicle_journey_indirect_ref::DatedVehicleJourneyIndirectRef;
use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "camelCase")]
pub enum JourneyIdentifier {
    DatedVehicleJourneyRef(String),
    EstimatedVehicleJourneyCode(String),
    DatedVehicleJourneyIndirectRef(DatedVehicleJourneyIndirectRef),
}
