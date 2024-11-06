use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::enums::occupancy::Occupancy;

use super::{
    arrival_info::ArrivalInfo, departure_info::DepartureInfo, distribution_group::DisruptionGroup,
    expected_departure_capacity::ExpectedDepartureCapacity,
    expected_departure_occupancy::ExpectedDepartureOccupancy,
};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct RecordedCall {
    pub stop_point_ref: String,
    pub order: u32,
    pub stop_point_name: Option<String>,
    pub extra_call: Option<bool>,
    pub cancellation: Option<bool>,
    pub occupancy: Option<Occupancy>,
    pub platform_traversal: Option<bool>,
    pub disruption_group: Option<DisruptionGroup>,
    pub arrival: Option<ArrivalInfo>,
    pub departure: Option<DepartureInfo>,
    pub expected_departure_occupancy: Option<ExpectedDepartureOccupancy>,
    pub expected_departure_capacity: Option<ExpectedDepartureCapacity>,
}
