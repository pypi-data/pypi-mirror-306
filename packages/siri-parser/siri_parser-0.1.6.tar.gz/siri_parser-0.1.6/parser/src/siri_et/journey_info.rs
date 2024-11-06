use serde::{Deserialize, Serialize};

use crate::models::framed_vehicle_journey_ref::FramedVehicleJourneyRef;

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct JourneyInfo {
    pub vehicle_journey_name: Option<String>,
    pub journey_note: Vec<String>,
    line_ref: LineCode,                              // Identifiant de la ligne
    direction_ref: DestinationCode,                  // Identifiant de la direction
    vehicle_journey_ref: FramedVehicleJourneyRef,    // Identification de la course
    journey_pattern_ref: Option<JourneyPatternCode>, // Identifiant de la mission
    journey_pattern_name: Option<String>,            // Nom ou numéro de course
    vehicle_mode: Option<String>,                    // Mode de transport
    route_ref: Option<RouteCode>,                    // Identifiant de l'itinéraire
    published_line_name: Option<String>,             // Nom commercial de la ligne
    group_of_lines_ref: Option<GroupOfLinesCode>,    // Identifiant du groupe de lignes
    direction_name: Option<String>,                  // Nom de la destination
}
