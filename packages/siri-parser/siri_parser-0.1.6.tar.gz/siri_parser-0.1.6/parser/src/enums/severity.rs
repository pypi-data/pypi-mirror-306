use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, PartialEq, GoGenerate, Eq, Clone)]
#[serde(rename_all = "camelCase")]
pub enum Severity {
    Unknown,   // Inconnu
    Slight,    // Léger
    Normal,    // Normal
    Severe,    // Sévère
    NoImpact,  // Pas d’impact
    Undefined, //Non défini
}
