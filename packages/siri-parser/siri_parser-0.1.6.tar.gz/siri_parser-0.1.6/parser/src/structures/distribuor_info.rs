use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::models::framed_vehicle_journey_ref::FramedVehicleJourneyRef;

use super::connecting_journey::ConnectingJourney;



#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct DistributorInfo{
   pub interchange_ref: String,
   pub connection_link_ref: String,
   pub stop_point_ref: String,
   pub distributor_order: Option<u32>,
   pub distributor_journey: Option<ConnectingJourney>,
   pub feeder_vehicle_journey_ref: Option<FramedVehicleJourneyRef>,
}
