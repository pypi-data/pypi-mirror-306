use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::siri_et::estimated_call::EstimatedCall;

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
pub struct EstimatedCalls {
    #[serde(alias = "EstimatedCall")]
    pub calls: Option<Vec<EstimatedCall>>,
}
