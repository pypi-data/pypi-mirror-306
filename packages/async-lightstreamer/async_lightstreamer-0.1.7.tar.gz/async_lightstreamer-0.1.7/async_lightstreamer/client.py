import asyncio
import logging
import traceback
from dataclasses import dataclass
from typing import Dict
from urllib import parse

import aiohttp

from async_lightstreamer import exceptions, subscription

CONNECTION_URL_PATH = "lightstreamer/create_session.txt"
BIND_URL_PATH = "lightstreamer/bind_session.txt"
CONTROL_URL_PATH = "lightstreamer/control.txt"
# Request parameter to create and activate a new Table.
OP_ADD = "add"
# Request parameter to delete a previously created Table.
OP_DELETE = "delete"
# Request parameter to force closure of an existing session.
OP_DESTROY = "destroy"
# List of possible server responses
PROBE_CMD = "PROBE"
END_CMD = "END"
LOOP_CMD = "LOOP"
ERROR_CMD = "ERROR"
SYNC_ERROR_CMD = "SYNC ERROR"
OK_CMD = "OK"


@dataclass
class Metrics:
    connected: bool = False
    binds_count: int = 0
    subscribe_count: int = 0
    failed_subscribe_count: int = 0
    reconnect_count: int = 0


class LightstreamerClient:
    """
    Async lightstreamer client

    Args:
        lightstreamer_username (str): Username
        lightstreamer_password (str): Password
        lightstreamer_url (str): Lightstreamer server url
        adapter_set (str): Adapter set. Defaults To ''
        logger (logging.Logger): Logger.
            Defaults to logger with `lightstreamer` name
        task_group (asyncio.TaskGroup | None): If you pass TaskGroup
            client use this TaskGroup for creating receiving task
            other wise creates task wtih `asyncio.create_task`
        should_reconnect (bool): Should client reconnect if there is an exception
            in session. Client re subscribe to all subscriptions.
            Defaults to False
        reconnect_retries (int): number of tries for reconnecting.
            If set to -1 retry till apocalypse
    """

    logger = logging.getLogger("lightstreamer")

    def __init__(
        self,
        lightstreamer_username: str,
        lightstreamer_password: str,
        lightstreamer_url: str,
        adapter_set: str = "",
        logger: logging.Logger = logger,
        task_group: asyncio.TaskGroup | None = None,
        should_reconnect: bool = False,
        reconnect_retries: int = 100,
    ):
        self.logger = logger
        self._reconnect = should_reconnect
        self._reconnect_retires = reconnect_retries
        self._task_group = task_group
        self._lightstreamer_username = lightstreamer_username
        self._lightstreamer_password = lightstreamer_password
        self._lightstreamer_url = parse.urlparse(lightstreamer_url)
        self._adapter_set = adapter_set
        self._session_id: str | None = None
        self._control_address = self._lightstreamer_url
        self._stream_session: aiohttp.ClientSession | None = None
        self._stream: aiohttp.ClientResponse | None = None
        self._current_subscription_key = 0
        self._subscriptions: Dict[int, subscription.LightstreamerSubscription] = {}
        self._task: asyncio.Task | None = None
        self._metrics = Metrics()
        self._can_reconnect = True

    def metrics(self) -> Metrics:
        """
        Returns metrics object
        """
        return self._metrics

    async def connect(self) -> None:
        """
        Establish a connection to Lightstreamer Server to create a new session.
        """

        self.logger.debug(
            "Opening a new session to <%s>",
            self._lightstreamer_url.geturl(),
        )
        params = {
            "LS_op2": "create",
            # TODO: check this field
            "LS_cid": "mgQkwtwdysogQz2BJ4Ji kOj2Bg",
            "LS_adapter_set": self._adapter_set,
            "LS_user": self._lightstreamer_username,
            "LS_password": self._lightstreamer_password,
        }
        url = parse.urljoin(self._lightstreamer_url.geturl(), CONNECTION_URL_PATH)
        self._stream_session = aiohttp.ClientSession(
            raise_for_status=True,
            timeout=aiohttp.ClientTimeout(total=None),
        )
        self._stream = await self._stream_session.post(
            url,
            data=params,
            timeout=aiohttp.ClientTimeout(total=None),
        )  # type: ignore
        await self._handle_connection_stream()
        self._metrics.connected = True

    async def bind(self) -> None:
        """Replace a completely consumed connection in listening for an active Session."""
        self.logger.debug("Binding to <%s>", self._control_address.geturl())
        await self._close_stream()
        params = {"LS_session": self._session_id}
        url = parse.urljoin(self._control_address.geturl(), BIND_URL_PATH)
        self._stream_session = aiohttp.ClientSession(
            raise_for_status=True,
            timeout=aiohttp.ClientTimeout(total=None),
        )
        self._stream = await self._stream_session.post(
            url,
            data=params,
            timeout=aiohttp.ClientTimeout(total=None),
        )  # type: ignore
        await self._handle_connection_stream()
        self.logger.info("Bound to <%s>", self._control_address.geturl())
        self._metrics.binds_count += 1

    async def disconnect(self, cancel_task: bool = True) -> None:
        """Request to close the session previously opened with the connect() invocation."""

        if self._stream is not None:
            self.logger.debug(
                "Closing session to <%s>", self._lightstreamer_url.geturl()
            )
            await self._control({"LS_op": OP_DESTROY})
            if self._task and cancel_task:
                self._task.cancel()
                try:
                    await self._task
                except asyncio.CancelledError:
                    pass
            await self._close_stream()
            self.logger.info("Closed session to <%s>", self._lightstreamer_url.geturl())
        else:
            self.logger.warning("No connection to Lightstreamer")
        self._metrics.connected = False

    async def subscribe(
        self,
        subscription: subscription.LightstreamerSubscription,
        subscription_key: int | None = None,
    ) -> int:
        """
        Perform a subscription request to Lightstreamer Server.
        This is not parallel safe

        Args:
            subscription (subscription.LightstreamerSubscription):
                subscription object contains, mode, fields, and ...
            key (int | None): key of subscription. Defaults to None
                if None use autoincrement id

        Returns:
            int: subscription key for unsubscribing
        """

        # register the Subscription with a new subscription key
        if subscription_key is None:
            self._current_subscription_key += 1
            subscription_key = self._current_subscription_key
        self._subscriptions[subscription_key] = subscription

        # send the control request to perform the subscription
        self.logger.debug("Making a new subscription request")
        server_response = await self._control(
            {
                "LS_Table": subscription_key,
                "LS_op": OP_ADD,
                "LS_data_adapter": subscription.adapter,
                "LS_mode": subscription.mode.value,
                "LS_schema": " ".join(subscription.field_names),
                "LS_id": " ".join(subscription.item_names),
            }
        )
        if server_response == OK_CMD:
            self.logger.info("Successfully subscribed ")
            self._metrics.subscribe_count += 1
        else:
            self.logger.warning("Subscription error %s", server_response)
            self._metrics.failed_subscribe_count += 1
            raise exceptions.SubscriptionFailed()
        return subscription_key 

    async def unsubscribe(self, subcription_key: int) -> None:
        """
        Unregister the Subscription associated to the specified subcription_key.

        Args:
            subcription_key(int): subscription key obtained from `subscribe` method
        """

        self.logger.debug("Making an unsubscription request")
        if subcription_key in self._subscriptions:
            server_response = await self._control(
                {
                    "LS_Table": subcription_key,
                    "LS_op": OP_DELETE,
                }
            )

            if server_response == OK_CMD:
                del self._subscriptions[subcription_key]
                self.logger.info("Successfully unsubscribed")
            else:
                self.logger.warning("Unsubscription error")
        else:
            self.logger.warning("No subscription key %s found!", subcription_key)
            raise KeyError(subcription_key)

    async def _try_reconnect(self) -> bool:
        try:
            await self.connect()
        except Exception as e:
            self.logger.error("connection failed %s", e)
            return False
        try:
            for key, sub in self._subscriptions.copy().items():
                await self.subscribe(sub, key)
        except Exception as e:
            self.logger.error("subscribe failed %s", e)
            return False
        return True

    async def reconnect(self) -> None:
        i = self._reconnect_retires
        self._session_id = None
        while i != 0:
            self.logger.info("reconnecting attempt %d", self._reconnect_retires - i + 1)
            try:
                await self.disconnect(cancel_task=False)
            except Exception as e:
                self.logger.error("failed to disconnect %s", e)
            self._metrics.reconnect_count += 1
            if await self._try_reconnect():
                break
            i -= 1
        self._can_reconnect = True


    async def _control(self, params: Dict) -> str:
        """
        Create a Control Connection to send control commands that manage the content of Stream Connection.
        """
        if self._session_id is None:
            raise exceptions.LightstreamerNotConnected()
        params["LS_session"] = self._session_id
        url = parse.urljoin(self._control_address.geturl(), CONTROL_URL_PATH)
        async with (
            aiohttp.ClientSession(raise_for_status=True) as session,
            session.post(url=url, data=params) as response,
        ):
            decoded_response = (await response.text()).rstrip()
        self.logger.debug("Server response: <%s>", decoded_response)
        return decoded_response

    async def _close_stream(self) -> None:
        try:
            if self._stream_session:
                await self._stream_session.close()
        except Exception as e:
            self.logger.warning("Failed to close stream: %s", e)

    async def _next_line(self) -> str:
        # TODO: add timeout
        if self._stream is None:
            raise exceptions.LightstreamerNotConnected()
        return (await self._stream.content.readline()).decode("utf-8").rstrip()

    async def _handle_connection_stream(self) -> None:
        stream_line = await self._next_line()
        if stream_line == OK_CMD:
            self.logger.info(
                "Successfully connected to <%s>", self._lightstreamer_url.geturl()
            )
            self.logger.debug("Starting to handling real-time stream")
            while True:
                next_stream_line = await self._next_line()
                if next_stream_line:
                    key, value = next_stream_line.split(":", 1)
                    if key == "SessionId":
                        self._session_id = value
                    elif key == "ControlAddress":
                        parsed_custom_address = parse.urlparse("//" + value)
                        self._control_address = parsed_custom_address._replace(
                            scheme=self._lightstreamer_url[0]
                        )
                else:
                    break

            if self._task_group:
                self._task = self._task_group.create_task(self._receive())
            else:
                self._task = asyncio.create_task(self._receive())

        else:
            self.logger.error("server response error %s", stream_line)
            raise OSError()

    async def _forward_update_message(self, update_message: str):
        """Forwards the real time update to the relative Subscription instance for further dispatching to its listeners."""

        self.logger.debug("Received update message: <%s>", update_message)
        try:
            tok = update_message.split(",", 1)
            table, item = int(tok[0]), tok[1]
            if table in self._subscriptions:
                await self._subscriptions[table].notifyupdate(item)
            else:
                self.logger.warning("No subscription found!")
        except Exception:
            print(traceback.format_exc())

    async def _receive(self):
        rebind = False
        receive = True
        try:
            while receive:
                self.logger.debug("Waiting for a new message")
                try:
                    message = await self._next_line()
                    self.logger.debug("Received message: <%s>", message)
                    if not message.strip():
                        message = None
                except Exception:
                    self.logger.error("Communication error")
                    print(traceback.format_exc())
                    message = None

                if message is None:
                    receive = False
                    self.logger.warning("No new message received")
                elif message == PROBE_CMD:
                    # skipping the PROBE message, keep on receiving messages
                    self.logger.debug("PROBE message")
                elif message.startswith(ERROR_CMD):
                    # terminate the receiving loop on ERROR message
                    receive = False
                    self.logger.error("ERROR")
                elif message.startswith(LOOP_CMD):
                    # terminate the the receiving loop on LOOP message
                    # a complete implementation should proceed with a rebind of the session
                    self.logger.debug("LOOP")
                    receive = False
                    rebind = True
                elif message.startswith(SYNC_ERROR_CMD):
                    # terminate the receiving loop on SYNC ERROR message
                    # a complete implementation should create a new session and re-subscribe to all the old items and relative fields
                    self.logger.error("SYNC ERROR")
                    receive = False
                elif message.startswith(END_CMD):
                    # terminate the receiving loop on END message
                    # the session has been forcibly closed on the server side a complete implementation should handle the "cause_code" if present
                    self.logger.info("Connection closed by the server")
                    receive = False
                elif message.startswith("Preamble"):
                    # skipping Preamble message, keep on receiving messages
                    self.logger.debug("Preamble")
                else:
                    await self._forward_update_message(message)

            if not rebind:
                self.logger.debug(
                    "No rebind to <%s>, clearing internal session data",
                    self._lightstreamer_url.geturl(),
                )
                # clear internal data structures for session and subscriptions management
                self._session_id = None
                # self._subscriptions.clear()
                # self._current_subscription_key = 0
                await self._close_stream()
            else:
                self.logger.debug("Binding to this active session")
                await self.bind()
        except Exception as e:
            self.logger.error("receiving failed with exception %s", e)
        # TODO: fix
        # There is a bug where sub fails and we have two task 
        if self._reconnect and self._can_reconnect:
            self._can_reconnect = False
            await self.reconnect()
