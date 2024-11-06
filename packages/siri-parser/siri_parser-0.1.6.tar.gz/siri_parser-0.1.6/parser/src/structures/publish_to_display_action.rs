use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use super::parametised_action::ParameterisedAction;



#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct PublishToDisplayAction {
    pub parameterized_action: Option<ParameterisedAction>,
    pub on_place: Option<bool>,        // Defaults to true
    pub onboard: Option<bool>,         // Defaults to false
}