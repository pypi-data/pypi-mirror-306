
use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::enums::{audience::Audience, scope_type::ScopeType, sensitivity::Sensivity};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct ReasonGroup {
    pub reason_name: Option<String>,
    pub severity: Option<String>,
    pub priority: Option<u32>,
    pub sensivity: Option<Sensivity>,
    pub audience: Option<Audience>,
    pub scope_type: Option<ScopeType>,
    pub planned: Option<bool>,
    pub keywords: Option<String>,
}