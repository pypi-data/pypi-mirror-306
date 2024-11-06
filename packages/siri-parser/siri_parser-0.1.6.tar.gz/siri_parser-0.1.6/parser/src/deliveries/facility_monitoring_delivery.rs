use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::models::xxx_delivery::XxxDelivery;
use crate::siri_fm::facility_condition::FacilityCondition;

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct FacilityMonitoringDelivery {
    #[serde(flatten)]
    pub leader: XxxDelivery,
    pub facility_condition: FacilityCondition,
}
