---
type: "ArcGIS Feature Layer"
title: "Pipelines"
description: "Pipelines in the North Sea in various phases."
resource: "NorthSea/NorthSea.gdb/Pipelines"
tags: ["arcgis", "filegdb", "polyline"]
generated: { by: "layers-json/0.3.1", at: "2026-09-14T14:58:34Z" }
table_name: "Pipelines"
stype: "Polyline"
display: "pipe_name"
subtype: "PipelinesType"
sources:
  - { id: "gdb", resource: "NorthSea/NorthSea.gdb", title: "File GDB NorthSea.gdb", last_modified: "2026-09-09T18:00:13Z" }
  - { id: "aprx", resource: "NorthSea/NorthSea.aprx", title: "ArcGIS project NorthSea.aprx", last_modified: "2026-09-13T12:08:15Z" }
---

Pipelines in the North Sea in various phases.

# Schema

| Column | Alias | Type | Sample values |
|---|---|---|---|
| `country` | country | String | `NO`, `UK`, `DK`, `NL` |
| `current_operator` | current operator | String | `GASSCO AS`, `EQUINOR ENERGY AS`, `CONOCOPHILLIPS SKANDINAVIA AS`, `AKER BP ASA`, `OKEA ASA`, `A/S NORSKE SHELL`, `VÅR ENERGI ASA`, `UNKNOWN` |
| `current_phase` | current phase | String | `IN SERVICE`, `DECOMMISSIONED`, `ABANDONED IN PLACE` |
| `dimension` | dimension | Double | `36.0`, `16.0`, `20.0`, `40.0`, `30.0`, `28.0`, `42.0`, `8.0`, `34.0`, `32.0`, `18.0`, `22.0`, `12.0`, `26.0`, `9.3`, `8.625`, `12.75`, `44.0`, `24.0`, `14.0` |
| `from_facility` | from facility | String | `SLEIPNER R`, `KOLLSNES`, `TROLL A`, `GJØA`, `STATFJORD B`, `HEIDRUN`, `HEIMDAL HRP`, `HULDRA`, `KÅRSTØ`, `DRAUPNER E`, `EKOFISK J`, `FRIGG TCP2`, `KVITEBJØRN`, `VALEMON`, `EDVARD GRIEG`, `JOHAN SVERDRUP RP`, `GUDRUN`, `36/22-BP`, `37/4-BP`, `ÅSGARD ERB` |
| `main_grouping` | main grouping | String | `Transportation` |
| `medium` | medium | String | `Gas`, `Oil`, `Condensate`, `Injection` |
| `pipe_name` | pipe name | String | `36" Gas TROLL A, KOLLSNES`, `34" Oil 36/22-BP, TEESSIDE`, `34" Oil 37/4-BP, 36/22-BP`, `42" Gas ÅSGARD ERB, KÅRSTØ`, `20" Gas TOGI, OSEBERG B`, `16" Oil GJØA, TOR II Y`, `26" Gas SKARV ERB, ÅSGARD T`, `36" Gas Disconnected, EKOFISK S`, `8" Condensate KOLLSNES, STURE`, `20" Oil ULA PP, EKOFISK J`, `9.3" Gas VESLEFRIKK A, STT-IN`, `40" Gas ZEEPIPE-SCP, ZEEBRUGGE`, `30" Gas STAT-SSTC, KÅRSTØ`, `16" Oil TROLL B, MONGSTAD`, `16" Gas NORNE ERB, NORNE/HEIDRUN T`, `36" Gas NORPIPE Y, B-11`, `20" Oil TROLL C, MONGSTAD`, `30" Gas STATFJORD B, STAT-SSTC`, `28" Oil OSEBERG A, STURE`, `40" Gas SLEIPNER R, ZEEPIPE-SCP` |
| `to_facility` | to facility | String | `KOLLSNES`, `MONGSTAD`, `KÅRSTØ`, `STURE`, `EMDEN`, `DRAUPNER S`, `NYHAMNA`, `TOR II Y`, `NORNE/HEIDRUN T`, `HEIMDAL HRP`, `SLEIPNER R`, `NORPIPE Y`, `SLEIPNER A`, `TEESSIDE`, `36/22-BP`, `OSEBERG B`, `ÅSGARD T`, `EKOFISK S`, `EKOFISK J`, `STT-IN` |
| `PipelinesType` | pipelines type | SmallInteger | `2`, `4`, `1`, `3`, `0` |

# Domains

## `country`

| Code | Value |
|---|---|
| `NO` | Norway |
| `UK` | United Kingdom |
| `DK` | Denmark |
| `NL` | Netherland |

## `PipelinesType`

| Code | Value |
|---|---|
| `1` | Condensate |
| `2` | Gas |
| `3` | Injection |
| `4` | Oil |
| `0` | Unknown |

# Query hints

## `country`

- Use 'country = 'NO'' for 'norway'.
- Use 'country = 'UK'' for 'united kingdom'.
- Use 'country = 'DK'' for 'denmark'.
- Use 'country = 'NL'' for 'netherland'.
- The country of the pipeline.
- NEVER use SQL LIKE in the WHERE clause for the values of the column country.

## `current_operator`

- The current operator
- Make sure to uppercase the compared values of the column current_operator in the where clause.
- For example: given the value >>gassco as<< becomes >>GASSCO AS<<

## `current_phase`

- The current phase of this pipeline
- Make sure to uppercase the compared values of the column current_phase in the where clause.
- For example: given the value >>in service<< becomes >>IN SERVICE<<

## `dimension`

- ALWAYS use SQL CAST AS DOUBLE PRECISION when comparing a value with the column dimension.
- Use 'dimension = cast(36.0 as DOUBLE PRECISION)' for 'dimension is 36.0'.

## `from_facility`

- The originating facility.
- Make sure to uppercase the compared values of the column from_facility in the where clause.
- For example: given the value >>sleipner r<< becomes >>SLEIPNER R<<

## `main_grouping`

- Make sure to use the SQL LIKE in the WHERE clause for the values of the column main_grouping.
- For example: given >>main grouping is transportation<< becomes >>main_grouping LIKE '%Transportation%'<<

## `medium`

- The content of the pipeline, like oil or gas
- Make sure to use the SQL LIKE in the WHERE clause for the values of the column medium.
- For example: given >>medium is gas<< becomes >>medium LIKE '%Gas%'<<

## `pipe_name`

- Make sure to use the SQL LIKE in the WHERE clause for the values of the column pipe_name.
- For example: given >>pipe name is 36"<< becomes >>pipe_name LIKE '%36"%'<<

## `to_facility`

- The destination facility
- Make sure to uppercase the compared values of the column to_facility in the where clause.
- For example: given the value >>kollsnes<< becomes >>KOLLSNES<<

## `PipelinesType`

- Use 'PipelinesType = cast(1 as SMALLINT)' for 'condensate'.
- Use 'PipelinesType = cast(2 as SMALLINT)' for 'gas'.
- Use 'PipelinesType = cast(3 as SMALLINT)' for 'injection'.
- Use 'PipelinesType = cast(4 as SMALLINT)' for 'oil'.
- Use 'PipelinesType = cast(0 as SMALLINT)' for 'unknown'.
- ALWAYS use SQL CAST AS SMALLINT when comparing a value with the column PipelinesType.

Field names, types, domains and sampled values come from the File GDB;[^gdb] layer name, aliases and hidden fields come from the map layer.[^aprx]

[^gdb]: File GDB
[^aprx]: ArcGIS project
