use crate::models::framed_vehicle_journey_ref::FramedVehicleJourneyRef;
use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct MonitoredVehicleJourney {
    line_ref: String, // LineCode
    framed_vehicle_journey_ref: FramedVehicleJourneyRef, // Framed-Vehicle-JourneyRef-Structure
                      // journey_pattern_info: Option<JourneyPatternInfo>, // Journey-Pattern-Info-Group
                      // vehicle_journey_info: Option<VehicleJourneyInfo>, // Vehicle-JourneyInfo-Group
                      // disruption_group: Option<DisruptionGroup>, // Disruption-Group
                      // journey_progress_info: Option<JourneyProgressInfo>, // Journey-Progress-Info-Group
                      // operational_info: Vec<TrainNumber>, // sequence
                      // journey_parts: Vec<JourneyPartInfo>, // List of journey parts
                      // calling_pattern: Option<MonitoredCall>, // Monitored-Call
                      // onward_calls: Option<OnwardCall>, // Onward-Calls
}
