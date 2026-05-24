import zmq

PORT = 5555


def compute(op, a, b):
    if op == "ADD":
        return a + b
    if op == "SUB":
        return a - b
    if op == "MUL":
        return a * b
    if op == "DIV":
        if b == 0:
            return "ERR div_by_zero"
        return a / b
    return f"ERR unknown_op:{op}"


def main():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.REP)
    sock.bind(f"tcp://*:{PORT}")
    print(f"Server listening on tcp://*:{PORT}")

    while True:
        msg = sock.recv_string()
        print(f"Received: {msg}")

        if msg == "STOP":
            sock.send_string("BYE")
            print("Stop requested. Exiting.")
            break

        try:
            parts = msg.split()
            op = parts[0]
            a = float(parts[1])
            b = float(parts[2])
            result = compute(op, a, b)
            reply = f"{result}"
        except Exception as e:
            reply = f"ERR parse:{e}"

        sock.send_string(reply)
        print(f"Sent: {reply}")


if __name__ == "__main__":
    main()
