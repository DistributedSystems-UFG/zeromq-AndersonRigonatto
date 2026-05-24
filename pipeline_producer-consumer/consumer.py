import json
import sys

import zmq

PORT_IN = 5558


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 consumer.py <worker-ip>")
        sys.exit(1)

    worker_ip = sys.argv[1]

    ctx = zmq.Context()
    sock = ctx.socket(zmq.PULL)
    sock.connect(f"tcp://{worker_ip}:{PORT_IN}")
    print(f"Consumer: PULL tcp://{worker_ip}:{PORT_IN}")

    count = 0
    total = 0
    minimum = None
    maximum = None

    while True:
        msg = json.loads(sock.recv_string())
        if msg.get("done"):
            break
        original = msg["value"]
        squared = msg["squared"]
        count += 1
        total += squared
        if minimum is None or squared < minimum:
            minimum = squared
        if maximum is None or squared > maximum:
            maximum = squared
        print(f"[{count}] received {original} -> {squared}")

    print("\n=== Pipeline Summary ===")
    print(f"Items processed: {count}")
    if count > 0:
        print(f"Sum of squares : {total}")
        print(f"Min squared    : {minimum}")
        print(f"Max squared    : {maximum}")
        print(f"Avg squared    : {total / count:.2f}")


if __name__ == "__main__":
    main()
