use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use super::publish_at_scope::PublishAtScope;




#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct ActionData {
    pub name: String,
    pub prompt: Option<String>,
    pub publish_at_scope: Option<PublishAtScope>,
}