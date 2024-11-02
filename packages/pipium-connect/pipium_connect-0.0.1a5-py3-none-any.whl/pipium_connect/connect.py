from pipium_connect.connect_model import ConnectOptions
from pipium_connect.run_connection_model import Connections
import requests
import socketio
import sys

sio = socketio.Client()


def connect(
    api_key: str,
    connections: Connections,
    options: ConnectOptions = ConnectOptions(),
):
    server_url = get_server_url(options)

    log(f"Connecting to Pipium")

    sio.connect(
        f"{server_url}?api-key={api_key}",
        transports=["websocket"],
    )

    @sio.on("pp-connect")
    def handle_connected():
        payload = {
            "source": "user",
            "models": [
                {
                    "id": id,
                    **omit_properties(connection, ["run_sync", "run_async"]),
                }
                for id, connection in connections.items()
            ],
        }

        sio.emit("pp-init", payload)

    @sio.on("pp-disconnect")
    def handle_disconnected():
        log("Disconnected")

    @sio.on("pp-run")
    def handle_run(connection_input: dict):
        input = connection_input_to_run_input(connection_input)

        id = input["id"]
        user_id = input["user_id"]
        pipe_id = input["pipe_id"]
        model_id = input["model_id"]
        layer_id = input["layer_id"]
        result_id = input["result_id"]
        model = connections.get(input["connection_model_id"])

        def emit_start():
            start = {
                "id": id,
                "user_id": user_id,
                "pipe_id": pipe_id,
                "model_id": model_id,
                "layer_id": layer_id,
                "result_id": result_id,
            }
            log("Emitting start")
            sio.emit("pp-start", start)

        def emit_result(value: dict):
            payload = {
                "value": value,
                "id": id,
                "user_id": user_id,
                "pipe_id": pipe_id,
                "layer_id": layer_id,
                "model_id": model_id,
                "result_id": result_id,
                "mime_type": model["types"]["output"],
            }
            log("Emitting result")
            sio.emit("pp-result", payload)

        def emit_error(message: str):
            payload = {
                "id": id,
                "user_id": user_id,
                "pipe_id": pipe_id,
                "layer_id": layer_id,
                "model_id": model_id,
                "result_id": result_id,
                "message": create_error_message(message),
            }
            log("Emitting error")
            sio.emit("pp-error", payload)

        def emit_complete():
            payload = {
                "id": id,
                "user_id": user_id,
                "pipe_id": pipe_id,
                "layer_id": layer_id,
                "model_id": model_id,
                "result_id": result_id,
            }
            log("Emitting complete")
            sio.emit("pp-complete", payload)

        if not model:
            log(f"Model {model_id} not found")
            emit_complete()
            return

        def create_error_message(native_error_message: str) -> str:
            return f'The model threw an error "{native_error_message}"'

        def on_error(error: Exception):
            native_error_message = (
                str(error) if isinstance(error, Exception) else "Unknown error"
            )
            error_message = create_error_message(native_error_message)
            log(error_message)
            emit_error(native_error_message)

        if "run_sync" not in model and "run_async" not in model:
            log("No run function found")
            emit_complete()
            return

        emit_start()

        if "run_sync" in model:
            log("Starting sync run")
            try:
                output = model["run_sync"](input)
                values = output if isinstance(output, list) else [output]
                for value in values:
                    emit_result(value)
                emit_complete()
            except Exception as error:
                on_error(error)
                return

        if "run_async" in model:
            log("Starting async run")
            try:
                model["run_async"](
                    input,
                    {
                        "next": emit_result,
                        "error": emit_error,
                        "complete": emit_complete,
                    },
                )
            except Exception as error:
                on_error(error)
                return

    @sio.on("pp-log")
    def handle_log(message: str):
        log(message)

    @sio.on("pp-log-error")
    def handle_log(message: str):
        log(message)

    @sio.on("exception")
    def handle_exception(message: str):
        log(message)

    sio.wait()


def log(message: str):
    print(f"[Pipium] {message}")
    sys.stdout.flush()


def connection_input_to_run_input(
    connection_input: dict,
):
    return {
        **connection_input,
        "text": try_string_decode(connection_input["binary"]),
        "previous_values": [
            connection_previous_value_to_run_previous_value(previous_value)
            for previous_value in connection_input["previous_values"]
        ],
    }


def get_server_url(options: ConnectOptions):
    if "server_url" in options:
        return options["server_url"]

    return "https://server-production-00001-pq8-vauf4uyfmq-ey.a.run.app"


def try_string_decode(binary):
    try:
        return binary.decode("utf-8")
    except UnicodeDecodeError:
        return ""


def omit_properties(obj, keys):
    return {k: v for k, v in obj.items() if k not in keys}


def connection_previous_value_to_run_previous_value(previous_value):
    return {
        **previous_value,
        "binary": lambda: fetch_binary(previous_value["uri"]),
        "text": lambda: fetch_text(previous_value["uri"]),
    }


def fetch_binary(uri):
    response = requests.get(uri)
    return response.content


def fetch_text(uri):
    response = requests.get(uri)
    return response.text
