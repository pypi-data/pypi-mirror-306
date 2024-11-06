use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Default, Clone, Serialize, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct GroupReservation {
    name_of_group: String, // NLString
    number_of_seats: u32,  // NumberOfPassengers
}
