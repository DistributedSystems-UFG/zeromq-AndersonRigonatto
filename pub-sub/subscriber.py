import sys

import zmq

PORT = 5556
MESSAGES_TO_READ = 10


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 subscriber.py <publisher-ip> <topic>")
        print("Topics: TEMP, PRESS, HUM")
        sys.exit(1)

    pub_ip = sys.argv[1]
    topic = sys.argv[2]

    ctx = zmq.Context()
    sock = ctx.socket(zmq.SUB)
    sock.connect(f"tcp://{pub_ip}:{PORT}")
    sock.setsockopt_string(zmq.SUBSCRIBE, topic)
    print(f"Subscribed to '{topic}' at tcp://{pub_ip}:{PORT}")

    for i in range(MESSAGES_TO_READ):
        msg = sock.recv_string()
        print(f"[{i + 1}/{MESSAGES_TO_READ}] {msg}")

    print("Subscriber done.")


if __name__ == "__main__":
    main()
