use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::enums::{access_mode::AccessMode, severity::Severity};



#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct AffectedMode {
    //pub vehicle_mode: VehicleModesOfTransportation,
    pub access_mode: AccessMode,
    pub severity: Severity,
}