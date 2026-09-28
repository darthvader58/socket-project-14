# 1950 Storm Dataset Provenance

The project PDF specifies a file named `details-YYYY.csv`, a 14-field record layout, and a milestone run with `YYYY = 1950` (PDF pages 4-5 and 8). Canvas Files search for `1950` and the Socket Programming Project module did not contain `details-1950.csv` when checked on September 27, 2026.

This project therefore uses a transparent fallback: the NOAA/NWS bulk 1950 Event Details CSV, downloaded from:

`https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/StormEvents_details-ftp_v1.0_d1950_c20260323.csv.gz`

The source archive file has 51 columns. `data/details-1950.csv` is produced by selecting these 14 columns, in the exact order used by `dht.py` and the assignment's description:

1. `EVENT_ID` -> `event_id`
2. `STATE` -> `state`
3. `YEAR` -> `year`
4. `MONTH_NAME` -> `month_name`
5. `EVENT_TYPE` -> `event_type`
6. `CZ_TYPE` -> `cz_type`
7. `CZ_NAME` -> `cz_name`
8. `INJURIES_DIRECT` -> `injuries_direct`
9. `INJURIES_INDIRECT` -> `injuries_indirect`
10. `DEATHS_DIRECT` -> `deaths_direct`
11. `DEATHS_INDIRECT` -> `deaths_indirect`
12. `DAMAGE_PROPERTY` -> `damage_property`
13. `DAMAGE_CROPS` -> `damage_crops`
14. `TOR_F_SCALE` -> `tor_f_scale`

The first row is a header. The extracted file contains 223 storm records plus that header. Hashing those records with the PDF's rule gives table size 449 and counts by ring ID 0, 1, 2 of 72, 75, and 76 in the verified CloudLab run.

**Important:** The assignment says the data is provided by NWS and describes its required format, but does not explicitly instruct students to derive a missing course file from NOAA's bulk archive. The NOAA conversion is a reasonable source-backed fallback, not a verified Canvas instruction or instructor approval. If time permits, ask the instructor/TA whether this exact source/version and field projection is acceptable; do not describe it as a course-provided file.
