#!/usr/bin/env python3

import os
import time
import rrdtool
import thermopi

rrdb = "/usr/share/thermopi/temperature.rrd"
output = "/var/www/html/thermopi/temperature.png"

# temp1 == Environment
# temp2 == Meat

def create_rrd():
    return rrdtool.create(file, "--step", "300", 
        "DS:temp1:GAUGE:900:0:300", 
        "DS:temp2:GAUGE:900:0:300", 
        "RRA:MAX:0.5:1:288")

def update_rrd():
    return rrdtool.update(file, "N:%s:%s" % thermopi.get_temp())

def graph_rrd():
    return rrdtool.graph("/var/www/html/thermopi/temperature.png", 
        "--start", "-6h", 
        "--vertical-label=Temperature (C)",
        "-w 640",
        "DEF:temp1=%s:temp1:MAX" % file,
        "DEF:temp2=%s:temp2:MAX" % file,
        "AREA:temp1#0000ffdd:Grill",
        "GPRINT:temp1:LAST:Current\:%3.1lf C %s",
        "GPRINT:temp1:AVERAGE:Average\:%3.1lf C %s",
        "GPRINT:temp1:MAX:Maximum\:%3.1lf C %s\\n",
        "LINE1:temp2#ff0000:Meat",
        "GPRINT:temp2:LAST: Current\:%3.1lf C %s",
        "GPRINT:temp2:AVERAGE:Average\:%3.1lf C %s",
        "GPRINT:temp2:MAX:Maximum\:%3.1lf C %s\\n",
        )

if __name__ == "__main__":
    if not os.path.exists(file):
        create_rrd()

    update_rrd()
    graph_rrd()

