use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone,  Serialize, Deserialize, PartialEq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub enum FirstOrLastJourneyEnum {
    FirstServiceOfDay,
    LastServiceOfDay,
    OtherService,
    Unspecified,
}
