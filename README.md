# Nyx MA Extension - Support of Multi-Agent PDDL files and visualization

## **Motivation for Research**
We aim to solve multi-agent planning problems in a PDDL+ domain, which includes:

* Numeric variables
* Temporal actions
* Durative actions

To address these challenges, we use Nyx, a planner that supports solving such problems.
With minor modifications to the code, our framework can also support other planners that handle subsets of these features, such as Metric-FF, which solves problems in PDDL 2.1.

You can find the original Nyx code [here](https://gitlab.com/wmgp9/nyx/-/tree/main?ref_type=headse=heads).

## **System requirements**
* Python less than 3.13 (version 3.11 is good enough)
* Install the requirements of the project:
```Shell
python3 -m pip install -r requirements.txt 
```

## **How to run**
### By shell:
* You have to be on the root folder [nyx-extenstion](nyx-extension)
* Run the following command:
```Shell
python3 -m UI.gui
```
### Optional:
  * You can also run the [gui.py](gui.py) file manually in your IDE.

## **PDDL+ files structure:**
  * Supports all the functionality NYX is supporting.
  * Agents should be defined under private section of objects.
  * You can look for examples [here](MA_PDDL/examples/).


## **Project Structure**

### **1. [MA_PDDL](MA_PDDL) - Multi-Agent PDDL Components**
- **[examples](MA_PDDL/examples/)**: Contains examples of multiple domain, problem and config files.
  - **[Blocks](MA_PDDL/examples/Blocks/)**
  - **[Car](MA_PDDL/examples/Car/)**
  - **[Minecraft](MA_PDDL/examples/Minecraft/)**
- **[outputs](MA_PDDL/outputs/)**: Stores MA plans processed by Nyx.
- **[MAtoSA.py](MA_PDDL/MAtoSA.py)**: Converts Multi-Agent PDDL files into Single-Agent PDDL files.

---

### **2. [UI](UI) - Graphical User Interface**
- **[img](UI/img/)**: Stores images used in the GUI (e.g., icons, backgrounds).
- **[gui.py](UI/gui.py)**: Main GUI runner.

---

### **3. [VIS](VIS) - Visualization Components**

- **[ActionsParser.py](VIS/SA_VIS/ActionsParser.py)**  
  - Parses actions in single-agent simulations.
- **[SA_Simulator.py](VIS/SA_VIS/SA_Simulator.py)**  
  - Generic simulator for single-agent planning.
- **[InitParser.py](VIS/SA_VIS/InitParser.py)**  
  - Parses initial state configurations.
- **[VisController.py](VIS/SA_VIS/VisController.py)**  
  - Manages visualization controls for SA and MA simulations.

#### **📌 Single-Agent Visualization ([SA_VIS](VIS/SA_VIS/))**
- **[CarSimulator](VIS/SA_VIS/CarSimulator/)**  
  - **[resources](VIS/SA_VIS/CarSimulator/resources/)**: Stores assets for the car simulator.
  - **[Car.py](VIS/SA_VIS/CarSimulator/Car.py)**: Defines car object properties and behavior.
  - **[CarSimulator.py](VIS/SA_VIS/CarSimulator/CarSimulator.py)**: Manages the car simulation process.
  - **[CarWindow.py](VIS/SA_VIS/CarSimulator/CarWindow.py)**: Handles the visualization for car simulation.

- **[SleepingBeautySimulator](VIS/SA_VIS/SleepingBeautySimulator/)**  
  - **[resources](VIS/SA_VIS/SleepingBeautySimulator/resources/)**: Stores assets for the Sleeping Beauty simulator.
  - **[SleepingBeauty.py](VIS/SA_VIS/SleepingBeautySimulator/SleepingBeauty.py)**: Defines Sleeping Beauty domain logic.
  - **[SleepingBeautySimulator.py](VIS/SA_VIS/SleepingBeautySimulator/SleepingBeautySimulator.py)**: Manages the Sleeping Beauty simulation.
  - **[SleepingBeautyWindow.py](VIS/SA_VIS/SleepingBeautySimulator/SleepingBeautyWindow.py)**: Handles the visualization for the Sleeping Beauty simulation.

#### **📌 Multi-Agent Visualization ([MA_VIS](VIS/MA_VIS/))**
- **[BlocksSimulator](VIS/MA_VIS/BlocksSimulator/)**  
  - **[resources](VIS/MA_VIS/BlocksSimulator/resources/)**: Stores assets (e.g., `table.png`, `hand.png`).
  - **[BlocksWindow.py](VIS/MA_VIS/BlocksSimulator/BlocksWindow.py)**: Manages the Blocks Simulation visualization.
