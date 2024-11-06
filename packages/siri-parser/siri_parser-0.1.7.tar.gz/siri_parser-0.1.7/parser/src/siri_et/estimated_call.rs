use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::enums::{
    arrival_status::ArrivalStatus, boarding_activity::BoardingActivity,
    departure_status::DepartureStatus, occupancy::Occupancy,
};

use super::{
    arrival::Arrival, departure::Departure, expected_capacity::ExpectedCapacity,
    expected_occupancy::ExpectedOccupancy,
};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct EstimatedCall {
    stop_point_ref: Option<String>,  // StopPointRef
    order: Option<u32>,              // positiveInteger
    stop_point_name: Option<String>, // NLString
    extra_call: Option<bool>,
    cancellation: Option<bool>,       // boolean
    occupancy: Option<Occupancy>,     // occupancy levels
    platform_traversal: Option<bool>, // boolean
    destination_display: Option<String>,
    aimed_arrival_time: Option<String>,          // dateTime
    expected_arrival_time: Option<String>,       // dateTime
    arrival_status: Option<ArrivalStatus>,       // onTime, missed, delayed, etc.
    arrival_proximity_text: Option<Vec<String>>, // NLString
    arrival_platform_name: Option<String>,       // NLString
    arrival_stop_assignment: Option<String>,     // structure
    aimed_quay_name: Option<String>,             // NLString
    aimed_departure_time: Option<String>,        // dateTime
    expected_departure_time: Option<String>,     // dateTime
    departure_status: Option<DepartureStatus>,   // onTime, early, delayed, etc.
    departure_platform_name: Option<String>,     // NLString
    departure_boarding_activity: Option<BoardingActivity>, // boarding, noBoarding, etc.
}
