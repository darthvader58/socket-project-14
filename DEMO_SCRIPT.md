# Milestone Video Checklist

The assignment requires a YouTube video no longer than 7 minutes, unedited, with audio, recorded before the deadline. This project has not been recorded as a video.

## Suggested single-take outline

1. **0:00-0:35:** State the milestone scope and show the two distinct CloudLab end hosts in the CloudLab experiment list.
2. **0:35-1:15:** On both nodes, show the source folder and run `python3 -m py_compile manager.py peer.py protocol.py dht.py` (or the equivalent compile check). Explain Python executes source directly.
3. **1:15-2:00:** Show the manager on node0 and the three peer processes across node0/node1, with each register command and SUCCESS response.
4. **2:00-3:30:** On PeerA, issue `setup-dht PeerA 3 1950`. Keep the manager and peer windows visible; show ring IDs, the 223 record input, and record distribution.
5. **3:30-4:15:** Show counts by peer ID (72, 75, 76; sum 223) and manager `DHT_COMPLETE SUCCESS`.
6. **4:15-4:45:** Briefly show the design PDF and Git history if time permits.

Use readable terminal fonts and keep the capture continuous. Do not edit or splice the recording. The exact public YouTube URL and actual timestamps must be added to the design PDF after the video is uploaded. Do not invent timestamps before recording.

## Current CloudLab result

The successful process output is recorded in `MILESTONE_TEST.md`. That text log is supporting evidence only and does not replace the required video.
