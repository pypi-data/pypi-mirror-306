use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};


#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct DistributorConnectionLink {
    pub connection_code: Option<String>,
    pub stop_point_ref: Option<String>,
    pub interchange_duration: Option<u32>,
    pub frequent_traveller_duration: Option<u32>,
    pub occasional_traveller_duration: Option<u32>,
    pub impaired_access_duration: Option<u32>
}