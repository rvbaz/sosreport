### This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import os
import sos.plugintools
import glob

class sanitize(sos.plugintools.PluginBase):
    """ sanitize plugin
    """
    def defaultenabled(self):
        return False
    
    def setup(self):
        # sanitize ip's, hostnames in logs
        rhelver = self.policy().rhelVersion()
        if rhelver == 5 or rhelver == 4:
            logs=self.doRegexFindAll(r"^\S+\s+(\/.*log.*)\s+$", "/etc/syslog.conf")
        else:
            logs=self.doRegexFindAll(r"^\S+\s+(\/.*log.*)\s+$", "/etc/rsyslog.conf")
        for log in logs:
            self.doRegexSub(log, r"\s+(%s.*)" % (self.hostname,), r"\1sanitized-hostname")
            self.doRegexSub(log, r"([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})", r"\1sanitized-ip")