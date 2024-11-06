use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, PartialEq, GoGenerate)]
#[serde(rename_all = "camelCase")]
enum CountedFeatureUnit {
    Bays,     // Emplacement pour garer un véhicule
    Seats,    // Place assise
    Devices,  // Les appareils divers (comme les casiers, les guides audio, etc.)
    Vehicles, // Tout type de véhicule
    Persons,  // Personne physique
}
