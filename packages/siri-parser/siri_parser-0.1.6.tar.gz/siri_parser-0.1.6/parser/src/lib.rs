use models::body::Body;

use go_generation_derive::GoGenerate;
use pyo3::pyclass;
use serde::{
    de::{DeserializeOwned, Visitor},
    Deserialize, Deserializer, Serialize,
};
use services::{
    connection_monitoring::NotifyConnectionMonitoring, estimated_table::NotifyEstimatedTimetable,
    facility_monitoring::NotifyFacilityMonitoring, general_message::NotifyGeneralMessage,
    production_timetable::NotifyProductionTimetable, situation_exchange::NotifySituationExchange,
    stop_monitoring::NotifyStopMonitoring, vehicle_monitoring::NotifyVechicleMonitoring,
};
use std::{fmt, fs};

pub mod deliveries;
pub mod enums;
pub mod models;
pub mod notifications;
pub mod services;
pub mod siri_et;
pub mod siri_sm;
pub mod structures;
pub mod siri_vm;
pub mod siri_gm;
pub mod siri_fm;


#[derive(Debug, Serialize, Deserialize, PartialEq)]
pub struct Error {
    pub description: Option<String>, // Optional description of the error
}

#[derive(Debug, Serialize, Deserialize, PartialEq)]
pub enum ErrorCondition {
    CapabilityNotSupportedError(Box<Error>), // Request not supported
    OtherError(Box<Error>),                  // Other error
}



#[derive(Debug, Clone, Serialize, PartialEq, Eq, GoGenerate)]
pub enum SiriServiceType {
    ProductionTimetable(NotifyProductionTimetable), // Delivery structure for production timetable
    EstimatedTimetable(NotifyEstimatedTimetable),   // Delivery structure for estimated timetable
    StopMonitoring(NotifyStopMonitoring),           // Delivery structure for stop monitoring
    VehicleMonitoring(NotifyVechicleMonitoring),    // Delivery structure for vehicle monitoring
    ConnectionMonitoring(NotifyConnectionMonitoring), // Delivery structure for connection monitoring
    GeneralMessage(NotifyGeneralMessage),             // Delivery structure for general message
    FacilityMonitoring(NotifyFacilityMonitoring),     // Delivery structure for facility monitoring
    SituationExchange(NotifySituationExchange),       // Delivery structure for situation exchange
}

/// SiriServiceType deserializer
///
/// # Arguments
///
/// * `deserializer` - The deserializer
///
/// # Returns
///
/// * `SiriServiceType` - The deserialized value
///
/// # Errors
///
/// * `serde::de::Error` - Error deserializing the value
///
impl<'de> Deserialize<'de> for SiriServiceType {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        struct SiriServiceTypeVisitor;

        impl<'de> Visitor<'de> for SiriServiceTypeVisitor {
            type Value = SiriServiceType;

            fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
                formatter.write_str("an XML element representing SiriServiceType")
            }

            fn visit_map<V>(self, mut map: V) -> Result<Self::Value, V::Error>
            where
                V: serde::de::MapAccess<'de>,
            {
                let mut service_type = None;
                while let Some(key) = map.next_key()? {
                    match key {
                        "NotifyProductionTimetable" => {
                            service_type =
                                Some(SiriServiceType::ProductionTimetable(map.next_value()?));
                        }
                        "NotifyEstimatedTimetable" => {
                            service_type =
                                Some(SiriServiceType::EstimatedTimetable(map.next_value()?));
                        }
                        "NotifyStopMonitoring" => {
                            service_type = Some(SiriServiceType::StopMonitoring(map.next_value()?));
                        }
                        "GetVehicleMonitoringResponse" => {
                            service_type =
                                Some(SiriServiceType::VehicleMonitoring(map.next_value()?));
                        }
                        "NotifyConnectionMonitoring" => {
                            service_type =
                                Some(SiriServiceType::ConnectionMonitoring(map.next_value()?));
                        }
                        "NotifyGeneralMessage" => {
                            service_type = Some(SiriServiceType::GeneralMessage(map.next_value()?));
                        }
                        "NotifyFacilityMonitoring" => {
                            service_type =
                                Some(SiriServiceType::FacilityMonitoring(map.next_value()?));
                        }
                        "NotifySituationExchange" => {
                            service_type =
                                Some(SiriServiceType::SituationExchange(map.next_value()?));
                        }
                        "GeneralMessage" => {
                            service_type = Some(SiriServiceType::GeneralMessage(map.next_value()?));
                        }

                        _ => {
                            return Err(serde::de::Error::unknown_field(
                                key.to_string().as_str(),
                                &["EstimatedTimetable", "StopMonitoring"],
                            ));
                        }
                    }
                }
                match service_type {
                    Some(service_type) => Ok(service_type),
                    None => Err(serde::de::Error::custom("Missing service type")),
                }
            }
        }

        deserializer.deserialize_map(SiriServiceTypeVisitor)
    }
}

/// The XML Envelope
///
/// # Attributes
///
/// * `Body` - The body of the envelope
///
#[pyclass]
#[derive(Debug, Serialize, Deserialize, PartialEq, Eq, GoGenerate)]
pub struct Envelope {
    #[serde(rename = "Body", alias = "soapenv:Body", alias = "Body")]
    pub body: Body,
}

#[derive(Debug, Serialize, Deserialize, PartialEq)]
#[serde(rename_all = "PascalCase")]
pub struct SIRI;

impl SIRI {
    /// Parse XML file to T
    ///
    /// # Arguments
    ///
    /// * `file_path` - The file path
    ///
    /// # Returns
    ///
    /// * `Result<T, Box<dyn std::error::Error>>`
    ///
    pub fn from_file<T: DeserializeOwned>(
        file_path: &str,
    ) -> Result<T, Box<dyn std::error::Error>> {
        let content = fs::read_to_string(file_path)?;
        let envelope: T = quick_xml::de::from_str(&content)?;
        Ok(envelope)
    }

    /// Parse XML string to T
    ///
    /// # Arguments
    ///
    /// * `xml_str` - The XML string
    ///
    /// # Returns
    ///
    /// * `Result<T, Box<dyn std::error::Error>>`
    ///
    pub fn from_str<'a, T: Deserialize<'a>>(
        xml_str: &'a str,
    ) -> Result<T, Box<dyn std::error::Error>> {
        let envelope: T = quick_xml::de::from_str(xml_str)?;
        Ok(envelope)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_siri_et_from_file() {
        let result = SIRI::from_file::<Envelope>("src/fixtures/siri_et_xml_tn/trip_add.xml");
        assert!(result.is_ok());
    }

    #[test]
    fn test_siri_sm_from_file() {
        let result = SIRI::from_file::<Envelope>(
            "src/fixtures/siri_sm/siri-destineo-sm-cus-2-2024-04-04-13-02-25.xml",
        );
        assert!(result.is_ok());
    }
}
