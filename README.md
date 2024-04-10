# Nyx - a new PDDL+ planner written in Python

Nyx is a PDDL+ parser and planner written in python with a focus on simplicity. It is a discretization-based planner that approximates the continuous system dynamics using uniform time steps (Δt) and step functions.


This work was initially based on the classical parser and planner written by PUCRS (https://github.com/pucrs-automated-planning/pddl-parser).

## Source
- [nyx.py](nyx.py): Main Runner
- [planner.py](planner.py): main planning loop and associated functions
- [PDDL.py](PDDL.py): PDDL parser
- [heuristic_functions.py](heuristic_functions.py): heuristic function definitions used in GBFS and A* Searches
- [simulator.py](simulator.py): (Work in Progress) PDDL+ plan simulator
- [semantic_attachments](semantic_attachments/):
  - [semantic_attachment.py](semantic_attachments/semantic_attachment.py): implementation of  semantic attachments (external functions)
- [syntax](syntax/) folder with PDDL object classes and supporting elements:
  - [action.py](syntax/action.py) 
  - [event.py](syntax/event.py) 
  - [process.py](syntax/process.py)
  - [state.py](syntax/state.py)
  - [visited_state.py](syntax/visited_state.py)
  - [constants.py](syntax/constants.py)
  - [plan.py](syntax/plan.py)
  - [trace.py](syntax/trace.py)
- [compiler](compiler/) folder with JIT compiler classes:
  - [JIT.py](compiler/JIT.py)
  - [HappeningMixin.py](compiler/HappeningMixin.py)
  - [preconditions_tree.py](compiler/preconditions_tree.py)
- [ex](ex/) folder with PDDL domains:
  - [Car](ex/car)
  - [Sleeping Beauty](ex/sleeping_beauty/)
  - [Cartpole](ex/cartpole/)
  - [Vending Machine](ex/vending_machine/)
  - [Powered Descent](ex/1D-powered-descent/)
  - [Convoys](ex/convoys_mt/)
  - [Linear Generator](ex/linear-generator/)
  - [Non-Linear Generator](ex/non-linear-generator/)
  - [Linear Generator (with processes)](ex/lg_process/)
  - [Solar Rover](ex/solar-rover/)
  - [Non-Linear Solar Rover](ex/non-linear-solar-rover/)
  - [Planetary Lander](ex/planetary/)
  - [Angry/Science Birds](ex/sb/)
  - [Non-Temporal](ex/non-temporal/) folder with non-temporal PDDL domains:
	  - [Dinner](ex/non-temporal/dinner/)
	  - [Blocks World](ex/non-temporal/blocksworld/)
	  - [Dock Worker Robot](ex/non-temporal/dwr/)
	  - [Travelling Salesman Problem](ex/non-temporal/tsp/)
    - [Driving](ex/non-temporal/driving/)
    - [Minecraft](ex/non-temporal/minecraft/)

## Planner execution
```Shell
python -B nyx.py ex/car/car.pddl ex/car/pb01.pddl -t:1
```

Planner options can also be stored in a config file.
```Shell
python -B nyx.py ex/car/car.pddl ex/car/pb01.pddl -config:"ex/car/car.config"
```

use flag ```-h``` for usage and planner option information.


## Custom heuristics and semantic attachments
To use custom heuristics, fill in the body of the heuristic_function method inside [heuristic_functions.py](heuristic_functions.py), assigning it an index, and running the planner with the '-custom_h:...' flag with the corresponding heuristic index. 
An example heuristic implementation and usage from the [cartpole](ex/cartpole/) domain: 

```
def heuristic_function(state):
    if constants.CUSTOM_HEURISTIC_ID == 1:
      h_val = math.sqrt(math.pow(state.state_vars["['x']"], 2) + math.pow(state.state_vars["['theta']"], 2) + \
                        math.pow(state.state_vars["['theta_dot']"], 2) + math.pow(state.state_vars["['x_dot']"], 2) + \
                        math.pow(state.state_vars["['theta_ddot']"], 2) + math.pow(state.state_vars["['x_ddot']"], 2)) * \
                        (state.state_vars["['time_limit']"] - state.state_vars["['elapsed_time']"])
      return h_val
```

```Shell
python -B nyx.py ex/cartpole/cartpole.pddl ex/cartpole/pb01.pddl -t:0.02 -dblevent -search:gbfs -custom_h:1
```

Semantic attachments can be used in the same manner as custom heuristics. Fill in the body of the external_function method in[semantic_attachment.py](semantic_attachments/semantic_attachment.py). When running the planner use flag '-sa:...' to specify which semantic attachment to activate. 

## Dependencies
- numba

## Current limitations of our planner
- No support for object subtypes
