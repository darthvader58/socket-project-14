# Milestone Test Record

Tested on September 27, 2026 on two CloudLab end hosts in the `sraj28-dht-m1` experiment:

- Node 0 `ms1027.utah.cloudlab.us` (private interface `10.10.1.1`): manager and PeerA.
- Node 1 `ms0624.utah.cloudlab.us` (private interface `10.10.1.2`): PeerB and PeerC.
- Manager port: 8000. Peer manager/peer ports: PeerA 8001/8002, PeerB 8003/8004, PeerC 8005/8006.
- Canvas shows Socket Project Group 14. Under the PDF's even-group rule, group 14's range is 8000-8499; these ports are within that assigned range.

Verified output:

```text
PeerA: [REGISTER] SUCCESS
PeerB: [REGISTER] SUCCESS
PeerC: [REGISTER] SUCCESS
PeerA: [SETUP] SUCCESS
PeerA: [RING] PeerA -> ID 0
PeerC: [RING] PeerC -> ID 1
PeerB: [RING] PeerB -> ID 2
[DATA] 223 records, table size 449
[DATA] Record distribution complete
[COUNT] {'1': 75, '2': 76, '0': 72}
[DHT_COMPLETE] SUCCESS
```

Manager log confirmed all three registrations, setup, counts, and completion. The peer processes and manager ran as CloudLab processes, not a local-only simulation.

This is a test log, not the required video. The assignment's video still must be a continuous, unedited recording with audio, no longer than 7 minutes, demonstrating compilation, the two end hosts, all three registrations, setup with 1950 data, counts, and completion.
