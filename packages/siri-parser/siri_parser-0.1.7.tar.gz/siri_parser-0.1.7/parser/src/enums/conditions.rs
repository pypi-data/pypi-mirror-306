use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, PartialEq, GoGenerate, Eq, Clone)]
#[serde(rename_all = "camelCase")]
pub enum Condition {
    Unknown,                     // inconnu
    Altered,                     // dégradé
    Cancelled,                   // annulé
    Delayed,                     // retardé
    Diverted,                    // dévié
    NoService,                   // pas de service
    Disrupted,                   // perturbé
    AdditionalService,           // service supplémentaire
    SpecialService,              // service spécial
    OnTime,                      // à l’heure
    NormalService,               // service normal
    IntermittentService,         // service intermittant
    ExtendedService,             // service étendu
    SplittingTrain,              // train fractionné
    ReplacementTransport,        // transport de remplacement
    ArrivesEarly,                // en avance
    ShuttleService,              // service navette
    ReplacementService,          // service de remplacement
    UndefinedServiceInformation, // service d’information inconnu
}
