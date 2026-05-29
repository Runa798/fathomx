#!/usr/bin/env python3
"""Persistent-stdin MCP stdio client over the SSH bridge to Lapis on heyev100.

Keeps stdin OPEN until the tools/call response (id=2) arrives, so long-running
async tools (aspect_research / deep_research) are not cancelled by stdin EOF.

Usage: mcp_call.py <tool_name> <args_json_file> <out_json_file> [timeout_s]
"""
import json, os, subprocess, sys, threading

tool = sys.argv[1]
args_file = sys.argv[2]
out_file = sys.argv[3]
timeout_s = int(sys.argv[4]) if len(sys.argv) > 4 else 1300
err_file = out_file + ".err"

arguments = json.load(open(args_file, encoding="utf-8"))

remote = "bash /home/heye/.lapis/lapis-mcp-bridge.sh"
rust_log = os.environ.get("LAPIS_RUST_LOG")
if rust_log:
    remote = f"RUST_LOG='{rust_log}' " + remote
cmd = [
    "ssh", "-T", "-i", os.path.expanduser("~/.ssh/id_ed25519"),
    "heye@172.17.0.1", remote,
]
proc = subprocess.Popen(
    cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    stderr=open(err_file, "wb"), text=True, bufsize=1,
)

done = threading.Event()
state = {"killed": False}

def watchdog():
    if not done.wait(timeout_s):
        state["killed"] = True
        proc.kill()

threading.Thread(target=watchdog, daemon=True).start()

def send(obj):
    proc.stdin.write(json.dumps(obj, ensure_ascii=False) + "\n")
    proc.stdin.flush()

result = None
try:
    send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
          "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                     "clientInfo": {"name": "m4", "version": "0"}}})
    _ = proc.stdout.readline()  # init response (id=1)
    send({"jsonrpc": "2.0", "method": "notifications/initialized"})
    send({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
          "params": {"name": tool, "arguments": arguments}})
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if msg.get("id") == 2:
            result = msg
            break
finally:
    done.set()
    try:
        proc.stdin.close()
    except Exception:
        pass
    try:
        proc.terminate()
    except Exception:
        pass

with open(out_file, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False)

if result is None:
    print(f"NO_RESULT killed={state['killed']} (timeout={timeout_s}s)")
    sys.exit(2)

env = result.get("result", {}).get("structuredContent") or {}
status = env.get("status")
err = env.get("error") or {}
print(f"OK got id=2; status={status} err_code={err.get('code')} "
      f"run_id={env.get('run_id')} out_bytes={os.path.getsize(out_file)}")
