use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::deliveries::situation_exchange_delivery::SituationExchangeDelivery;

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct SituationExchangeNotification {
    pub situation_exchange_delivery: SituationExchangeDelivery,
}
