use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::{models::xxx_delivery::XxxDelivery, structures::{monitored_feeder_arrival::MonitoredFeederArrival, monitored_feeder_arrival_cancellation::MonitoredFeederArrivalCancellation}};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct ConnectionMonitoringFeederDelivery {
    #[serde(flatten)]
    pub leader: XxxDelivery,
    pub monitored_feeder_arrival: MonitoredFeederArrival,
    pub monitored_feeder_arrival_cancellation: MonitoredFeederArrivalCancellation,
}
