use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
pub struct TrainNumbers {
    #[serde(rename = "TrainNumberRef")]
    pub train_number_ref: Option<String>,
}
