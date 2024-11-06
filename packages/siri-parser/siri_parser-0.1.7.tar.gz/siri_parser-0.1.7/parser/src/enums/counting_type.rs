use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, PartialEq, GoGenerate)]
#[serde(rename_all = "camelCase")]
enum CountingType {
    AvailabilityCount, // Comptage des véhicules disponibles, des appareils, de l'espace, etc.
    ReservedCount,     // Comptage du véhicule réservé, des appareils, de l'espace, etc.
    OutOfOrderCount,   // Comptage des véhicules, appareils, espaces hors service, etc.
    PresentCount,      // Comptage des personnes présentes.
    CurrentStateCount, // Niveau de ressource ou statut de la mesure (carburant, etc.).
}
