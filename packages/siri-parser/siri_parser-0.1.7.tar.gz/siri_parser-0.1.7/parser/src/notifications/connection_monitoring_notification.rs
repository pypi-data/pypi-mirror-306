use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::deliveries::{connection_monitoring_feeder_delivery::ConnectionMonitoringFeederDelivery, connection_monitoring_distributor_delivery::ConnectionMonitoringDistributorDelivery};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct ConnectionMonitoringNotification {
    pub connection_monitoring_feeder_delivery: Option<ConnectionMonitoringFeederDelivery>,
    pub connection_monitoring_distributor_delivery: Option<ConnectionMonitoringDistributorDelivery>,
}
