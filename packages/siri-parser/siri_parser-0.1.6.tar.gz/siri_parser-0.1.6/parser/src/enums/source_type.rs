use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, PartialEq, GoGenerate, Eq, Clone)]
#[serde(rename_all = "camelCase")]
pub enum SourceType {
    DirectReport, // Rapport remis en direct
    Email,        // Rapport reçu via email
    Phone,        // Rapport reçu via téléphone
    Post,         // Rapport reçu via courrier postal
    Feed,         // Rapport reçu via alimentation automatique
    Radio,        // Rapport reçu via radio
    TV,           // Rapport reçu via TV
    Web,          // Rapport reçu via website
    Text,         // Rapport reçu via message
    Other,        // Rapport reçu via autres moyens
}
