use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, PartialEq, GoGenerate)]
#[serde(rename_all = "camelCase")]
enum Reason {
    Unknown,            // Inconnu
    Incident,           // Incident
    BombExplosion,      // Explosion d’une bombe
    SecurityAlert,      // Alerte sécurité
    Fire,               // Feu
    Vandalism,          // Vandalisme
    Accident,           // Accident
    Overcrowded,        // Surchargé
    InsufficientDemand, // Demande insuffisante
    LightingFailure,    // Panne d’éclairage
    ServiceFailure,     // Défaut de service
    Congestion,         // Congestion
    RouteBlockage,      // Blocage de l’itinéraire
    PersonOnTheLine,    // Personne sur la ligne
    VehicleOnTheLine,   // Véhicule sur la ligne
    ObjectOnTheLine,    // Objet sur la ligne
    AnimalOnTheLine,    // Animal sur la ligne
    RouteDiversion,     // Déviation
    RoadClosed,         // Route fermée
    Roadworks,          // Travaux
    SpecialEvent,       // Événement spécial
    BridgeStrike,       // Grève de pont
    UndefinedProblem,   // Problème non défini
}
