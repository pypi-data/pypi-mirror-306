use crate::siri_sm::journey_pattern_info_group::JourneyPatternInfoGroup;
use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use super::framed_vehicle_journey_ref::FramedVehicleJourneyRef;

#[derive(Debug, Default, Clone, Serialize, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct VehicleActivityCancellation {
    recorded_at_time: Option<String>, // Heure à laquelle l’annulation a été signalée
    event_identity: Option<String>,   // Identifiant de l’objet annulé
    vehicle_monitoring_ref: Option<String>, // Identifiant du véhicule
    framed_vehicle_journey_ref: Option<FramedVehicleJourneyRef>, // Description de la course annulée
    line_ref: Option<String>,         // Identifiant de la ligne
    journey_pattern_info: Option<JourneyPatternInfoGroup>, // Informations sur le modèle de trajet
    reasons: Vec<String>,             // Description textuelle de la cause de l’annulation
}
