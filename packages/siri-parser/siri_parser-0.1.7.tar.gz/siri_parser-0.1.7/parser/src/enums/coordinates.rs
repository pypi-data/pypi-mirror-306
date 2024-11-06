use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub enum Coordinates {
    LatLong(Option<f64>, Option<f64>), // Latitude and Longitude
    GML(Option<String>),               // GML coordinates
}
