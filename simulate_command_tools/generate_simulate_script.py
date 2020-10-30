#!/bin/python
# main function of this script: generate simulate_command according to parameters list and output txt.
# [command]
# name = simulate_storcli.py
# [part]
# [[part.1]]
# param = show ctrlcount
# result = show_ctlcount_res.txt
# [[part.2]]
# param = /c0 show all
# result = c0_show_all_res.txt
# [[part.3]]
# param = /c0 show events filter=critical,fatal
# result = c0_show_events_filter_res.txt

import os
import sys
import configobj

simulate_config_file = "simulate.conf"
simulate_config = configobj.ConfigObj(simulate_config_file)

str_arr = []

for part in simulate_config['part']:
    param = simulate_config['part'][part]['param']
    result = simulate_config['part'][part]['result']
    if not os.path.exists(result):
        print("file %s is not exists!" % result)
        sys.exit(1)
    f = open(result, "r")
    context = f.read()
    f.close()
    str_arr.append(param)
    str_arr.append(context)

f = open(simulate_config['command']['name'], "w")

simulate_storcli_context = """
import sys
if __name__ == '__main__':
"""

for i in range(0, len(str_arr), 2):
    simulate_storcli_context += """
    if \" \".join(sys.argv[1:]) == \"%s\":
        print \"\"\"%s\n\"\"\"
        sys.exit(0)
    """ % (str_arr[i], str_arr[i+1])

f.write(simulate_storcli_context)