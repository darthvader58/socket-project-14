# CSE 434 DHT Socket Project

Milestone programs:

- `manager.py PORT`
- `peer.py MANAGER_IP MANAGER_PORT`

The manager handles registration and DHT state. Peers form the logical ring and distribute the storm records with UDP.

## Commands

```text
register NAME IP MANAGER_PORT PEER_PORT
setup-dht NAME SIZE YEAR
```

Place the course-provided `details-1950.csv` file in `data/` before running the milestone.
