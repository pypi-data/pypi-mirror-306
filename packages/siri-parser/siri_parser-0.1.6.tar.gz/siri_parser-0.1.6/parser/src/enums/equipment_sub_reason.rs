use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, PartialEq, GoGenerate)]
#[serde(rename_all = "camelCase")]
pub enum EquipmentSubreason {
    TractionFailure,                   // Défaut de la Traction
    DefectiveTrain,                    // Train Défectueux
    SlipperyTrack,                     // Voie Glissante
    TrackCircuitProblem,               // Problème de Circuit de Voie
    SignalAndSwitchFailure,            // Échec du Signal et de Switch
    BrokenRail,                        // Rail Cassé
    PoorRailConditions,                // Mauvaises Conditions Ferroviaires
    LackOfOperationalStock,            // Manque de Stock Opérationnel
    DefectiveFireAlarmEquipment,       // Équipement d’Alarme Incendie Défectueux
    DefectivePlatformEdgeDoors,        // Portes Palières Défectueuses
    DefectiveCctv,                     // CCTV Défectueux
    DefectivePublicAnnouncementSystem, // Système d’Annonce Publique Défectueux
    TicketingSystemNotAvailable,       // Système Billetique Non Disponible
    LevelCrossingFailure,              // Défaut de Passage à Niveau
    TrafficManagementSystemFailure,    // Défaillance du Système de Gestion du Trafic
    EmergencyEngineeringWork,          // Travaux d’Ingénierie d’Urgence
    LateFinishToEngineeringWork,       // Finition Tardive de Travaux d’Ingénierie
    OverheadWireFailure,               // Panne de Câbles Aériens
}
