# Nyx Extension - Support also Multi-Agent files and visualization

The original nyx repository: https://gitlab.com/wmgp9/nyx/-/tree/main?ref_type=headse=heads

## **What do you need for start**
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

## **Project Structure**

### **1. [MA_PDDL](MA_PDDL) - Multi-Agent PDDL Components**
- **[examples](MA_PDDL/examples/)**  
  - **[Blocks](MA_PDDL/examples/Blocks/)**: Contains 4 domains and 4 problems for multi-agent planning.
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
