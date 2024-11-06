use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::enums::facility_class::FacilityClass;

use super::{
    accessibility_assesment::AccessibilityAssessment, facility_location::FacilityLocation,
    validity_condition::ValidityCondition,
};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct Facility {
    facility_code: Option<String>, // FacilityCode - Identifiant de la Facility
    description: Option<String>,   // Description de la facility
    facility_class: Option<FacilityClass>, // Classe de la facility
    // features: Vec<Feature>, // Fonctionnalités du service todo("add support for features")
    validity_condition: Option<ValidityCondition>,
    facility_location: Option<FacilityLocation>,
    accessibility_assesment: Option<AccessibilityAssessment>, // Informations d’accessibilité
    limitations: Option<Limitations>,
    suitabilities: Option<Suitabilities>,
}

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct Limitations {
    pub wheelchair_access: Option<bool>,
    pub step_free_access: Option<bool>,
    pub lift_free_access: Option<bool>,
}

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct Suitabilities {
    pub suitability: Option<Vec<Suitability>>,
}

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct Suitability {
    pub suitable: String,
    pub user_need: Option<UserNeed>,
}

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct UserNeed {
    pub mobility_need: Option<String>,
}
