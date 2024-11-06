use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, GoGenerate)]
pub enum MonitoringError {
    GPS,
    GPRS,
    Radio,
}
