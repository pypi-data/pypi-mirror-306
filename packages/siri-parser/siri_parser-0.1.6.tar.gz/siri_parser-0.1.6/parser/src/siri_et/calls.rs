use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use super::{estimated_call::EstimatedCall, recorded_call::RecordedCall};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct Calls {
    pub recorded_calls: Option<Vec<RecordedCall>>,
    pub estimated_calls: Option<Vec<EstimatedCall>>,
    pub is_complete_stop_sequence: Option<bool>,
}
