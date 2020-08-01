"""
main() for Habitat Engineering, a program for control of Habitat and AYSE
subsystems, electrical power distribution, and thermal loading.

Communicates to orbitx with GRPC.
"""

import argparse
import logging
import random
import time

import grpc

from orbitx import common
from orbitx import physics
from orbitx import network
from orbitx import programs
from orbitx.graphics.compat_gui import StartupFailedGui
from orbitx.graphics.eng_gui import MainApplication
from orbitx.graphics.tkinter_style import Style
from orbitx.strings import HABITAT


log = logging.getLogger()


name = "Habitat Engineering"

description = (
    "Control Habitat and AYSE subsystems, electrical power distribution, and"
    "thermal loading."
)

argument_parser = argparse.ArgumentParser(
    'habeng', description=description.replace('<br />', '\n'))
argument_parser.add_argument(
    "--physics-server", default="localhost",
    help=(
        'Network name of the computer where the physics server is running. If '
        'the physics server is running on the same machine, put "localhost".')
)


def main(args: argparse.Namespace):
    orbitx_connection = network.StateClient(
        network.Request.HAB_ENG, args.physics_server)
    log.info(f'Connecting to OrbitX Physics Server: {args.physics_server}')

    try:
        # Make sure we have a connection before continuing.
        orbitx_connection.get_state(
            [network.Request()])
    except grpc.RpcError as err:
        log.error(f'Could not connect to Physics Server: {err.code()}')
        StartupFailedGui(args.physics_server, err)
        return

    server_state = orbitx_connection.get_state()
    physics_engine = physics.PhysicsEngine(server_state)

    def update():
        state = physics_engine.get_state()
        gui.update_labels(state[HABITAT].pos[0])
        gui.after(int(1000 / common.FRAMERATE), update)

    gui = MainApplication(Style('flat'))
    update()
    gui.mainloop()

    random.seed()

    try:
        while True:
            print(random.choice(['ASTRONAUT STATUS: DYING',
                                 'astronaut status: okay']))
            print(orbitx_connection.get_state(
                  [network.Request()])['Earth'].pos)
            time.sleep(1)
    except grpc.RpcError as err:
        log.error(
            f'Got response code {err.code()} from orbitx, shutting down')


program = programs.Program(
    name=name,
    description=description,
    main=main,
    argparser=argument_parser
)
