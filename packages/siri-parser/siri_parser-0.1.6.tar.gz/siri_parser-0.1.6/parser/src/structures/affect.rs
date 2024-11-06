use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use super::{affected_operator::AffectedOperatorType, affected_place::AffectedPlace, affected_stop_point::AffectedStopPoint, affected_vehicle_journey::AffectedVehicleJourney, network::Network};




#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct Affect{
    pub area_of_interest: Option<String>,      // Geographic area of interest
    pub operators: Vec<AffectedOperatorType>,        // Operators affected
    pub networks: Vec<Network>,           // Networks impacted
    pub stop_points: Vec<AffectedStopPoint>,            // Scheduled stop points impacted
    pub stop_places: Vec<AffectedPlace>,      // Stop places impacted
    pub places: Vec<AffectedPlace>,                // Places impacted
    pub vehicle_journeys: Vec<AffectedVehicleJourney>,    // Vehicle journeys impacted
    //pub vehicles: Vec<Vehicle>,           // Vehicles impacted
}



