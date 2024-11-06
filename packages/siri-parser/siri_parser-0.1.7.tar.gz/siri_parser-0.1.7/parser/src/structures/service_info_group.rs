use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use crate::enums::vehicule_feature::VehicleFeature;


#[derive(Debug, Default, Clone, Serialize, Deserialize, PartialEq, GoGenerate, Eq)]
#[serde(rename_all = "PascalCase")]
pub struct ServiceInfoGroup {
    operator_ref: Option<String>,         // OperatorCode
    product_category_ref: Option<String>, // ProductCategoryCode
    service_feature_ref: Vec<String>,     // Vec<ServiceFeatureCode>
    vehicle_feature_ref: Vec<VehicleFeature>,     // Vec<VehicleFeatureCode>
}