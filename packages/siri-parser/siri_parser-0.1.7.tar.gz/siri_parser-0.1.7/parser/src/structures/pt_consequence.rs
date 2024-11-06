use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::enums::{conditions::Condition, severity::Severity};

use super::{blocking::Blocking, boarding::Boarding, pt_advice::PtAdvice};



#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct PtConsequence {
    pub condition: Condition, // 0:1
    pub severity: Severity, // 1:1
    pub advice: Option<PtAdvice>, // 0:1
    pub blocking: Option<Blocking>, // 0:1
    pub boarding: Boarding,
    pub delays: Option<u32>,

}