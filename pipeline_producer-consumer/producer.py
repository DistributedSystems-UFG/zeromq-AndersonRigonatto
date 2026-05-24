import json
import random
import time

import zmq

PORT_OUT = 5557
N_EVENTS = 20


def main():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUSH)
    sock.bind(f"tcp://*:{PORT_OUT}")
    print(f"Producer bound to tcp://*:{PORT_OUT}")

    # Give downstream stages time to connect before pushing.
    time.sleep(2)

    for i in range(N_EVENTS):
        value = random.randint(1, 50)
        sock.send_string(json.dumps({"value": value}))
        print(f"Produced {i + 1}/{N_EVENTS}: {value}")
        time.sleep(0.2)

    # Sentinel so the pipeline terminates cleanly.
    sock.send_string(json.dumps({"done": True}))
    print("Producer done, sentinel sent.")
    time.sleep(2)


if __name__ == "__main__":
    main()
