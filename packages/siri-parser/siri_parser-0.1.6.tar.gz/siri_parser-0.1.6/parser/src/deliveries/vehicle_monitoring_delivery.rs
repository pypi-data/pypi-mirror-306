use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::{
    models::xxx_delivery::XxxDelivery,
    siri_vm::{
        vehicle_activity::VehicleActivity,
        vehicle_activity_cancellation::VehicleActivityCancellation,
    },
};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct VehicleMonitoringDelivery {
    #[serde(flatten)]
    pub leader: XxxDelivery,
    pub vehicle_activity: Option<Vec<VehicleActivity>>,
    pub vehicle_activity_cancellation: Option<Vec<VehicleActivityCancellation>>,
}
