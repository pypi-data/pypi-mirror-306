#!python

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


import asyncio
from sys import argv
import pdcom_gateway_lib
from importlib import import_module


async def main(config):
    tasks = []
    loop = asyncio.get_event_loop()
    for module in config.modules.keys():
        py_module = import_module("pdcom_gateway_lib.modules." + module)
        tasks.append(loop.create_task(py_module.start(config)))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    if len(argv) != 2 or argv[1] in ("-h", "--help"):
        print("usage: ", argv[0], "<config file>")
        exit(1)

    conf = pdcom_gateway_lib.Config(argv[1])
    asyncio.get_event_loop().run_until_complete(main(conf))
