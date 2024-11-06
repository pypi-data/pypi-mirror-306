use crate::{
    models::service_delivery_info::ServiceDeliveryInfo,
    notifications::general_message_notification::GeneralMessageNotification,
};
use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};
use pyo3::pyclass;

#[pyclass]
#[derive(Debug, Deserialize, Clone, Serialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct NotifyGeneralMessage {
    pub service_delivery_info: ServiceDeliveryInfo,
    pub notification: GeneralMessageNotification,
}
