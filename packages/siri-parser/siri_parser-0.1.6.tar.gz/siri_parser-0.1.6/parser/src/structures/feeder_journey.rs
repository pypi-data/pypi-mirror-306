use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::models::framed_vehicle_journey_ref::FramedVehicleJourneyRef;



#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct FeederJourney  {
    pub line_ref: Option<String>,
    pub direction_ref: Option<String>,
    pub framed_journey_ref: FramedVehicleJourneyRef,
    pub monitored: Option<bool>,
    pub aimed_arrival_time: Option<String>,
}