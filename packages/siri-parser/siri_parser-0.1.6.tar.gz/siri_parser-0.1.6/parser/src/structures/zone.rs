use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};




#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct Zone {
    pub place_ref: String,
    pub place_name: String,
    // pub accessibility_assessment: Option<AccessibilityAssessment>,
    pub stop_condition: String, // RoutePointTypeEnumeration	
    //pub connection_links: Vec<AffectedConnectionLink>,

}