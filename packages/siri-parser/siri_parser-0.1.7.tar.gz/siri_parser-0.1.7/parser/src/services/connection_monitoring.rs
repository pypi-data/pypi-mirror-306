use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::{
    models::service_delivery_info::ServiceDeliveryInfo,
    notifications::connection_monitoring_notification::ConnectionMonitoringNotification,
};

use pyo3::pyclass;

#[pyclass]
#[derive(Debug, Deserialize, Clone, Serialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct NotifyConnectionMonitoring {
    pub service_delivery_info: ServiceDeliveryInfo,
    pub notification: ConnectionMonitoringNotification,
}
