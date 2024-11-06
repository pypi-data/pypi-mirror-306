use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, PartialEq, GoGenerate)]
#[serde(rename_all = "camelCase")]
pub enum EnvironmentWeatherSubreason {
    DriftingSnow,       // Neige à la Dérive
    BlizzardConditions, // Conditions de Blizzard
    StormDamage,        // Dégâts de Tempête
    StormConditions,    // Conditions de Tempête
    Slipperiness,       // Glissance
    IceDrift,           // Dérive de Glace
    GlazedFrost,        // Glacé
    LightningStrike,    // Coup de Foudre
    Avalanches,         // Avalanches
    FlashFloods,        // Crues Éclair
}
