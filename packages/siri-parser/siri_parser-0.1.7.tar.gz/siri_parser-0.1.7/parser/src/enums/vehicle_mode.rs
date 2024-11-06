use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "lowercase")]
pub enum VehicleMode {
    Air,
    Bus,
    Coach,
    Ferry,
    Metro,
    Rail,
    Tram,
    Underground,
    // Add more modes as needed
}
