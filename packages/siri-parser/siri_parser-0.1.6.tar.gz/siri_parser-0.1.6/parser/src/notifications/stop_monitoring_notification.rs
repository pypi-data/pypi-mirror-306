use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::deliveries::stop_monitoring_delivery::StopMonitoringDelivery;

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct StopMonitoringNotification {
    pub stop_monitoring_delivery: StopMonitoringDelivery,
}
