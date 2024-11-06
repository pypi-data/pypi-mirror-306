use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct StopAssignment {
    pub aimed_quay_ref: Option<String>,
    pub aimed_quay_name: Option<String>,
    pub expected_quay_ref: Option<String>,
}
