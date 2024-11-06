use crate::{
    models::service_delivery_info::ServiceDeliveryInfo,
    notifications::vehicle_monitoring_notification::VehicleMonitoringNotification,
};
use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};
use pyo3::pyclass;

#[pyclass]
#[derive(Debug, Deserialize, Clone, Serialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct NotifyVechicleMonitoring {
    pub service_delivery_info: ServiceDeliveryInfo,
    #[serde(rename = "Answer", alias = "Anwser", alias = "Notification")]
    pub notification: VehicleMonitoringNotification,
}
