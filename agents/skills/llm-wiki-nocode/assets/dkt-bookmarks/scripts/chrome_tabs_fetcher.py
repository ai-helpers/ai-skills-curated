import json
import subprocess
import sys
import time

def main():
    # Start the chrome-devtools-mcp server using npx
    cmd = ["npx", "chrome-devtools-mcp@latest", "--autoConnect"]
    print("Starting process...", file=sys.stderr)
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    # Let's read from stderr in a non-blocking way, or wait a bit
    time.sleep(1)

    try:
        # Helper to send a message
        def send(msg):
            line = json.dumps(msg)
            print(f"--> CLIENT SEND: {line}", file=sys.stderr)
            proc.stdin.write(line + "\n")
            proc.stdin.flush()

        # Helper to read a response
        def recv():
            line = proc.stdout.readline()
            if not line:
                print("<-- CLIENT RECV: EOF", file=sys.stderr)
                return None
            print(f"<-- CLIENT RECV: {line.strip()}", file=sys.stderr)
            return json.loads(line)

        # 1. Send initialize
        init_req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "gemini-cli-client",
                    "version": "1.0.0"
                }
            }
        }
        send(init_req)
        
        # Read lines until we get the initialize response (matching id=1)
        init_resp = None
        while True:
            msg = recv()
            if msg is None:
                break
            if msg.get("id") == 1:
                init_resp = msg
                break

        if not init_resp:
            print("Failed to initialize MCP server", file=sys.stderr)
            sys.exit(1)

        # 2. Send notifications/initialized
        initialized_notif = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        send(initialized_notif)

        # 3. Call tool list_pages
        call_req = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "list_pages",
                "arguments": {}
            }
        }
        send(call_req)

        # Read lines until we get the response for id=2
        call_resp = None
        while True:
            msg = recv()
            if msg is None:
                break
            if msg.get("id") == 2:
                call_resp = msg
                break

        if not call_resp or "error" in call_resp:
            err = call_resp.get("error") if call_resp else "No response"
            print(f"Error calling list_pages: {err}", file=sys.stderr)
            # Let's print stderr of the process to debug
            proc.terminate()
            stderr_out = proc.stderr.read()
            print(f"Server STDERR:\n{stderr_out}", file=sys.stderr)
            sys.exit(1)

        # Output the result
        result = call_resp.get("result", {})
        print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"Exception: {e}", file=sys.stderr)
        proc.terminate()
        stderr_out = proc.stderr.read()
        print(f"Server STDERR:\n{stderr_out}", file=sys.stderr)
        sys.exit(1)
    finally:
        if proc.poll() is None:
            proc.terminate()
            proc.wait()

if __name__ == "__main__":
    main()
