use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::deliveries::general_message_delivery::GeneralMessageDelivery;

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct GeneralMessageNotification {
    pub general_message_delivery: GeneralMessageDelivery,
}
