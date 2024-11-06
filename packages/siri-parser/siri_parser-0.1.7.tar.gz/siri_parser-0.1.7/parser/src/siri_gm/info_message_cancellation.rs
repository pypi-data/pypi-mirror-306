use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, GoGenerate, Eq)]
#[serde(rename_all = "PascalCase")]
pub struct InfoMessageCancellation {
    pub recorded_at_time: String, // Heure à laquelle le message a été annulé
    pub info_message_identifier: String, // Référence InfoMessage du message à annuler
    pub info_channel_ref: Option<String>, // Canal auquel appartient le message
    //extensions: Option<Extensions>,  // Emplacement pour extension utilisateur
}
