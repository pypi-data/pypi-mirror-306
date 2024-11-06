use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::{models::xxx_delivery::XxxDelivery, siri_gm::{info_message::InfoMessage, info_message_cancellation::InfoMessageCancellation}};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct GeneralMessageDelivery {
    #[serde(flatten)]
    pub leader: XxxDelivery,
    #[serde(alias = "InfoMessage", alias = "GeneralMessage")]
    pub info_message: Option<InfoMessage>,
    #[serde(alias = "InfoMessageCancellation", alias = "GeneralMessageCancellation")]
    pub info_message_cancellation: Option<InfoMessageCancellation>,
}
