use crate::{
    models::service_delivery_info::ServiceDeliveryInfo,
    notifications::facility_monitoring_notification::FacilityMonitoringNotification,
};
use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};
use pyo3::pyclass;

#[pyclass]
#[derive(Debug, Deserialize, Clone, Serialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct NotifyFacilityMonitoring {
    pub service_delivery_info: ServiceDeliveryInfo,
    pub notification: FacilityMonitoringNotification,
}
