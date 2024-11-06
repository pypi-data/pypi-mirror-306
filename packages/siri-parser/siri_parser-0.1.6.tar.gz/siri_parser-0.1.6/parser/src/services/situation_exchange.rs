use crate::{
    models::service_delivery_info::ServiceDeliveryInfo,
    notifications::situation_exchange_notification::SituationExchangeNotification,
};
use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};
use pyo3::pyclass;

#[pyclass]
#[derive(Debug, Deserialize, Clone, Serialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct NotifySituationExchange {
    pub service_delivery_info: ServiceDeliveryInfo,
    pub notification: SituationExchangeNotification,
}
