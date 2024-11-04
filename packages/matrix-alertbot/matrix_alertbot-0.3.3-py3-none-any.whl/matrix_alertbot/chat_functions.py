from __future__ import annotations

import logging
from typing import Dict, Optional, TypedDict, Union

from nio.client import AsyncClient
from nio.exceptions import SendRetryError
from nio.responses import ErrorResponse, Response, RoomSendError, RoomSendResponse
from typing_extensions import NotRequired

logger = logging.getLogger(__name__)


ContentEventDict = TypedDict(
    "ContentEventDict",
    {
        "msgtype": str,
        "format": str,
        "body": str,
        "formatted_body": NotRequired[str],
        "m.relates_to": NotRequired[Dict],
    },
)


async def send_text_to_room(
    matrix_client: AsyncClient,
    room_id: str,
    plaintext: str,
    html: Optional[str] = None,
    notice: bool = True,
    reply_to_event_id: Optional[str] = None,
) -> RoomSendResponse:
    """Send text to a matrix room.

    Args:
        client: The client to communicate to matrix with.

        room_id: The ID of the room to send the message to.

        plaintext: The message content.

        html: The message content in HTML format.

        notice: Whether the message should be sent with an "m.notice" message type
            (will not ping users).

        reply_to_event_id: Whether this message is a reply to another event. The event
            ID this is message is a reply to.

    Returns:
        A RoomSendResponse if the request was successful, else an ErrorResponse.
    """
    # Determine whether to ping room members or not
    msgtype = "m.notice" if notice else "m.text"

    content: ContentEventDict = {
        "msgtype": msgtype,
        "format": "org.matrix.custom.html",
        "body": plaintext,
    }

    if html is not None:
        content["formatted_body"] = html

    if reply_to_event_id:
        content["m.relates_to"] = {"m.in_reply_to": {"event_id": reply_to_event_id}}

    response_event = await matrix_client.room_send(
        room_id,
        "m.room.message",
        content,
        ignore_unverified_devices=True,
    )

    if isinstance(response_event, RoomSendError):
        raise SendRetryError(f"{response_event.status_code} - {response_event.message}")
    return response_event


async def react_to_event(
    client: AsyncClient,
    room_id: str,
    event_id: str,
    reaction_text: str,
) -> Union[Response, ErrorResponse]:
    """Reacts to a given event in a room with the given reaction text

    Args:
        client: The client to communicate to matrix with.

        room_id: The ID of the room to send the message to.

        event_id: The ID of the event to react to.

        reaction_text: The string to react with. Can also be (one or more) emoji characters.

    Returns:
        A nio.Response or nio.ErrorResponse if an error occurred.

    Raises:
        SendRetryError: If the reaction was unable to be sent.
    """
    content = {
        "m.relates_to": {
            "rel_type": "m.annotation",
            "event_id": event_id,
            "key": reaction_text,
        }
    }

    response_event = await client.room_send(
        room_id,
        "m.reaction",
        content,
        ignore_unverified_devices=True,
    )

    if isinstance(response_event, RoomSendError):
        raise SendRetryError(f"{response_event.status_code} - {response_event.message}")
    return response_event


def strip_fallback(content: str) -> str:
    index = 0
    for line in content.splitlines(keepends=True):
        if not line.startswith("> "):
            break
        if index == 0:
            index += 1
        index += len(line)
    return content[index:]
