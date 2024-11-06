use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq,  Serialize, Deserialize, Eq, GoGenerate)]
#[serde(rename_all = "camelCase")]
pub enum ActionStatus {
    // Define the possible statuses here, for example:
    Unknown,
    Active,
    Inactive,
    // Add other statuses as necessary
}