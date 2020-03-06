#!/usr/local/bin/python3
'''
This script is used to upgrade software on Cisco Catalyst 3750 and 3650 switch stacks.
'''

import os, sys, time
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command


# Run show commands on each switch
def run_commands(task):
    print(f'{task.host}: running show comands.')
    # run "show version" on each host
    sh_version = task.run(
        task=netmiko_send_command,
        command_string="show dot1x all",
        use_textfsm=True,
    )

    print(run_commands.result)


def main():
  
    # initialize The Norn
    nr = InitNornir()
    # filter The Norn
    nr = nr.filter(platform="cisco_ios")
        # run The Norn run commands
    nr.run(task=run_commands)
    

if __name__ == "__main__":
    main()
