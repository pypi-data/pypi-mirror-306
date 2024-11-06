use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::models::framed_vehicle_journey_ref::FramedVehicleJourneyRef;

use super::journey_pattern_info_group::JourneyPatternInfoGroup;

#[derive(Debug, Default, Clone, Serialize, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct MonitoredStopVisitCancellation {
    recorded_at_time: String,                              // xsd:dateTime
    event_identity: Option<String>,                        // ItemRef
    monitoring_ref: Option<String>,                        // MonitoringCode
    line_ref: Option<String>,                              // LineCode
    vehicle_journey_ref: Option<FramedVehicleJourneyRef>, // Structure (FramedVehicleJourneyRefStructure)
    journey_pattern_info: Option<JourneyPatternInfoGroup>, // Journey-Pattern-Info-Group
    message_reason: Option<String>,                       // NLString
                                                          //extensions: Option<Extensions>, // user-defined extensions
}
