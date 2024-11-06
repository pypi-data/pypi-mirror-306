use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use super::{affected_line::AffectedLine, affected_mode::AffectedMode, affected_operator::AffectedOperator, network::Network};



#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct AffectedNetwork{
    pub operators: Vec<AffectedOperator>,
    #[serde(flatten)]
    pub network: Network,
    pub mode: AffectedMode,
    pub lines: Vec<LineAffected>
    
}

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "camelCase")]
pub enum LineAffected{
    AllLines,
    SelectedRoutes,
    AffectedLine(AffectedLine)
}