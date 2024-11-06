use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use super::validity_period::ValidityPeriod;

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct ValidityCondition {
    pub period: Vec<ValidityPeriod>,
}
