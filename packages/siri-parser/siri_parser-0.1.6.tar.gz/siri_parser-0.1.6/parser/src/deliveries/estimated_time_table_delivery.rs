use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::models::{
    estimated_journey_version_frame::EstimatedJourneyVersionFrame, xxx_delivery::XxxDelivery,
};



#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct EstimatedTimetableDelivery {
    #[serde(flatten)]
    pub leader: XxxDelivery,
    pub estimated_journey_version_frame: EstimatedJourneyVersionFrame,
}
