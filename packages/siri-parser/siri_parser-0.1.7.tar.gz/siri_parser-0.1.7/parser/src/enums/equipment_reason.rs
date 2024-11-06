use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, PartialEq, GoGenerate)]
#[serde(rename_all = "camelCase")]
pub enum EquipmentReason {
    Unknown,                   // Inconnu
    SignalProblem,             // Problème de Signalisation
    SignalFailure,             // Panne de Signalisation
    Derailment,                // Déraillement
    EngineFailure,             // Panne Moteur
    BreakDown,                 // Panne
    TechnicalProblem,          // Problème Technique
    RepairWork,                // En Réparation
    ConstructionWork,          // Travaux de Construction
    MaintenanceWork,           // En Maintenance
    PowerProblem,              // Problème d’Alimentation
    FuelProblem,               // Problème de Carburant
    SwingBridgeFailure,        // Échec du Pont Tournant
    EscalatorFailure,          // Panne d’Escalator
    LiftFailure,               // Panne d’Ascenseur
    GangwayProblem,            // Problème de Passerelle
    ClosedForMaintenance,      // Fermeture pour Maintenance
    FuelShortage,              // Pénurie de Carburant
    DeicingWork,               // Travaux de Dégivrage
    WheelProblem,              // Problème de Roue
    LuggageCarouselProblem,    // Problème Carrousel à Bagages
    UndefinedEquipmentProblem, // Problème d’Équipement Non Défini
}
