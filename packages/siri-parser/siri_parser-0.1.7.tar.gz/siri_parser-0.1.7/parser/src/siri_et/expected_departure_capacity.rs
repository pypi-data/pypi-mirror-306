use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct ExpectedDepartureCapacity {
    train_formation_reference_group: Option<String>, // TrainFormation-ReferenceGroup
    passenger_category: Option<String>,              // NLString
    total_capacity: Option<u32>,                     // NumberOf-Passengers
    seating_capacity: Option<u32>,                   // NumberOf-Passengers
    standing_capacity: Option<u32>,                  // NumberOf-Passengers
    pushchair_capacity: Option<u32>,                 // NumberOf-Passengers
    wheelchair_place_capacity: Option<u32>,          // NumberOf-Passengers
    pram_place_capacity: Option<u32>,                // nonnegative-Integer
    bicycle_rack_capacity: Option<u32>,              // nonnegative-Integer
}
