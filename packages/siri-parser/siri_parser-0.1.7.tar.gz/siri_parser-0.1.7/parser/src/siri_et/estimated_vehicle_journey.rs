use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use super::{
    calls::Calls, distribution_group::DisruptionGroup, estimated_info::EstimatedInfo,
    journey_end_names::JourneyEndNames, journey_identifier::JourneyIdentifier,
    journey_pattern_info::JourneyPatternInfo, journey_progress_info::JourneyProgressInfo,
    operational_info::OperationalInfo, service_info::ServiceInfo,
    vehicle_journey_info::VehicleJourneyInfo,
};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct EstimatedVehicleJourney {
    pub line_ref: String,
    pub direction_ref: String,
    pub journey_identifier: JourneyIdentifier,
    pub extra_journey: Option<bool>,
    pub cancellation: Option<bool>,
    pub journey_pattern_info: Option<JourneyPatternInfo>,
    pub journey_end_names: Option<JourneyEndNames>,
    pub vehicle_journey_info: Option<VehicleJourneyInfo>,
    pub service_info: Option<ServiceInfo>,
    //pub journey_info: JourneyInfo,
    pub estimated_info: EstimatedInfo,
    pub disruption_group: Option<DisruptionGroup>,
    pub journey_progress_info: Option<JourneyProgressInfo>,
    pub operational_info: Option<OperationalInfo>,
    pub calls: Calls,
}
