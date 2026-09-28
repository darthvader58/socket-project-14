import json
import uuid

BUFFER_SIZE = 65535

def make_message(msg_type, sender, payload=None):
    return {
        "type": msg_type,
        "request_id": str(uuid.uuid4()),
        "sender": sender,
        "payload": payload or {},
    }

def encode(message):
    return json.dumps(message, separators=(",", ":")).encode("utf-8")

def decode(data):
    return json.loads(data.decode("utf-8"))

def make_response(request, status, payload=None):
    return {
        "type": request["type"] + "_RESPONSE",
        "request_id": request["request_id"],
        "status": status,
        "payload": payload or {},
    }
