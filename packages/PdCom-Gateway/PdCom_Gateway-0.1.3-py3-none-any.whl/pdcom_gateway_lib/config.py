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

import libconf
import urllib
import urllib.parse


def fix_scheme(url):
    url = urllib.parse.urlparse(url)
    if url.scheme == "tcp":
        url = url._replace(scheme="msr")
    return url.geturl()


class Config:
    def __init__(self, conffile):
        with open(conffile) as f:
            self._config = libconf.load(f)

        self.rtserver = fix_scheme(self._config["rtserver"])
        self.modules = dict()
        if isinstance(self._config["modules"], str):
            module = self._config["modules"]
            self.modules[module] = self._config[module][0]
        else:
            for module in self._config["modules"]:
                self.modules[module] = self._config[module][0]
