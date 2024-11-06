use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use super::{before_notice::BeforeNotice, parametised_action::ParameterisedAction};



#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct NotifyByEmailAction {
    pub parameterized_action: Option<ParameterisedAction>,
    pub before_notices: Vec<BeforeNotice>,
    pub clear_notice: Option<bool>,
    pub email: Option<String>,          // Email address for reminders
}