use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct ServiceDeliveryInfo {
    pub response_timestamp: Option<String>,
    pub producer_ref: String,
    pub request_message_identifier: Option<String>,
    pub response_message_ref: Option<String>,
}
