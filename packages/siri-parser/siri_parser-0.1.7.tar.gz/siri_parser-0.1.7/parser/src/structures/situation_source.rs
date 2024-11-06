use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::enums::source_type::SourceType;

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct SituationSource{
    pub name: Option<String>,
    pub source_type: Option<SourceType>
}