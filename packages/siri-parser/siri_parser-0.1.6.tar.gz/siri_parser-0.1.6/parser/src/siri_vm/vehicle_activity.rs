use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::siri_sm::monitored_vehicle_journey::MonitoredVehicleJourney;

use super::progress_between_stops::ProgressBetweenStops;

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct VehicleActivity {
    recorded_at_time: Option<String>, // Heure de mise à jour de la position
    valid_until_time: Option<String>, // Heure jusqu'à laquelle l'information est valable
    item_identifier: Option<String>,  // Identifiant pour annulation
    vehicle_monitoring_ref: Option<String>, // Identifiant du véhicule
    progress_between_stops: Option<ProgressBetweenStops>, // Position du véhicule entre les arrêts
    monitored_vehicle_journey: MonitoredVehicleJourney, // Détails de la course effectuée par le véhicule
    vehicle_activity_note: Option<String>, // Informations textuelles concernant le véhicule
}
