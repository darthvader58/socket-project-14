# CSE 434 DHT Socket Project

This repository implements the September 27 milestone only: peer registration, DHT setup, ring ID assignment, 1950 storm-record distribution, peer counts, and completion signaling. October query, join, leave, and teardown features are not included.

## Programs

- `python3 manager.py PORT` starts the UDP manager.
- `python3 peer.py MANAGER_IP MANAGER_PORT` starts a peer command process.

The manager tracks registered peers and selects three peers for the ring. The leader assigns IDs, reads `data/details-1950.csv`, hashes each event to a peer, and forwards STORE messages around the ring. It gathers counts and reports `DHT_COMPLETE` after all records are accounted for.

## Peer commands

```text
register NAME IPv4 MANAGER_PORT PEER_PORT
setup-dht NAME SIZE YEAR
```

For this milestone, use `setup-dht NAME 3 1950`.

## Dataset

`data/details-1950.csv` is a 14-column adaptation of NOAA/NWS's public 1950 Storm Events details file. It is included because the named CSV was not found in the course Canvas Files or project module. Its source and field mapping are documented in `DATA_SOURCE.md`; this is a fallback data preparation, not an instruction explicitly stated by Canvas. Check with the instructor if the course intended a different copy or transformation.

## Run

Start the manager and three peers on at least two distinct end hosts. Use unique manager and peer ports from your assigned Socket Project group range. Canvas shows this submission is in Socket Project Group 14. The PDF assigns even group 14 the port range 8000-8499; this run uses ports 8000-8006. For the CloudLab test topology, the two private node addresses are `10.10.1.1` and `10.10.1.2`.
