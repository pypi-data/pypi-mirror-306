use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};



#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct Network {
    pub network_ref: Option<String>,
    pub network_name: Option<String>,
    pub routes_affected: Option<String>,
}