use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq,  Serialize, Deserialize, Eq, GoGenerate)]
#[serde(rename_all = "camelCase")]
pub enum VehicleFeature {
    ShortTrain,
    LongTrain,
}