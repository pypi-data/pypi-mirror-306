use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Default, Clone, Serialize, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct StopIdentity {
    stop_point_code: String, // StopPoint-Code
                             // Add any additional fields as necessary
}
