use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::deliveries::situation_monitoring_delivery::SituationMonitoringDelivery;

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct SituationMonitoringNotification {
    pub situation_monitoring_delivery: SituationMonitoringDelivery,
}
