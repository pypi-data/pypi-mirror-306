use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::deliveries::estimated_time_table_delivery::EstimatedTimetableDelivery;

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct EstimatedTimetableNotification {
    #[serde(
        alias = "EstimatedTimetableDelivery",
        alias = "siri1:EstimatedTimetableDelivery"
    )]
    pub estimated_timetable_delivery: EstimatedTimetableDelivery,
}
