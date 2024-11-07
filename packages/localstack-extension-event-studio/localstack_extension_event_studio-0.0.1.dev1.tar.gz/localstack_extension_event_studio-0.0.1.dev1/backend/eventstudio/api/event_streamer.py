import json
import logging
from typing import Any

from localstack.http.websocket import (
    WebSocket,
    WebSocketDisconnectedError,
    WebSocketRequest,
)

from eventstudio.api.utils.utils import CustomJSONEncoder

LOG = logging.getLogger(__name__)


class EventStreamer:
    sockets: list[WebSocket]

    def __init__(self):
        self.sockets = []

    def on_websocket_request(self, request: WebSocketRequest, *args, **kwargs):
        websocket = None
        try:
            with request.accept() as websocket:
                self.sockets.append(websocket)
                while True:
                    msg = websocket.receive()
                    LOG.info("Received message from log streamer websocket: %s", msg)
        except WebSocketDisconnectedError:
            LOG.debug("Websocket disconnected: %s", websocket)
        finally:
            if websocket is not None:
                self.sockets.remove(websocket)

    def notify(self, doc: Any):
        data = json.dumps(doc, cls=CustomJSONEncoder)
        for socket in self.sockets:
            socket.send(data)
