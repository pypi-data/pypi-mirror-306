use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};
use serde_json::Value;

#[derive(Debug, Serialize, Clone, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct XxxDelivery {
    pub response_timestamp: String, // Timestamp for when the response was created
    #[serde(rename = "@optional")]
    pub request_message_ref: Option<String>, // Optional reference for the originating request
    #[serde(rename = "@optional")]
    pub subscriber_ref: Option<String>, // Optional identifier for the subscriber (mandatory if related to a subscription)
    #[serde(rename = "@optional")]
    pub subscription_ref: Option<String>, // Mandatory identifier for the subscription issued by the requester
    #[serde(rename = "@optional")]
    pub status: Option<bool>, // Indicates if the complete request was processed successfully
    //pub error_condition: Option<ErrorCondition>,            // Optional error condition details
    #[serde(rename = "@optional")]
    pub valid_until: Option<String>, // Optional validity limit for the data
    #[serde(rename = "@optional")]
    pub shortest_possible_cycle: Option<u32>, // Optional minimum interval for updates (could be a duration type)
}

impl<'de> Deserialize<'de> for XxxDelivery {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: serde::Deserializer<'de>,
    {
        struct XxxDeliveryVisitor;

        impl<'de> serde::de::Visitor<'de> for XxxDeliveryVisitor {
            type Value = XxxDelivery;

            fn expecting(&self, formatter: &mut std::fmt::Formatter) -> std::fmt::Result {
                formatter.write_str("an XML element representing XxxDelivery")
            }

            fn visit_map<V>(self, mut map: V) -> Result<Self::Value, V::Error>
            where
                V: serde::de::MapAccess<'de>,
            {
                let mut response_timestamp = None;
                let mut request_message_ref = None;
                let mut subscriber_ref = None;
                let mut subscription_ref = None;
                let mut status = None;
                //let mut error_condition = None;
                let mut valid_until = None;
                let mut shortest_possible_cycle = None;

                while let Some(key) = map.next_key::<String>()? {
                    match key.as_str() {
                        key if key.starts_with("@xmlns:siri") => {
                            continue;
                        }
                        key if key.starts_with("@version") => {
                            continue;
                        }
                        "ResponseTimestamp" => {
                            let value: Value = map.next_value()?;
                            response_timestamp =
                                value.get("$text").and_then(Value::as_str).map(String::from);
                        }
                        "RequestMessageRef" => {
                            let value: Value = map.next_value()?;
                            request_message_ref =
                                value.get("$text").and_then(Value::as_str).map(String::from);
                        }
                        "SubscriberRef" => {
                            let value: Value = map.next_value()?;
                            subscriber_ref =
                                value.get("$text").and_then(Value::as_str).map(String::from);
                        }
                        "SubscriptionRef" => {
                            let value: Value = map.next_value()?;
                            subscription_ref =
                                value.get("$text").and_then(Value::as_str).map(String::from);
                        }
                        "Status" => {
                            let value: Value = map.next_value()?;
                            status = value.get("$text").and_then(Value::as_bool);
                        }
                        "ValidUntil" => {
                            let value: Value = map.next_value()?;
                            valid_until =
                                value.get("$text").and_then(Value::as_str).map(String::from);
                        }
                        "ShortestPossibleCycle" => {
                            let value: Value = map.next_value()?;
                            shortest_possible_cycle =
                                value.get("$text").and_then(Value::as_u64).map(|x| x as u32);
                        }

                        _ => {
                            return Err(serde::de::Error::unknown_field(
                                key.to_string().as_str(),
                                &[
                                    "ResponseTimestamp",
                                    "RequestMessageRef",
                                    "SubscriberRef",
                                    "Status",
                                    "ValidUntil",
                                    "ShortestPossibleCycle",
                                ],
                            ));
                        }
                    }
                }

                Ok(XxxDelivery {
                    response_timestamp: response_timestamp.unwrap(),
                    request_message_ref: request_message_ref,
                    subscriber_ref: subscriber_ref,
                    subscription_ref: subscription_ref,
                    status: status,
                    valid_until: valid_until,
                    shortest_possible_cycle: shortest_possible_cycle,
                })
            }
        }
        deserializer.deserialize_map(XxxDeliveryVisitor)
    }
}
