use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "camelCase")]
pub enum FacilityClass {
    FixedEquipment,
    MobileEquipment,
    SiteComponent,
    Site,
    ParkingBay,
    Vehicle,
}
