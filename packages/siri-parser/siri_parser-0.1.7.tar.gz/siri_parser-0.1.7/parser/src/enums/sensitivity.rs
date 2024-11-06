use serde::{Deserialize, Serialize};
use go_generation_derive::GoGenerate;

#[derive(Debug, Serialize, Deserialize, PartialEq, GoGenerate, Eq, Clone)]
#[serde(rename_all = "camelCase")]
pub enum Sensivity {
    High,
    Medium,
    Low,
}
