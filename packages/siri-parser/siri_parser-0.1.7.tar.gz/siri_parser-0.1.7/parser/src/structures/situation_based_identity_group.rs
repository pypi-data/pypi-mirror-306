use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct SituationBasedIdentityGroup {
    pub country_ref: String,
    pub participant_ref: String,
    pub situation_number: String,
    //pub situation_update_identity_group: Option<SituationUpdateIdentityGroup>,
    pub version: Option<String>
}