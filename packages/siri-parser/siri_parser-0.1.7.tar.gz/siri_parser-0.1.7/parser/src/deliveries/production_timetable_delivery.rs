use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::{models::xxx_delivery::XxxDelivery, structures::dated_timetable_version_frame::DatedTimetableVersionFrame};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct ProductionTimetableDelivery {
    #[serde(flatten)]
    pub leader: XxxDelivery,
    pub dated_timetable_version_frame: DatedTimetableVersionFrame,
}
