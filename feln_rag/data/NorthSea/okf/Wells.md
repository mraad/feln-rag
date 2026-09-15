---
type: "ArcGIS Feature Layer"
title: "Wells"
description: "Oil and gas wells in the north sea."
resource: "NorthSea/NorthSea.gdb/Wellbores"
tags: ["arcgis", "filegdb", "point"]
generated: { by: "layers-json/0.3.1", at: "2026-09-14T14:58:34Z" }
table_name: "Wells"
stype: "Point"
display: "well_name"
subtype: "content_type"
sources:
  - { id: "gdb", resource: "NorthSea/NorthSea.gdb", title: "File GDB NorthSea.gdb", last_modified: "2026-09-09T18:00:13Z" }
  - { id: "aprx", resource: "NorthSea/NorthSea.aprx", title: "ArcGIS project NorthSea.aprx", last_modified: "2026-09-13T12:08:15Z" }
---

Oil and gas wells in the north sea.

# Schema

| Column | Alias | Type | Sample values |
|---|---|---|---|
| `well_name` | well name | String | `22/02b- 14`, `22/14b- 6`, `9/23a- 29`, `22/02b- 13`, `21/23a- 9`, `213/25c- 1`, `21/10- 10`, `25/1-7`, `25/1-8`, `15/9-19`, `34/10-33`, `29/05b-F10`, `43/25a- 2`, `15/29a- 15`, `16/29a- 16`, `9/14a- 8`, `34/8-14`, `9/18a- 33`, `36/7-5`, `31/2-17` |
| `wellbore_name` | wellbore name | String | `M-1X`, `GERT-1`, `7120/7-1`, `1/3-3`, `25/5-1`, `34/10-37`, `6406/2-1`, `6407/7-7 S`, `25/8-17`, `6406/9-3`, `7325/1-1`, `7324/9-1`, `7319/12-1`, `7220/2-1`, `35/11-27 S`, `6507/3-15`, `36/7-5 B`, `6605/1-2 S`, `30/6-C-2 A`, `K03-01` |
| `purpose` | purpose | String | `EXPLORATION`, `APPRAISAL`, `HYDROCARBON EXPLORATION`, `WILDCAT`, `PRODUCTION`, `UNKNOWN`, `INJECTION`, `STORAGE`, `APPRAISAL-CCS`, `OTHER`, `DISPOSAL`, `WILDCAT-CCS` |
| `content` | content | String | `DRY`, `OIL`, `GAS`, `NOT AVAILABLE`, `OIL/GAS`, `OIL SHOW`, `NOT APPLICABLE`, `GAS/CONDENSATE`, `GAS SHOWS`, `SHOWS`, `OIL/GAS SHOWS`, `OIL SHOWS`, `CONDENSATE/GAS SHOWS`, `OIL/GAS/CONDENSATE`, `GAS/SHOWS`, `GAS/OIL SHOWS`, `CONDENSATE/OIL SHOWS`, `OIL/CONDENSATE SHOWS`, `WATER`, `OIL/CONDENSATE` |
| `field_name` | field name | String | `TROLL`, `OSEBERG`, `BALDER`, `GULLFAKS`, `GULLFAKS SØR`, `JOHAN SVERDRUP`, `ÅSGARD`, `SNØHVIT`, `OSEBERG SØR`, `FRIGG`, `VISUND`, `VIGDIS`, `SLEIPNER VEST`, `IVAR AASEN`, `SNORRE`, `HEIDRUN`, `HUGIN`, `ALVHEIM`, `MUNIN`, `KRISTIN` |
| `multilateral` | multilateral | String | `NO` |
| `entry_date` | entry date | Date | `1991-04-15 00:00:00`, `1985-10-18 00:00:00`, `2007-10-08 00:00:00`, `2009-10-17 00:00:00`, `1990-10-12 00:00:00`, `1991-06-06 00:00:00`, `1982-01-09 00:00:00`, `1973-12-25 00:00:00`, `1997-01-29 00:00:00`, `1983-03-16 00:00:00`, `1975-05-09 00:00:00`, `1985-11-21 00:00:00`, `1977-10-06 00:00:00`, `1988-09-03 00:00:00`, `1989-09-26 00:00:00`, `1989-12-22 00:00:00`, `1981-04-10 00:00:00`, `1987-08-18 00:00:00`, `1985-12-02 00:00:00`, `1987-11-22 00:00:00` |
| `completion_date` | completion date | Date | `1990-05-07 00:00:00`, `1988-10-22 00:00:00`, `1981-11-07 00:00:00`, `1997-04-05 00:00:00`, `1989-03-28 00:00:00`, `2002-12-13 00:00:00`, `2009-10-17 00:00:00`, `1991-09-27 00:00:00`, `1977-10-03 00:00:00`, `1984-06-07 00:00:00`, `1992-06-19 00:00:00`, `1988-09-14 00:00:00`, `1991-04-14 00:00:00`, `1978-08-16 00:00:00`, `2001-01-08 00:00:00`, `1982-06-27 00:00:00`, `1976-11-09 00:00:00`, `2000-05-23 00:00:00`, `1988-02-25 00:00:00`, `1988-05-15 00:00:00` |
| `status` | status | String | `ABANDONED PHASE 3`, `P&A`, `ABANDONED PHASE 1`, `ABANDONED PHASE 2`, `SUSPENDED`, `PLUGGED`, `JUNKED`, `RE-CLASS TO DEV`, `COMPLETED (SHUT IN)`, `COMPLETED (OPERATING)`, `WILL NEVER BE DRILLED`, `DRILLING`, `RE-CLASS TO TEST`, `BLOWOUT`, `PREDRILLED` |
| `water_depth` | water depth in meters | Double | `110.0`, `92.964`, `70.0`, `32.004`, `69.0`, `90.5256`, `71.0`, `66.0`, `121.0`, `120.0`, `68.0`, `72.0`, `106.0`, `111.0`, `89.916`, `113.0`, `146.304`, `127.0`, `112.0`, `105.0` |
| `production_facility` | production facility | String | `VARG A`, `MARTIN LINGE A`, `VALEMON`, `FENJA G`, `ORMEN LANGE C`, `BRAGE`, `FOSSEKALL R`, `VIGDIS E`, `ÅSGARD NB` |
| `source` | source | String | `OGA`, `NPD`, `NLOG`, `DEA/GEUS`, `DEA`, `DECC` |
| `well_type` | well type | String | `EXPLORATION` |
| `discovery_wellbore` | discovery wellbore | String | `NO`, `YES` |
| `drilling_operator` | drilling operator | String | `Unknown`, `No Data Available`, `Den Norske Stats Oljeselskap A.S`, `Chrysaor Production (U.K.) Limited`, `Norsk Hydro Produksjon As`, `Perenco Uk Limited`, `Bp Exploration Operating Company Limited`, `Repsol Resources Uk Limited`, `Apache Beryl I Limited`, `Shell U.K. Limited`, `Cnooc Petroleum Europe Limited`, `Cnr International (U.K.) Limited`, `Taqa Bratani Limited`, `Statoil Petroleum As`, `Totalenergies E&P Uk Limited`, `Saga Petroleum Asa`, `Spirit Energy Resources Limited`, `Totalenergies E&P North Sea Uk Limited`, `Equinor Energy As`, `Premier Oil Uk Limited` |
| `drilling_facility` | drilling facility | String | `Unknown`, `Deepsea Bergen`, `Transocean Arctic`, `Treasure Saga`, `Polar Pioneer`, `Bredford Dolphin`, `West Vanguard`, `Deepsea Stavanger`, `Ocean Vanguard`, `Borgland Dolphin`, `West Alpha`, `Byford Dolphin`, `Vildkat Explorer`, `Ross Isle`, `Leiv Eiriksson`, `Transocean Leader`, `Transocean Winner`, `Scarabeo 8`, `Nortrym`, `West Hercules` |
| `production_licence` | production licence | String | `01/62`, `050`, `018`, `089`, `053`, `01/35`, `054`, `120`, `128`, `006`, `046`, `104`, `037`, `090`, `001`, `085`, `038`, `501`, `265`, `052` |
| `country` | country | String | `UK`, `NO`, `NL`, `DK` |
| `formation_tops` | formation tops | SmallInteger | `1`, `0` |
| `geochem_info` | geochem info | SmallInteger | `0`, `1` |
| `log` | log | SmallInteger | `1`, `0` |
| `mud` | mud | SmallInteger | `1`, `0` |
| `oil_samples` | oil samples | SmallInteger | `0`, `1` |
| `old_wdss` | old wdss | SmallInteger | `0`, `1` |
| `paly_slides` | paly slides | SmallInteger | `0`, `1` |
| `wellbore_history` | wellbore history | SmallInteger | `1`, `0` |
| `npd_papers` | npd papers | SmallInteger | `0`, `1` |
| `cuttings_sample` | cuttings sample | String | `YES`, `NO` |
| `core_sample` | core sample | String | `YES`, `NO` |
| `doc_by_licensee` | doc by licensee | SmallInteger | `1`, `0` |
| `CountryName` | countryname | String | `United Kingdom`, `Norway`, `Netherland`, `Denmark` |
| `content_type` | content type | SmallInteger | `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `16`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `17` |

# Domains

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

## `content_type`

| Code | Value |
|---|---|
| `0` | DRY |
| `1` | OIL |
| `2` | GAS |
| `3` | NOT AVAILABLE |
| `4` | OIL SHOWS |
| `5` | OIL/GAS |
| `6` | NOT APPLICABLE |
| `7` | GAS/CONDENSATE |
| `8` | GAS SHOWS |
| `9` | SHOWS |
| `10` | OIL/GAS SHOWS |
| `11` | GAS/CONDENSATE SHOWS |
| `12` | OIL/CONDENSATE SHOWS |
| `13` | OIL/GAS/CONDENSATE |
| `14` | WATER |
| `15` | OIL/CONDENSATE |
| `16` | UNKNOWN |
| `17` | SALT |

# Query hints

## `well_name`

- The name of the well
- Make sure to use the SQL LIKE in the WHERE clause for the values of the column well_name.
- For example: given >>well name is 22/02b-<< becomes >>well_name LIKE '%22/02b-%'<<

## `wellbore_name`

- Make sure to use the SQL LIKE in the WHERE clause for the values of the column wellbore_name.
- For example: given >>wellbore name is m-1x<< becomes >>wellbore_name LIKE '%M-1X%'<<

## `purpose`

- Make sure to uppercase the compared values of the column purpose in the where clause.
- For example: given the value >>exploration<< becomes >>EXPLORATION<<

## `content`

- Make sure to uppercase the compared values of the column content in the where clause.
- For example: given the value >>dry<< becomes >>DRY<<

## `field_name`

- The name of the field
- Make sure to uppercase the compared values of the column field_name in the where clause.
- For example: given the value >>troll<< becomes >>TROLL<<

## `multilateral`

- Make sure to uppercase the compared values of the column multilateral in the where clause.
- For example: given the value >>no<< becomes >>NO<<

## `status`

- Make sure to uppercase the compared values of the column status in the where clause.
- For example: given the value >>abandoned phase 3<< becomes >>ABANDONED PHASE 3<<

## `water_depth`

- Depth of the well in meters
- ALWAYS use SQL CAST AS DOUBLE PRECISION when comparing a value with the column water_depth.
- Use 'water_depth = cast(110.0 as DOUBLE PRECISION)' for 'water depth in meters is 110.0'.

## `production_facility`

- Make sure to uppercase the compared values of the column production_facility in the where clause.
- For example: given the value >>varg a<< becomes >>VARG A<<

## `source`

- Use 'source = 'NPD'' for 'norwegian petroleum directorate'.
- Use 'source = 'DECC'' for 'department of energy & climate change'.
- Use 'source = 'DEA'' for 'danish energy agency'.
- Use 'source = 'NLOG'' for 'nl oil and gas portal'.
- NEVER use SQL LIKE in the WHERE clause for the values of the column source.

## `well_type`

- Make sure to uppercase the compared values of the column well_type in the where clause.
- For example: given the value >>exploration<< becomes >>EXPLORATION<<

## `discovery_wellbore`

- Make sure to uppercase the compared values of the column discovery_wellbore in the where clause.
- For example: given the value >>no<< becomes >>NO<<

## `drilling_operator`

- Make sure to use the SQL LIKE in the WHERE clause for the values of the column drilling_operator.
- For example: given >>drilling operator is unknown<< becomes >>drilling_operator LIKE '%Unknown%'<<

## `drilling_facility`

- Make sure to use the SQL LIKE in the WHERE clause for the values of the column drilling_facility.
- For example: given >>drilling facility is unknown<< becomes >>drilling_facility LIKE '%Unknown%'<<

## `production_licence`

- Make sure to use the SQL LIKE in the WHERE clause for the values of the column production_licence.
- For example: given >>production licence is 01/62<< becomes >>production_licence LIKE '%01/62%'<<

## `country`

- Use 'country = 'NO'' for 'norway'.
- Use 'country = 'UK'' for 'united kingdom'.
- Use 'country = 'DK'' for 'denmark'.
- Use 'country = 'NL'' for 'netherland'.
- The country where the well is located
- NEVER use SQL LIKE in the WHERE clause for the values of the column country.

## `formation_tops`

- ALWAYS use SQL CAST AS SMALLINT when comparing a value with the column formation_tops.
- Use 'formation_tops = cast(1 as SMALLINT)' for 'formation tops is 1'.

## `geochem_info`

- ALWAYS use SQL CAST AS SMALLINT when comparing a value with the column geochem_info.
- Use 'geochem_info = cast(0 as SMALLINT)' for 'geochem info is 0'.

## `log`

- ALWAYS use SQL CAST AS SMALLINT when comparing a value with the column log.
- Use 'log = cast(1 as SMALLINT)' for 'log is 1'.

## `mud`

- ALWAYS use SQL CAST AS SMALLINT when comparing a value with the column mud.
- Use 'mud = cast(1 as SMALLINT)' for 'mud is 1'.

## `oil_samples`

- ALWAYS use SQL CAST AS SMALLINT when comparing a value with the column oil_samples.
- Use 'oil_samples = cast(0 as SMALLINT)' for 'oil samples is 0'.

## `old_wdss`

- ALWAYS use SQL CAST AS SMALLINT when comparing a value with the column old_wdss.
- Use 'old_wdss = cast(0 as SMALLINT)' for 'old wdss is 0'.

## `paly_slides`

- ALWAYS use SQL CAST AS SMALLINT when comparing a value with the column paly_slides.
- Use 'paly_slides = cast(0 as SMALLINT)' for 'paly slides is 0'.

## `wellbore_history`

- ALWAYS use SQL CAST AS SMALLINT when comparing a value with the column wellbore_history.
- Use 'wellbore_history = cast(1 as SMALLINT)' for 'wellbore history is 1'.

## `npd_papers`

- ALWAYS use SQL CAST AS SMALLINT when comparing a value with the column npd_papers.
- Use 'npd_papers = cast(0 as SMALLINT)' for 'npd papers is 0'.

## `cuttings_sample`

- Make sure to uppercase the compared values of the column cuttings_sample in the where clause.
- For example: given the value >>yes<< becomes >>YES<<

## `core_sample`

- Make sure to uppercase the compared values of the column core_sample in the where clause.
- For example: given the value >>yes<< becomes >>YES<<

## `doc_by_licensee`

- ALWAYS use SQL CAST AS SMALLINT when comparing a value with the column doc_by_licensee.
- Use 'doc_by_licensee = cast(1 as SMALLINT)' for 'doc by licensee is 1'.

## `CountryName`

- Make sure to use the SQL LIKE in the WHERE clause for the values of the column CountryName.
- For example: given >>countryname is united<< becomes >>CountryName LIKE '%United%'<<

## `content_type`

- Use 'content_type = cast(0 as SMALLINT)' for 'dry'.
- Use 'content_type = cast(1 as SMALLINT)' for 'oil'.
- Use 'content_type = cast(2 as SMALLINT)' for 'gas'.
- Use 'content_type = cast(3 as SMALLINT)' for 'not available'.
- Use 'content_type = cast(4 as SMALLINT)' for 'oil shows'.
- Use 'content_type = cast(5 as SMALLINT)' for 'oil or gas'.
- Use 'content_type = cast(6 as SMALLINT)' for 'not applicable'.
- Use 'content_type = cast(7 as SMALLINT)' for 'gas or condensate'.
- Use 'content_type = cast(8 as SMALLINT)' for 'gas shows'.
- Use 'content_type = cast(9 as SMALLINT)' for 'shows'.
- Use 'content_type = cast(10 as SMALLINT)' for 'oil or gas shows'.
- Use 'content_type = cast(11 as SMALLINT)' for 'gas or condensate shows'.
- Use 'content_type = cast(12 as SMALLINT)' for 'oil or condensate shows'.
- Use 'content_type = cast(13 as SMALLINT)' for 'oil or gas or condensate'.
- Use 'content_type = cast(14 as SMALLINT)' for 'water'.
- Use 'content_type = cast(15 as SMALLINT)' for 'oil or condensate'.
- Use 'content_type = cast(16 as SMALLINT)' for 'unknown'.
- Use 'content_type = cast(17 as SMALLINT)' for 'salt'.
- ALWAYS use SQL CAST AS SMALLINT when comparing a value with the column content_type.

Field names, types, domains and sampled values come from the File GDB;[^gdb] layer name, aliases and hidden fields come from the map layer.[^aprx]

[^gdb]: File GDB
[^aprx]: ArcGIS project
