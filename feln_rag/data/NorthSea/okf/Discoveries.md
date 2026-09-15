---
type: "ArcGIS Feature Layer"
title: "Discoveries"
description: "Discover fields with various hydrocarbon content."
resource: "NorthSea/NorthSea.gdb/Discoveries"
tags: ["arcgis", "filegdb", "polygon"]
generated: { by: "layers-json/0.3.1", at: "2026-09-14T14:58:34Z" }
table_name: "Discoveries"
stype: "Polygon"
display: "discovery_name"
subtype: "discovery_type"
sources:
  - { id: "gdb", resource: "NorthSea/NorthSea.gdb", title: "File GDB NorthSea.gdb", last_modified: "2026-09-09T18:00:13Z" }
  - { id: "aprx", resource: "NorthSea/NorthSea.aprx", title: "ArcGIS project NorthSea.aprx", last_modified: "2026-09-13T12:08:15Z" }
---

Discover fields with various hydrocarbon content.

# Schema

| Column | Alias | Type | Sample values |
|---|---|---|---|
| `discovery_name` | discovery name | String | `7220/8-2 S (Snøfonn Nord)`, `6506/11-10 Berling`, `7122/7-1 Goliat`, `34/7-23 S`, `31/6-1 (Troll Øst)`, `16/1-8 Edvard Grieg`, `34/8-1 Visund`, `34/7-8 Vigdis`, `7120/12-2 (Alke Sør)`, `35/11-24 S (Swisher)`, `Markham`, `7220/7-4 (Isflak)`, `7122/8-1 S (Countach)`, `6406/2-6 Ragnfrid`, `2/8-19 (Overly)`, `7228/7-1 (Pandora)`, `7122/9-1 (Lupa)`, `34/4-10 (Beta Brent)`, `34/4-1 Snorre`, `35/3-2 Agat` |
| `discovery_type` | discovery type | Integer | `1`, `3`, `4`, `2`, `5`, `-1` |
| `included_in_field` | included in field | String | `YES`, `NO` |
| `included_in_discovery_name` | included in discovery name | String | `34/10-2 Gullfaks Sør`, `30/9-3 Oseberg Sør`, `7220/8-1 Johan Castberg`, `30/11-8 S Munin`, `7121/4-1 Snøhvit`, `30/6-1 Oseberg`, `35/11-4 Fram`, `6507/11-1 Midgard`, `24/6-2 Alvheim`, `34/7-8 Vigdis`, `31/4-3 Brage`, `34/7-12 Tordis`, `6507/11-6 Halten Øst`, `25/11-1 Balder`, `6707/10-1 Aasta Hansteen`, `34/8-1 Visund`, `34/10-1 Gullfaks`, `6608/10-6 Svale`, `6507/5-1 Skarv`, `25/2-10 S Hugin` |
| `field_label` | field label | String | `GULLFAKS SØR`, `OSEBERG SØR`, `JOHAN CASTBERG`, `OSEBERG`, `MUNIN`, `SNØHVIT`, `FRAM`, `VIGDIS`, `GOLIAT`, `ÅSGARD`, `VISUND`, `ALVHEIM`, `BRAGE`, `TORDIS`, `HALTEN ØST`, `BERLING`, `BALDER`, `SKARV`, `GULLFAKS`, `AASTA HANSTEEN` |
| `discovery_hc_type` | discovery hydrocarbon type | String | `GAS`, `OIL`, `OIL/GAS`, `GAS/CONDENSATE`, `CONDENSATE` |
| `source` | source | String | `NPD`, `NLOG`, `OGA`, `DEA`, `DECC` |
| `field_name` | field name | String | `GULLFAKS SØR`, `OSEBERG SØR`, `JOHAN CASTBERG`, `OSEBERG`, `MUNIN`, `SNØHVIT`, `FRAM`, `VIGDIS`, `GOLIAT`, `ÅSGARD`, `VISUND`, `ALVHEIM`, `BRAGE`, `TORDIS`, `HALTEN ØST`, `BERLING`, `BALDER`, `SKARV`, `GULLFAKS`, `AASTA HANSTEEN` |
| `field_hc_type` | field hydrocarbon type | String | `GAS`, `OIL`, `OIL/GAS`, `GAS/CONDENSATE`, `CONDENSATE`, `OIL/CONDENSATE` |
| `field_current_activity_status` | field current activity status | String | `UNKNOWN`, `PRODUCING`, `PRODUCTION CEASED`, `APPROVED FOR PRODUCT`, `SHUT DOWN`, `POST-COP`, `PRODUCTION SUSPENDED - POSSIBLE RESERVES REMAIN`, `CONSTRUCTION-FDP APPROV`, `PRODUCTION CEASED - VENT CONSENT NEEDED`, `UNDER APPRAIS - NO FDP`, `UNDER APPRAI-FUTURE FDP`, `NO APPRAISAL`, `PRODUCTION SUSPENDED`, `SHELVED` |
| `discovery_current_activity_sta` | discovery current activity status | String | `PRODUCING`, `INCLUDED IN OTHER DISCOVERY`, `PRODUCTION IS UNLIKELY`, `PRODUCTION CEASED`, `PRODUCTION LIKELY BUT UNCLARIFIED`, `POST-COP`, `PRODUCTION NOT EVALUATED`, `SHUT DOWN`, `APPROVED FOR PRODUCTION`, `PRODUCTION SUSPENDED - POSSIBLE RESERVES`, `PRODUCTION IN CLARIFICATION PHASE`, `CONSTRUCTION-FDP APPROV`, `PRODUCTION CEASED - VENT CONSENT NEEDED`, `UNDER APPRAIS - NO FDP`, `UNDER APPRAI-FUTURE FDP`, `NO APPRAISAL`, `PRODUCTION SUSPENDED`, `SHELVED` |
| `discovery_wellbore_name` | discovery wellbore name | String | `42/30- 2`, `22/05B- 2`, `21/30- 6A`, `98/07- 2`, `22/30A- 5`, `110/15- 6`, `3/04- 4`, `21/24- 3`, `211/13- 2`, `21/24- 1`, `16/03B- 8Z`, `49/29- 2`, `110/13B- 19`, `22/29- 2Z`, `211/19- 6`, `21/30-12`, `29/02A- 6`, `48/07B- 8`, `16/03A- 1`, `3/15- 2` |
| `country` | country | String | `NO`, `NL`, `UK`, `DK` |

# Domains

## `discovery_type`

| Code | Value |
|---|---|
| `-1` | Unknown |
| `1` | Gas |
| `2` | Gas/Condensate |
| `3` | Oil |
| `4` | Oil/Gas |
| `5` | Condensate |

## `source`

| Code | Value |
|---|---|
| `NPD` | Norwegian Petroleum Directorate |
| `DECC` | Department of Energy & Climate Change |
| `DEA` | Danish Energy Agency |
| `NLOG` | NL Oil and GAS Portal |

## `country`

| Code | Value |
|---|---|
| `NO` | Norway |
| `UK` | United Kingdom |
| `DK` | Denmark |
| `NL` | Netherland |

# Query hints

## `discovery_name`

- Make sure to use the SQL LIKE in the WHERE clause for the values of the column discovery_name.
- For example: given >>discovery name is 7220/8-2<< becomes >>discovery_name LIKE '%7220/8-2%'<<

## `discovery_type`

- Use 'discovery_type = cast(-1 as INTEGER)' for 'unknown'.
- Use 'discovery_type = cast(1 as INTEGER)' for 'gas'.
- Use 'discovery_type = cast(2 as INTEGER)' for 'gas or condensate'.
- Use 'discovery_type = cast(3 as INTEGER)' for 'oil'.
- Use 'discovery_type = cast(4 as INTEGER)' for 'oil or gas'.
- Use 'discovery_type = cast(5 as INTEGER)' for 'condensate'.
- ALWAYS use SQL CAST AS INTEGER when comparing a value with the column discovery_type.

## `included_in_field`

- Make sure to uppercase the compared values of the column included_in_field in the where clause.
- For example: given the value >>yes<< becomes >>YES<<

## `included_in_discovery_name`

- Make sure to use the SQL LIKE in the WHERE clause for the values of the column included_in_discovery_name.
- For example: given >>included in discovery name is 34/10-2<< becomes >>included_in_discovery_name LIKE '%34/10-2%'<<

## `field_label`

- Make sure to uppercase the compared values of the column field_label in the where clause.
- For example: given the value >>gullfaks sør<< becomes >>GULLFAKS SØR<<

## `discovery_hc_type`

- Make sure to uppercase the compared values of the column discovery_hc_type in the where clause.
- For example: given the value >>gas<< becomes >>GAS<<

## `source`

- Use 'source = 'NPD'' for 'norwegian petroleum directorate'.
- Use 'source = 'DECC'' for 'department of energy & climate change'.
- Use 'source = 'DEA'' for 'danish energy agency'.
- Use 'source = 'NLOG'' for 'nl oil and gas portal'.
- NEVER use SQL LIKE in the WHERE clause for the values of the column source.

## `field_name`

- Make sure to uppercase the compared values of the column field_name in the where clause.
- For example: given the value >>gullfaks sør<< becomes >>GULLFAKS SØR<<

## `field_hc_type`

- Make sure to uppercase the compared values of the column field_hc_type in the where clause.
- For example: given the value >>gas<< becomes >>GAS<<

## `field_current_activity_status`

- Make sure to uppercase the compared values of the column field_current_activity_status in the where clause.
- For example: given the value >>unknown<< becomes >>UNKNOWN<<

## `discovery_current_activity_sta`

- Make sure to uppercase the compared values of the column discovery_current_activity_sta in the where clause.
- For example: given the value >>producing<< becomes >>PRODUCING<<

## `discovery_wellbore_name`

- Make sure to use the SQL LIKE in the WHERE clause for the values of the column discovery_wellbore_name.
- For example: given >>discovery wellbore name is 42/30-<< becomes >>discovery_wellbore_name LIKE '%42/30-%'<<

## `country`

- Use 'country = 'NO'' for 'norway'.
- Use 'country = 'UK'' for 'united kingdom'.
- Use 'country = 'DK'' for 'denmark'.
- Use 'country = 'NL'' for 'netherland'.
- NEVER use SQL LIKE in the WHERE clause for the values of the column country.

Field names, types, domains and sampled values come from the File GDB;[^gdb] layer name, aliases and hidden fields come from the map layer.[^aprx]

[^gdb]: File GDB
[^aprx]: ArcGIS project
