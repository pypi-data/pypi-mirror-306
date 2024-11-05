import json
from rich import print
from websockets.sync.client import connect

from snarkify_cli.lib.auth import get_auth_header
from snarkify_cli.lib.constants import SNARKIFY_WEBSOCKET_URL


def loop_for_task_logs(task_id: str):
    try:
        with connect(
            f"{SNARKIFY_WEBSOCKET_URL}/tasks/{task_id}/logs",
            additional_headers=get_auth_header(),
        ) as websocket:
            while True:
                message = websocket.recv()
                log_data = json.loads(json.loads(message))
                for log in log_data.get("logs", []):
                    print(log)
                websocket.send(json.dumps({"message": "received"}))
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Fail to fetch task logs due to {str(e)}.")
