use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};





#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct Direction {
    pub direction_ref: String,
    pub direction_name: String
}