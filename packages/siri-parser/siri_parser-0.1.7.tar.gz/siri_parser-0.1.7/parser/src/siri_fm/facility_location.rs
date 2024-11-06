use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct FacilityLocation {
    line_ref: Option<String>,                // Identifiant d’une ligne
    stop_point_ref: Option<String>,          // Identifiant d’un point d’arrêt
    vehicle_ref: Option<String>,             // Identifiant d’un véhicule
    stop_place_ref: Option<String>,          // Identifiant d’un lieu d’arrêt
    stop_place_component_id: Option<String>, // Identifiant d’un composant de lieu d’arrêt
    operator_ref: Option<String>,            // OPERATOR of a VEHICLE JOURNEY
}
