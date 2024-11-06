use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::{models::framed_vehicle_journey_ref::FramedVehicleJourneyRef, siri_et::distribution_group::DisruptionGroup, siri_sm::{journey_pattern_info_group::JourneyPatternInfoGroup, vehicle_journey_info_group::VehicleJourneyInfoGroup}};



#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct ConnectingJourney  {
    pub line_ref: Option<String>,
    pub framed_journey_ref: FramedVehicleJourneyRef,
    pub journey_pattern_info: Option<JourneyPatternInfoGroup>,
    pub vehicle_journey_info: Option<VehicleJourneyInfoGroup>,
    pub distruptuin_group: Option<DisruptionGroup>,
    pub monitored: Option<bool>,
    pub aimed_arrival_time: Option<String>,
}