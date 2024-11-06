use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::deliveries::production_timetable_delivery::ProductionTimetableDelivery;

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct ProductionTimetableNotification {
    pub production_timetable_delivery: ProductionTimetableDelivery,
}
