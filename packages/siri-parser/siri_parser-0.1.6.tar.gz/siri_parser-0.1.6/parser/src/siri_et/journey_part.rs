use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct JourneyPart {
    pub journey_part_ref: Option<String>,
    pub train_number_ref: Option<String>,
}
