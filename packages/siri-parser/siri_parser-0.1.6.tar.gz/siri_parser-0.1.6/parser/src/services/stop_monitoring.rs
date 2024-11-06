use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::{
    models::service_delivery_info::ServiceDeliveryInfo,
    notifications::stop_monitoring_notification::StopMonitoringNotification,
};
use pyo3::pyclass;

#[pyclass]
#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct NotifyStopMonitoring {
    pub service_delivery_info: ServiceDeliveryInfo,
    pub notification: StopMonitoringNotification,
}
