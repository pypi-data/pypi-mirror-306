use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::siri_et::{
    journey_identifier::JourneyIdentifier, journey_pattern_info::JourneyPatternInfo,
};

use super::{
    estimated_calls::EstimatedCalls, framed_vehicle_journey_ref::FramedVehicleJourneyRef,
    recorded_calls::RecordedCalls, train_numbers::TrainNumbers,
};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct EstimatedVehicleJourney {
    pub line_ref: String,
    pub published_line_name: Option<String>,
    pub direction_ref: Option<String>,
    pub journey_identifier: Option<JourneyIdentifier>,
    pub dated_vehicule_journey_ref: Option<String>,
    pub cancellation: Option<String>,
    pub extra_journey: Option<bool>,
    pub journey_pattern_name: Option<String>,
    pub journey_pattern_info: Option<JourneyPatternInfo>,
    pub vehicle_mode: Option<String>,
    pub origin_ref: Option<String>,
    pub origin_name: Option<String>,
    pub destination_ref: Option<String>,
    pub destination_name: Option<String>,
    pub operator_ref: Option<String>,
    pub product_category_ref: Option<String>,
    pub train_numbers: Option<TrainNumbers>,
    pub vehicule_journey_name: Option<String>,
    pub origin_aimed_departure_time: Option<String>,
    pub destination_aimed_arrival_time: Option<String>,
    pub recorded_calls: Option<RecordedCalls>,
    pub estimated_calls: Option<EstimatedCalls>,
    pub framed_vehicle_journey_ref: Option<FramedVehicleJourneyRef>,
    pub data_source: Option<String>,
    pub vehicle_ref: Option<String>,
    pub aimed_departure_time: Option<String>,
    pub aimed_arrival_time: Option<String>,
    pub journey_note: Option<String>,
    pub headway_service: Option<String>,
    pub first_or_last_journey: Option<String>, // (firstServiceOfDay | lastServiceOfDay | otherService | unspecified).
    pub disruption_group: Option<String>,      // Voir Disruption­Group.
    pub journey_progress_info: Option<String>, // Voir JourneyProgressInfo.
}
