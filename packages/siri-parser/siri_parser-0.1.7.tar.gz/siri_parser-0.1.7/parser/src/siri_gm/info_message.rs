use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, GoGenerate, Eq)]
#[serde(rename_all = "PascalCase")]
pub struct InfoMessage {
    format_ref: Option<String>,                // FormatCode - always "France" for this profile
    recorded_at_time: String,   // Heure d'enregistrement du message
    item_identifier: Option<String>,          // Identifiant unique du message SIRI
    info_message_identifier: String,   // Identifiant InfoMessage
    info_message_version: Option<u32>, // Version du InfoMessage
    info_channel_ref: String,          // Canal auquel appartient le message
    valid_until_time: String,   // Date et heure jusqu'à laquelle le message est valide
    situation_ref: Option<String>, // Référence à des événements externes
    content: Option<String>,                   // Le message lui-même
    //extensions: Option<Extensions>,    // Emplacement pour extension utilisateur
}
