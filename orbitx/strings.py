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
RADS_BATT = 'RADS_BATT'
AGRAV = 'A GRAV'    # Artificial gravity

HAB_REACT = 'HAB reactor'
RCON1 = 'R-CON1'    # Habitat Reactor Confinement
RCON2 = 'R-CON2'    # Habitat Reactor Confinement
RCON_BATT = 'RCON_BATT'
REACT_INJ1 = 'INJ1'   # Habitat Reactor: Fuel Injector
REACT_INJ2 = 'INJ2'   # Habitat Reactor: Fuel Injector

AYSE_REACT = 'AYSE reactor'

INJ1 = 'INJ1'    # Habitat Engines: Fuel Injector
INJ2 = 'INJ2'    # Habitat Engines: Fuel Injector
ION1 = 'ION1'       # Habitat Engine: Ionizer
ION2 = 'ION2'       # Habitat Engine: Ionizer
ION3 = 'ION3'       # Habitat Engine: Ionizer
ION4 = 'ION4'       # Habitat Engine: Ionizer
ACC1 = 'ACC1'       # Habitat Engine: Accelerator
ACC2 = 'ACC2'       # Habitat Engine: Accelerator
ACC3 = 'ACC3'       # Habitat Engine: Accelerator
ACC4 = 'ACC4'       # Habitat Engine: Accelerator
RCSP = 'RCSP'       # Reaction Control System Power
GPD1 = 'GPD1'
GPD2 = 'GPD2'
GPD3 = 'GPD3'
GPD4 = 'GPD4'

TRN1 = 'TRN1'       # Transformer: HabBus1 to HabBus2
TRN2 = 'TRN2'       # Transformer: HabBus2 to HabBus3
BUS1 = 'Habitat Main Bus'
BUS2 = '2nd Bus'
BUS3 = '3rd Bus'       # HabBus3 (Life Support + Critical)
BUSA = 'AYSE_BUS'

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

# Radiator States
ISOLATED = 'ISOL'
BROKEN = 'BRKN'
STOWED = 'STWD'
LOOP1 = 'HLP1'
LOOP2 = 'HLP2'
LOOP3 = 'ALP3'
BOTH = 'BOTH'

A_MASTER = 'MASTER ALARM'     # Master Alarm Alert
A_ASTEROID = 'ASTEROID'       # Asteroid Alert
A_RADIATION = 'RADIATION'     # Radiation Alert
A_DOCKED = 'DOCKED'
A_ATMO = 'IN ATMO'
A_OVERTEMP = 'OVERTEMP'
A_LOWBATT = 'LOW BATT'

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
    GPD1,
    GPD2,
    GPD3,
    GPD4,
    TRN1,
    BUS1,
    BUS2,
    BUS3,
    BUSA,
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
    LP1,
    LP2,
    LP3,
    RADS_BATT,
    RCON_BATT
]

SMALL_COMPONENTS_NAMES = [    # Temp for testing
    HAB_REACT,
    ION1,
    ION2,
    ION3,
    ION4,
    LP1
]