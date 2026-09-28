import random
import socket
import sys

from protocol import BUFFER_SIZE, decode, encode, make_response

PORT_MIN = 8000
PORT_MAX = 8499


class Manager:
    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", port))
        self.peers = {}
        self.phase = "IDLE"
        self.leader = None
        self.members = []

    def send_response(self, request, addr, status, payload=None):
        self.sock.sendto(encode(make_response(request, status, payload)), addr)

    def valid_port(self, port):
        return PORT_MIN <= int(port) <= PORT_MAX

    def register(self, request, addr):
        payload = request.get("payload", {})
        name = request.get("sender", "")
        ip = payload.get("ip", "")
        m_port = payload.get("m_port")
        p_port = payload.get("p_port")
        if not name.isalpha() or len(name) > 15:
            return "FAILURE", {"reason": "invalid name"}
        if name in self.peers:
            return "FAILURE", {"reason": "duplicate name"}
        try:
            m_port = int(m_port)
            p_port = int(p_port)
        except (TypeError, ValueError):
            return "FAILURE", {"reason": "invalid port"}
        if not self.valid_port(m_port) or not self.valid_port(p_port) or m_port == p_port:
            return "FAILURE", {"reason": "port outside group range"}
        for peer in self.peers.values():
            if peer["ip"] == ip and {peer["m_port"], peer["p_port"]} & {m_port, p_port}:
                return "FAILURE", {"reason": "port conflict"}
        self.peers[name] = {
            "name": name, "ip": ip, "m_port": m_port, "p_port": p_port,
            "manager_addr": addr, "state": "Free",
        }
        print(f"[REGISTER] {name} -> SUCCESS", flush=True)
        return "SUCCESS", {}

    def setup(self, request, addr):
        if self.phase != "IDLE":
            return "FAILURE", {"reason": "manager busy"}
        payload = request.get("payload", {})
        leader_name = request.get("sender", "")
        try:
            size = int(payload.get("size"))
            year = int(payload.get("year"))
        except (TypeError, ValueError):
            return "FAILURE", {"reason": "invalid setup"}
        if size < 3:
            return "FAILURE", {"reason": "ring size must be at least three"}
        if leader_name not in self.peers:
            return "FAILURE", {"reason": "leader is not registered"}
        free = [p for p in self.peers.values() if p["state"] == "Free" and p["name"] != leader_name]
        if len(free) < size - 1:
            return "FAILURE", {"reason": "not enough free peers"}
        chosen = random.sample(free, size - 1)
        leader = self.peers[leader_name]
        leader["state"] = "Leader"
        selected = [leader] + chosen
        for peer in chosen:
            peer["state"] = "InDHT"
        self.phase = "BUILDING"
        self.leader = leader_name
        self.members = [
            {"name": p["name"], "ip": p["ip"], "p_port": p["p_port"]}
            for p in selected
        ]
        print(f"[SETUP] {leader_name} size={size} year={year}", flush=True)
        return "SUCCESS", {"year": year, "members": self.members}

    def handle(self, request, addr):
        msg_type = request.get("type")
        if msg_type == "REGISTER":
            return self.register(request, addr)
        if msg_type == "SETUP_DHT":
            return self.setup(request, addr)
        if msg_type == "DHT_COMPLETE":
            if self.phase != "BUILDING" or request.get("sender") != self.leader:
                return "FAILURE", {"reason": "no construction in progress"}
            self.phase = "READY"
            counts = request.get("payload", {}).get("counts", {})
            print(f"[COUNT] {counts}", flush=True)
            print("[DHT_COMPLETE] SUCCESS", flush=True)
            return "SUCCESS", {}
        if self.phase != "IDLE" and msg_type not in {"DHT_COMPLETE"}:
            return "FAILURE", {"reason": "manager busy"}
        return "FAILURE", {"reason": "unknown command"}

    def run(self):
        port = self.sock.getsockname()[1]
        print(f"[MANAGER] UDP server listening on port {port}", flush=True)
        while True:
            data, addr = self.sock.recvfrom(BUFFER_SIZE)
            try:
                request = decode(data)
                status, payload = self.handle(request, addr)
            except Exception as error:
                status, payload = "FAILURE", {"reason": str(error)}
            self.send_response(request, addr, status, payload)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 manager.py PORT")
    Manager(int(sys.argv[1])).run()
