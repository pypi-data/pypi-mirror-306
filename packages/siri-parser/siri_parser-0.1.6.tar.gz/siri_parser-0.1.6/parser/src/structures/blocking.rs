use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};




#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct Blocking {
    /// Indicates whether the event data should be considered by a journey planner.
    journey_planner: bool, // 0:1
}