use crate::{
    models::xxx_delivery::XxxDelivery,
    siri_sm::{
        monitored_stop_visit::MonitoredStopVisit,
        monitored_stop_visit_cancellation::MonitoredStopVisitCancellation,
    },
};
use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct StopMonitoringDelivery {
    #[serde(flatten)]
    pub leader: XxxDelivery,
    pub monitoring_ref: Option<String>,
    pub monitored_stop_visit: Option<Vec<MonitoredStopVisit>>,
    pub monitored_stop_visit_cancellation: Option<Vec<MonitoredStopVisitCancellation>>,
}
