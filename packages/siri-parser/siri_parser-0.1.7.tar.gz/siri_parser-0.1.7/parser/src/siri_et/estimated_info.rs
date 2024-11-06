use super::fist_or_last_journey_enum::FirstOrLastJourneyEnum;
use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct EstimatedInfo {
    pub headway_service: Option<bool>,
    pub origin_aimed_departure_time: Option<String>,
    pub destination_aimed_arrival_time: Option<String>,
    pub first_or_last_journey: Option<FirstOrLastJourneyEnum>,
}
