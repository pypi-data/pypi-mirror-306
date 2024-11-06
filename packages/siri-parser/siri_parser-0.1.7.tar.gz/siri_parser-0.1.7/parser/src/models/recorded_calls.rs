use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::siri_et::recorded_call::RecordedCall;

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
pub struct RecordedCalls {
    #[serde(rename = "RecordedCall")]
    pub calls: Option<Vec<RecordedCall>>,
}
