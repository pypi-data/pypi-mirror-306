use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::enums::occupancy::Occupancy;

use super::group_reservation::GroupReservation;

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct ExpectedDepartureOccupancy {
    passenger_category: Option<String>,        // NLString
    occupancy_level: Option<Occupancy>,        // Occupancy-Enumeration
    occupancy_percentage: Option<u32>,         // PercentageType
    alighting_count: Option<u32>,              // NumberOf-Passengers
    boarding_count: Option<u32>,               // NumberOf-Passengers
    onboard_count: Option<u32>,                // NumberOf-Passengers
    group_reservations: Vec<GroupReservation>, // Group-Reservation
}
