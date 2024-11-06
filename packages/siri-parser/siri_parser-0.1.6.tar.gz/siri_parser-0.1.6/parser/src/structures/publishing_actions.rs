use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

use super::{notify_by_email_action::NotifyByEmailAction, notify_by_sms_action::NotifyBySmsAction, publish_to_display_action::PublishToDisplayAction, publish_to_mobile_action::PublishToMobileAction, publish_to_web_action::PublishToWebAction};


#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct PublishingActions {
    publish_to_web_action: Option<PublishToWebAction>,
    publish_to_mobile_action: Option<PublishToMobileAction>,
    publish_to_display_action: Option<PublishToDisplayAction>,
    notify_by_email_action: Option<NotifyByEmailAction>,
    notify_by_sms_action: Option<NotifyBySmsAction>,
}