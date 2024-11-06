use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::{enums::{audience::Audience, scope_type::ScopeType, sensitivity::Sensivity}, siri_fm::validity_period::ValidityPeriod};

use super::{affect::Affect, pt_consequence::PtConsequence, pt_situation_body_group::PtSituationBodyGroup, publishing_actions::PublishingActions, situation_based_identity_group::SituationBasedIdentityGroup, situation_source::SituationSource};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct PtSituationElement {
    pub creation_time: String, // Heure de creation de SITUATION (xsd:dateTime)
    pub situation_based_identity_group: SituationBasedIdentityGroup, // →Group	Éléments Référence à une SITUATION ou mise à jour d'une SITUATION. ParticipantRef est facultatif et peut être fourni à partir du contexte.
    pub source: Option<SituationSource>,
    pub versioned_at_time: Option<String>,
    pub verification: Option<PtSituationBodyGroup>,
    pub validity_period: Option<ValidityPeriod>,
    pub reason_name: Option<String>,
    pub severity: Option<String>,
    pub priority: Option<u32>,
    pub sensivity: Option<Sensivity>,
    pub audience: Option<Audience>,
    pub scope_type: Option<ScopeType>,
    pub planned: Option<bool>,
    pub keywords: Option<String>,
    pub summary: Option<String>,
    pub description: Option<String>,
    pub detail: Option<String>,
    pub advice: Option<String>,
    pub internal: Option<String>,
    //pub images: Vec<Image>,
    //pub info_links: Vec<InfoLink>,
    pub affects: Vec<Affect>,
    pub consequences: Vec<PtConsequence>,
    pub publishing_actions: Option<PublishingActions>,
}
