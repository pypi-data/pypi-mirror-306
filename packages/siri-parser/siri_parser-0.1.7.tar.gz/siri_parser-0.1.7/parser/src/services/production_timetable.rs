use crate::{
    models::service_delivery_info::ServiceDeliveryInfo,
    notifications::production_timetable_notification::ProductionTimetableNotification,
};
use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};
use pyo3::pyclass;

#[pyclass]
#[derive(Debug, Deserialize, Clone, Serialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct NotifyProductionTimetable {
    pub service_delivery_info: ServiceDeliveryInfo,
    pub notification: ProductionTimetableNotification,
}
