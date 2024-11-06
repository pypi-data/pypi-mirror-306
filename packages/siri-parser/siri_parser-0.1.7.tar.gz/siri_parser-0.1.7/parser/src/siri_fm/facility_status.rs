use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::enums::facility_availability::FacilityAvailability;

use super::accessibility_assesment::AccessibilityAssessment;

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct FacilityStatus {
    pub status: Option<FacilityAvailability>, // Etat d’une Facility
    pub description: Option<String>,          // Description associée à l’état d’une Facility
    #[serde(rename = "AccessibilityAssessment")]
    pub accessibility_assesment: Vec<AccessibilityAssessment>, // État de l’accessibilité pour différents types de besoins spéciaux
}
