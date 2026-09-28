import queue
import socket
import sys
import threading
import time

from dht import LocalTable, calculate_hash, load_storm_data, next_prime
from protocol import BUFFER_SIZE, decode, encode, make_message


class Peer:
    def __init__(self, manager_ip, manager_port):
        self.manager_addr = (manager_ip, int(manager_port))
        self.manager_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.manager_sock.settimeout(10)
        self.peer_sock = None
        self.name = None
        self.ip = None
        self.p_port = None
        self.my_id = None
        self.ring_size = 0
        self.members = []
        self.right = None
        self.leader = None
        self.table = LocalTable()
        self.store_acks = queue.Queue()
        self.count_results = queue.Queue()

    def request_manager(self, request):
        self.manager_sock.sendto(encode(request), self.manager_addr)
        while True:
            data, _ = self.manager_sock.recvfrom(BUFFER_SIZE)
            response = decode(data)
            if response.get("request_id") == request.get("request_id"):
                return response

    def start_peer_socket(self, port):
        self.peer_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.peer_sock.bind(("0.0.0.0", port))
        self.peer_sock.settimeout(1)
        threading.Thread(target=self.listen, daemon=True).start()

    def register(self, name, ip, manager_port, peer_port):
        request = make_message("REGISTER", name, {
            "ip": ip,
            "m_port": int(manager_port),
            "p_port": int(peer_port),
        })
        response = self.request_manager(request)
        status = response.get("status")
        reason = response.get("payload", {}).get("reason", "")
        print(f"[REGISTER] {status} {reason}".rstrip(), flush=True)
        if status == "SUCCESS":
            self.name = name
            self.ip = ip
            self.p_port = int(peer_port)
            self.start_peer_socket(self.p_port)

    def send_peer(self, peer, message):
        self.peer_sock.sendto(encode(message), (peer["ip"], int(peer["p_port"])))

    def set_id(self, payload):
        self.my_id = int(payload["id"])
        self.ring_size = int(payload["ring_size"])
        self.members = payload["members"]
        self.leader = payload["leader"]
        self.right = self.members[(self.my_id + 1) % self.ring_size]
        print(f"[RING] {self.name} -> ID {self.my_id}", flush=True)

    def handle_store(self, message):
        payload = message["payload"]
        if payload["target_id"] == self.my_id:
            self.table.store(payload["position"], payload["record"])
            ack = make_message("STORE_ACK", self.name, {
                "store_id": message["request_id"],
                "count": self.table.count(),
            })
            leader = payload["leader"]
            self.peer_sock.sendto(encode(ack), (leader["ip"], int(leader["p_port"])))
            return
        payload["hop_count"] += 1
        if payload["hop_count"] >= self.ring_size:
            return
        self.send_peer(self.right, message)

    def handle_count(self, message):
        payload = message["payload"]
        counts = payload.setdefault("counts", {})
        counts[str(self.my_id)] = self.table.count()
        if self.my_id == 0 and payload["hop_count"] > 0:
            self.count_results.put(counts)
            return
        payload["hop_count"] += 1
        self.send_peer(self.right, message)

    def handle(self, message):
        msg_type = message.get("type")
        if msg_type == "SET_ID":
            self.set_id(message["payload"])
        elif msg_type == "STORE":
            self.handle_store(message)
        elif msg_type == "STORE_ACK":
            self.store_acks.put(message)
        elif msg_type == "COUNT":
            self.handle_count(message)

    def listen(self):
        while True:
            try:
                data, _ = self.peer_sock.recvfrom(BUFFER_SIZE)
            except socket.timeout:
                continue
            except OSError:
                return
            try:
                self.handle(decode(data))
            except Exception as error:
                print(f"[PEER] {error}", flush=True)

    def configure_ring(self, response):
        payload = response["payload"]
        self.set_id({
            "id": 0,
            "ring_size": len(payload["members"]),
            "members": payload["members"],
            "leader": self.name,
        })
        for index, member in enumerate(self.members[1:], 1):
            message = make_message("SET_ID", self.name, {
                "id": index,
                "ring_size": self.ring_size,
                "members": self.members,
                "leader": self.name,
            })
            self.send_peer(member, message)

    def build(self, year):
        records = load_storm_data(f"data/details-{year}.csv")
        table_size = next_prime(2 * len(records))
        print(f"[DATA] {len(records)} records, table size {table_size}", flush=True)
        for record in records:
            position, target_id = calculate_hash(record["event_id"], table_size, self.ring_size)
            if target_id == 0:
                self.table.store(position, record)
                continue
            message = make_message("STORE", self.name, {
                "target_id": target_id,
                "position": position,
                "hop_count": 0,
                "record": record,
                "leader": {"ip": self.ip, "p_port": self.p_port},
            })
            self.send_peer(self.right, message)
            self.store_acks.get(timeout=10)
        print("[DATA] Record distribution complete", flush=True)
        self.send_peer(self.right, make_message("COUNT", self.name, {
            "counts": {},
            "hop_count": 0,
        }))
        counts = self.count_results.get(timeout=10)
        print(f"[COUNT] {counts}", flush=True)
        if sum(counts.values()) != len(records):
            raise RuntimeError("record count mismatch")
        response = self.request_manager(make_message("DHT_COMPLETE", self.name, {
            "counts": counts,
        }))
        print(f"[DHT_COMPLETE] {response.get('status')}", flush=True)

    def setup(self, size, year):
        response = self.request_manager(make_message("SETUP_DHT", self.name, {
            "size": int(size),
            "year": int(year),
        }))
        print(f"[SETUP] {response.get('status')}", flush=True)
        if response.get("status") != "SUCCESS":
            return
        self.configure_ring(response)
        time.sleep(1)
        try:
            self.build(int(year))
        except Exception as error:
            print(f"[DHT] {error}", flush=True)

    def run(self):
        while True:
            try:
                line = input("peer> ").strip().split()
            except EOFError:
                return
            if not line:
                continue
            if line[0] == "register" and len(line) == 5:
                self.register(line[1], line[2], line[3], line[4])
            elif line[0] == "setup-dht" and len(line) == 4:
                self.setup(line[2], line[3])
            elif line[0] in {"quit", "exit"}:
                return
            else:
                print("usage: register NAME IP MANAGER_PORT PEER_PORT | setup-dht NAME SIZE YEAR", flush=True)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: python3 peer.py MANAGER_IP MANAGER_PORT")
    Peer(sys.argv[1], sys.argv[2]).run()
