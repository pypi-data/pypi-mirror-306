# Copyright (C) 2022 Bjarne von Horn (vh at igh dot de).
#
# This file is part of the PdCom Gateway.
#
# The PdCom Gateway is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# The PdCom Gateway is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more .
#
# You should have received a copy of the GNU Lesser General Public License
# along with the PdCom Gateway. If not, see <http://www.gnu.org/licenses/>.

from asyncio import (
    Event,
    CancelledError,
    get_event_loop,
    start_server,
)
from pdcom5 import Process, ScalarSelector
from datetime import datetime, timedelta
from urllib.parse import urlparse
from io import BytesIO


class DataSender:
    """Helper class to add preamble and checksum to each data line"""

    def __init__(self, parent: "NMEA", writer):
        self._parent = parent
        self._writer = writer
        self._checksum = 0

    def __enter__(self):
        self._writer.write(("$" + self._parent._id).encode("ascii"))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._writer.write(b"*%02x\r\n" % (self._checksum,))
        return False

    def add_iter(self, iterable):
        for value in iterable:
            self._checksum ^= ord(",")
            for char in value:
                self._checksum ^= ord(char)
            self._writer.write(b"," + value.encode("ascii"))


class SenderStream:
    def __init__(self, writer):
        self._content_available = Event()
        self._buffer = []
        self._writer = writer

    def append(self, output):
        if len(self._buffer) <= 10:
            self._buffer.append(output)
        self._content_available.set()

    def cancel(self):
        self._writer.close()
        self._buffer.insert(0, None)
        self._content_available.set()

    async def pop(self):
        while len(self._buffer) == 0:
            await self._content_available.wait()
        ans = self._buffer.pop(0)
        if len(self._buffer) == 0:
            self._content_available.clear()
        return ans


class NMEA:
    def __init__(self, config):
        self._config = config
        self._subscriptions = []
        self._process = Process("pdcom_gateway")
        my_config = self._config.modules["NMEA"]
        self._id = my_config.id
        self._writers = set()
        self._idle_task = None

    async def initialize(self):
        # basically list of open client connections
        self._writers = set()
        self._idle_task = None
        await self._process.connect(self._config.rtserver)
        my_config = self._config.modules["NMEA"]
        self._subscriber = self._process.create_subscriber(
            timedelta(seconds=my_config["update-interval"])
        )
        # subscribe to all variables
        pd_time_var = await self._process.find(my_config.time)
        if pd_time_var is None:
            raise RuntimeError("Time Variable " + my_config.time + " not found")
        if pd_time_var.shape != (1,):
            raise RuntimeError("Time Variable " + my_config.time + " is not a scalar")
        self._wall_time = await self._subscriber.subscribe(my_config.time)
        for var in my_config["variables"]:
            splitted_path = var.path.split("#")
            selector = None
            if len(splitted_path) == 2:
                selector = ScalarSelector([int(x) for x in splitted_path[1].split("/")])
            pd_var = await self._process.find(splitted_path[0])
            if pd_var is None:
                raise RuntimeError("Variable " + var.path + " not found")
            subscripton = await self._subscriber.subscribe(pd_var, selector)
            subscripton.gain = var.get("gain", 1.0)
            subscripton.format_str = var.get("format", "%d")
            self._subscriptions.append(subscripton)

        # start server
        async def callback(reader, writer):
            try:
                sender = SenderStream(writer)
                self._writers.add(sender)
                while True:
                    # flush output buffer to socket
                    try:
                        writer.write(await sender.pop())
                        await writer.drain()
                    except Exception:
                        # just close this connection
                        break
            finally:
                if sender in self._writers:
                    self._writers.remove(sender)
                writer.close()

        bind_url = urlparse(my_config.server)
        self._server = await start_server(
            callback, host=bind_url.hostname, port=bind_url.port
        )

        async def idle_task():
            try:
                async for ts in self._subscriber.newValues():
                    buf = BytesIO()
                    with DataSender(self, buf) as ds:
                        ds.add_iter(self.make_wall_time())
                        ds.add_iter(self.make_variable_output())
                    for writer in self._writers:
                        writer.append(buf.getvalue())

            except CancelledError:
                # task.cancel() emits this exception, it has to propagate
                raise
            except Exception as e:
                print(e)
                # close whole server on pdcom error
                self._server.close()
                for any_writer in self._writers:
                    # kill all running connections
                    any_writer.cancel()
                self._server.close()

        # start idle task to close server on pdcom error when no client
        # connection exists
        self._idle_task = get_event_loop().create_task(idle_task())
        await self._server.wait_closed()

    def make_variable_output(self):
        for var in self._subscriptions:
            for cell in var:
                yield var.format_str % (cell * var.gain,)

    def make_wall_time(self):
        # FIMXE(vh) what epoch? e.g. apply offset
        dt = datetime.fromtimestamp(self._wall_time.value)
        yield dt.strftime("%H%M%S.") + str(round(dt.microsecond / 1e4))
        yield dt.strftime("%d")
        yield dt.strftime("%m")
        yield dt.strftime("%Y")


async def start(config):
    nmea = NMEA(config)
    await nmea.initialize()
