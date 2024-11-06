use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, PartialEq, GoGenerate)]
#[serde(rename_all = "camelCase")]
enum PersonnelReason {
    Unknown,                   // Inconnu
    StaffSickness,             // Personnel Malade
    StaffAbsence,              // Personnel Absent
    StaffInWrongPlace,         // Personne Mal Positionné
    StaffShortage,             // Manque de Personnel
    IndustrialAction,          // Grève
    UndefinedPersonnelProblem, // Problème de Personnel Non Défini
}
