use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, PartialEq, GoGenerate, Eq, Clone)]
#[serde(rename_all = "camelCase")]
pub enum ScopeType {
    General,        // La perturbation a un impact global.
    Operator,       // La perturbation a un impact sur un opérateur spécifique.
    Network,        // La perturbation a un impact sur tout le réseau.
    Route,          // La perturbation a un impact sur un itinéraire particulier.
    Line,           // La perturbation a un impact sur une ligne particulière.
    Place,          // La perturbation a un impact sur un lieu particulier.
    StopPlace,      // La perturbation a un impact sur un lieu d’arrêt particulier.
    StopPoint,      // La perturbation a un impact sur un point d’arrêt particulier.
    VehicleJourney, // La perturbation a un impact sur une course spécifique.
}
