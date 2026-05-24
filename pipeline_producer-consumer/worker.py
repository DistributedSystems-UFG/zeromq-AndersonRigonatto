import json
import sys
import time

import zmq

PORT_IN = 5557
PORT_OUT = 5558


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 worker.py <producer-ip>")
        sys.exit(1)

    producer_ip = sys.argv[1]

    ctx = zmq.Context()
    pull = ctx.socket(zmq.PULL)
    pull.connect(f"tcp://{producer_ip}:{PORT_IN}")
    push = ctx.socket(zmq.PUSH)
    push.bind(f"tcp://*:{PORT_OUT}")
    print(
        f"Worker: PULL tcp://{producer_ip}:{PORT_IN} -> PUSH tcp://*:{PORT_OUT}"
    )

    count = 0
    while True:
        msg = json.loads(pull.recv_string())
        if msg.get("done"):
            push.send_string(json.dumps({"done": True}))
            print(f"Worker done. Forwarded {count} items.")
            break
        value = msg["value"]
        squared = value * value
        push.send_string(json.dumps({"value": value, "squared": squared}))
        count += 1
        print(f"[{count}] {value} -> {squared}")

    time.sleep(2)


if __name__ == "__main__":
    main()
