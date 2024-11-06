use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::enums::action::ActionStatus;

use super::action_data::ActionData;



#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct ParameterisedAction {
    pub action_status: Option<ActionStatus>,      // Optional status of the action
    pub description: Option<String>,               // Optional description of the action
    pub action_data: Vec<ActionData>,              // List of associated action data
}