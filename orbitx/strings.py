"""Symbols representing commonly used strings.
Feel free to `from strings import *`, your linter might not like you though."""

HABITAT = 'Habitat'
AYSE = 'AYSE'
SUN = 'Sun'
EARTH = 'Earth'
MODULE = 'Module'
SUN = 'Sun'
OCESS = 'OCESS'

# Subsystems
RADS1 = 'RAD-S1'    # Radiation shielding
RADS2 = 'RAD-S2'    # Radiation shielding
AGRAV = 'A GRAV'    # Artificial gravity

HAB_REACT = 'HAB reactor'
RCON1 = 'R-CON1'    # Habitat Reactor Confinement
RCON2 = 'R-CON2'    # Habitat Reactor Confinement
REACT_INJ1 = 'REACT INJ1'   # Habitat Reactor: Fuel Injector
REACT_INJ2 = 'REACT INJ2'   # Habitat Reactor: Fuel Injector

AYSE_REACT = 'AYSE reactor'

INJ1 = 'INJECTOR 1'    # Habitat Engines: Fuel Injector
INJ2 = 'INJECTOR 2'    # Habitat Engines: Fuel Injector
ION1 = 'ION1'       # Habitat Engine: Ionizer
ION2 = 'ION2'       # Habitat Engine: Ionizer
ION3 = 'ION3'       # Habitat Engine: Ionizer
ION4 = 'ION4'       # Habitat Engine: Ionizer
ACC1 = 'ACC1'       # Habitat Engine: Accelerator
ACC2 = 'ACC2'       # Habitat Engine: Accelerator
ACC3 = 'ACC3'       # Habitat Engine: Accelerator
ACC4 = 'ACC4'       # Habitat Engine: Accelerator
RCSP = 'RCSP'       # Reaction Control System Power

TRN1 = 'TRN1'       # Transformer: HabBus1 to HabBus2
TRN2 = 'TRN2'       # Transformer: HabBus2 to HabBus3
BUS3 = 'BUS3'       # HabBus3 (Life Support + Critical)

BAT = 'BAT'         # Battery - HB2, HB3, AB
COM = 'COM'         # Communications
FCELL_INJ = 'F-CELL INJ'    # Habitat Fuel Cell: Fuel Injector

DETACH_MOD = 'DETACH MOD'   # Detach science module
DOCK_MOD = 'DOCK MOD'       # Dock science module
RADAR = 'RADAR'
INS = 'INS'                 # Inertial Navigation System
DEPLY_PAK = 'DEPLY PAK'     # Deploy science module
ACTVT_PAK = 'ACTVT PAK'     # Activate science module

GNC = 'GNC'                 # Guidance, Navigation & Control
LOS = 'LOS'                 # Line of Sight
SRB = 'SRB'                 # Solid Rocket Booster
CHUTE = 'CHUTE'             # Parachute
PLS = 'PLS'
CNT = 'CNT'

DUMP = 'DUMP'               # Dump Fuel
LOAD = 'LOAD'               # Load Fuel

LP1 = 'LP-1'                # Coolant Loop 1 - Habitat
LP2 = 'LP-2'                # Coolant Loop 1 - Habitat
LP3 = 'LP-3'                # Coolant Loop 1 - Habitat

A_MASTER = 'MASTER ALARM'     # Master Alarm Alert
A_ASTEROID = 'ASTEROID'       # Asteroid Alert
A_RADIATION = 'RADIATION'     # Radiation Alert

COMPONENT_NAMES = [
    RADS1,
    RADS2,
    AGRAV,
    RCON1,
    RCON2,
    ACC1,
    ION1,
    ACC2,
    ION2,
    ACC3,
    ION3,
    ACC4,
    ION4,
    TRN1,
    BUS3,
    TRN2,
    BAT,
    RCSP,
    COM,
    HAB_REACT,
    INJ1,
    INJ2,
    REACT_INJ1,
    REACT_INJ2,
    FCELL_INJ,
    AYSE_REACT,
    DETACH_MOD,
    DOCK_MOD,
    RADAR,
    INS,
]

SMALL_COMPONENTS_NAMES = [    # Temp for testing
    HAB_REACT,
    ION1,
    ACC1,
    LP1
]