use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};



#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct AffectedOperator {
    pub operator_ref: String,               // Identifier for the operator (Transmodel)
}


#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "camelCase")]
pub enum AffectedOperatorType {
    AllOperators,
    AffectedOperator(AffectedOperator),
}