use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use super::{facility::Facility, facility_status::FacilityStatus, validity_period::ValidityPeriod};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct FacilityCondition {
    pub facility: Facility,           // Description générale d'une facility
    pub facility_ref: Option<String>, // Identifiant de la facility
    pub facility_status: Option<FacilityStatus>,
    // monitored_counting: Option<String>, // Mise à jour du compteur associé à la facility
    // facility_updated_position: Option<String>, // Mise à jour de la position de la facility
    //situation_ref: Option<String>, // Identifiant d'une situation associée todo("TODO")
    validity_period: Option<ValidityPeriod>, // Période de validité de la condition
                                             // extensions: Option<Extensions>, // user-defined extensions
}
