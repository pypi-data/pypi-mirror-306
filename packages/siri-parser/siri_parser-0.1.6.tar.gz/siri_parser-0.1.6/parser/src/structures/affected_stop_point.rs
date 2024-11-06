use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use super::zone::Zone;



#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct AffectedStopPoint {
    pub stop_point_ref: Option<String>,
    pub affected_modes: Option<String>,
    #[serde(flatten)]
    pub zone: Option<Zone>,
}