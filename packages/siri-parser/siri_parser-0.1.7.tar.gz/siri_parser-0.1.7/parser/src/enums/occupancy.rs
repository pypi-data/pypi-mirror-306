use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, Eq, GoGenerate)]
#[serde(rename_all = "camelCase")]
pub enum Occupancy {
    Full,
    SeatsAvailable,
    StandingAvailable,
    Unknown,
    Empty,
    ManySeatAvailable,
    FewSeatAvailable,
    StandingRoomOnly,
    CrushStandingRoomOnly,
    NotAcceptingPassengers,
}
