use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::{models::xxx_delivery::XxxDelivery, structures::{distributor_departure_cancellation::DistributorDepartureCancellation, stopping_position_change_departure::StoppingPositionChangeDeparture, wait_prolonged_departure::WaitProlongedDeparture}};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct ConnectionMonitoringDistributorDelivery {
    #[serde(flatten)]
    pub leader: XxxDelivery,
    pub wait_prolonged_departure: Option<WaitProlongedDeparture>,
    pub stopping_position_change_departure: Option<StoppingPositionChangeDeparture>,
    pub distributor_departure_cancellation: Option<DistributorDepartureCancellation>,
}
