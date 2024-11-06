use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use super::parametised_action::ParameterisedAction;



#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct PublishToWebAction {
    pub parameterized_action: Option<ParameterisedAction>,
    pub incidents: Option<bool>,       // Defaults to true
    pub home_page: Option<bool>,       // Defaults to false
    pub ticker: Option<bool>,          // Defaults to false
    pub social_network: Vec<String>,   // e.g., "twitter.com", "facebook.com"
}