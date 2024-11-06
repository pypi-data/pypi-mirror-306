use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::deliveries::vehicle_monitoring_delivery::VehicleMonitoringDelivery;

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct VehicleMonitoringNotification {
    pub vehicle_monitoring_delivery: VehicleMonitoringDelivery,
}
