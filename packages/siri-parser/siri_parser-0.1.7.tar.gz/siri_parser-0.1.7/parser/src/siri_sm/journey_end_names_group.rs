use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use super::via::Via;

#[derive(Debug, Default, Clone, Serialize, Deserialize, PartialEq, GoGenerate, Eq)]
#[serde(rename_all = "PascalCase")]
pub struct JourneyEndNamesGroup {
    origin_ref: Option<String>,  // JourneyPlaceCode for the origin stop
    origin_name: Option<String>, // Name of the origin stop
    via: Option<Via>,            // Optional structure for via information
    destination_ref: String,     // JourneyPlaceCode for the destination stop (mandatory)
    destination_name: String,    // Name of the destination stop (mandatory)
}
