import random
import time

import zmq

PORT = 5556

TOPICS = {
    "TEMP": (15.0, 35.0),
    "PRESS": (980.0, 1050.0),
    "HUM": (20.0, 95.0),
}


def main():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUB)
    sock.bind(f"tcp://*:{PORT}")
    print(f"Publisher running on tcp://*:{PORT} (Ctrl+C to stop)")

    while True:
        topic = random.choice(list(TOPICS.keys()))
        lo, hi = TOPICS[topic]
        value = round(random.uniform(lo, hi), 1)
        msg = f"{topic} {value}"
        sock.send_string(msg)
        print(f"Published: {msg}")
        time.sleep(1)


if __name__ == "__main__":
    main()
