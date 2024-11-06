use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::deliveries::facility_monitoring_delivery::FacilityMonitoringDelivery;

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct FacilityMonitoringNotification {
    pub facility_monitoring_delivery: FacilityMonitoringDelivery,
}
