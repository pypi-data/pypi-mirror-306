use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, PartialEq, GoGenerate)]
#[serde(rename_all = "camelCase")]
pub enum EnvironmentReason {
    Unknown,                       // Inconnu
    Fog,                           // Brouillard
    RoughSea,                      // Mer Agitée
    HeavySnowFall,                 // Fortes Chutes de Neige
    HeavyRain,                     // Fortes Pluies
    StrongWinds,                   // Vents Forts
    TidalRestrictions,             // Restriction Liée aux Marées
    HighTide,                      // Marée Haute
    LowTide,                       // Marée Basse
    Ice,                           // Glace
    Frozen,                        // Gel
    Hail,                          // Grêle
    HighTemperatures,              // Température Élevée
    Flooding,                      // Inondation
    Waterlogged,                   // Sol Détrempé
    LowWaterLevel,                 // Niveau d’Eau Faible
    HighWaterLevel,                // Niveau d’Eau Élevé
    FallenLeaves,                  // Feuilles Mortes
    FallenTree,                    // Chute d’Arbres
    Landslide,                     // Glissement de Terrain
    UndefinedEnvironmentalProblem, // Problème Environnemental Non Défini
}
