use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::{
    models::service_delivery_info::ServiceDeliveryInfo,
    notifications::estimated_timetable_notification::EstimatedTimetableNotification,
};

use pyo3::pyclass;

#[pyclass]
#[derive(Deserialize, Serialize, Clone, PartialEq, Debug, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct NotifyEstimatedTimetable {
    pub service_delivery_info: ServiceDeliveryInfo,
    pub notification: EstimatedTimetableNotification,
}
