use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::{
    enums::{
        arrival_status::ArrivalStatus, boarding_activity::BoardingActivity,
        departure_status::DepartureStatus,
    },
    siri_et::{
        distribution_group::DisruptionGroup,
        expected_departure_capacity::ExpectedDepartureCapacity,
        expected_departure_occupancy::ExpectedDepartureOccupancy,
    },
};

use super::stop_identity::StopIdentity;

#[derive(Debug, Default, Clone, Serialize, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct MonitoredCall {
    stop_identity: StopIdentity,                           // Stop-Point-Ref
    order: Option<u32>,                                    // xsd:positiveInteger
    stop_point_name: String,                               // NLString
    vehicle_at_stop: Option<bool>,                         // xsd:boolean
    platform_traversal: Option<bool>,                      // xsd:boolean
    destination_display: Option<String>,                   // NLString
    disruption_group: Option<DisruptionGroup>,             // Disruption-Group
    aimed_arrival_time: Option<String>,                    // xsd:dateTime
    actual_arrival_time: Option<String>,                   // xsd:dateTime
    expected_arrival_time: Option<String>,                 // xsd:dateTime
    arrival_status: Option<ArrivalStatus>,                 // Arrival-Status
    arrival_proximity_text: Vec<String>,                   // NLString
    arrival_platform_name: Option<String>,                 // NLString
    aimed_quay_name: Option<String>,                       // NLString
    aimed_departure_time: Option<String>,                  // xsd:dateTime
    actual_departure_time: Option<String>,                 // xsd:dateTime
    expected_departure_time: Option<String>,               // xsd:dateTime
    departure_status: Option<DepartureStatus>,             // Departure-Status
    departure_platform_name: Option<String>,               // NLString
    departure_boarding_activity: Option<BoardingActivity>, // boarding | noBoarding | passThru
    expected_departure_occupancy: Vec<ExpectedDepartureOccupancy>, // +structure
    expected_departure_capacity: Vec<ExpectedDepartureCapacity>, // +structure
    aimed_headway_interval: Option<u32>,                   // Positive-DurationType
    expected_headway_interval: Option<u32>,                // Positive-DurationType
    distance_from_stop: Option<u32>,                       // DistanceType
    number_of_stops_away: Option<u32>,                     // nonNegativeInteger
                                                           //extensions: Option<Extensions>, // user-defined extensions
}
