use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::enums::{progress_status::ProgressStatus, quality_index::QualityIndex, verification_status::VerificationStatus};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct PtSituationBodyGroup{
    pub verification: Option<VerificationStatus>,
    pub progress: Option<ProgressStatus>,
    pub quality_index: Option<QualityIndex>,
    pub publication: Option<String>, // TODO : enum
}