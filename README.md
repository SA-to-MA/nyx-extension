# Nyx MA Extension - Support of Multi-Agent PDDL files and visualization

# **Motivation for Research**
We aim to solve multi-agent planning problems in a PDDL+ domain, which includes:

* Numeric variables
* Temporal actions
* Durative actions

To address these challenges, we use Nyx, a planner that supports solving such problems.
With minor modifications to the code, our framework can also support other planners that handle subsets of these features, such as Metric-FF, which solves problems in PDDL 2.1.

You can find the original Nyx code [here](https://gitlab.com/wmgp9/nyx/-/tree/main?ref_type=headse=heads).

# **System requirements**
* Python less than 3.13 (version 3.11 is good enough)
* Install the requirements of the project:
```Shell
python3 -m pip install -r requirements.txt 
```

# **How to run**
## By shell:
* You have to be on the root folder [nyx-extenstion](nyx-extension)
* Run the following command:
```Shell
python3 -m UI.gui
```
## Optional:
  * You can also run the [gui.py](gui.py) file manually in your IDE.

## **PDDL+ files structure:**
  * Supports all the functionality NYX is supporting.
  * The way agents are defined varies between sequential and parallel execution modes.
  * You can look for examples [here](MA_PDDL/examples/).


# **Project Structure**

## **1. [MA_PDDL](MA_PDDL) - Multi-Agent PDDL Components**
- **[examples](MA_PDDL/examples/)**: Contains examples of multiple domain, problem and config files. Each domain includes both MA examples of parallel run and sequential run (under 'seq' directory of each domain).
  - **[Blocks](MA_PDDL/examples/Blocks/)**
  - **[Car](MA_PDDL/examples/Car/)**
  - **[Minecraft](MA_PDDL/examples/Minecraft/)**
- **[outputs](MA_PDDL/outputs/)**: Stores MA plans processed by Nyx.
- **[MAtoSA.py](MA_PDDL/MAtoSA.py)**: Converts Multi-Agent PDDL files into Single-Agent PDDL files.
- **[Deduplicate.py](MA_PDDL/Deduplicate.py)**: Performs deduplication of actions in PDDL domain files.

---

## **2. [heuristic_functions.py](heuristic_functions.py) - Heuristics**
This file contains heuristics from [ActionBasedNovelty](https://github.com/SPL-BGU/ActionBasedNovelty). You can see instructions from their readme file and add the necessary flags to your **config** file when running the solver.

---

## **3. [UI](UI) - Graphical User Interface**
- **[img](UI/img/)**: Stores images used in the GUI (e.g., icons, backgrounds).
- **[gui.py](UI/gui.py)**: Main GUI runner.

---

## **4. [VIS](VIS) - Visualization Components**
- **[Agent.py](VIS/Agent.py)**  
  - Class of Agent object.
- **[InitParser.py](VIS/SA_VIS/InitParser.py)**  
  - Parses initial state configurations.
- **[SolutionParser.py](VIS/SA_VIS/InitParser.py)**  
  - Parses output of solution plan from NYX.
- **[VisController.py](VIS/SA_VIS/VisController.py)**  
  - Manages visualization controls for SA and MA simulations.

### **📌 Search Tree Visualization ([Search_VIS](VIS/Search_VIS/))**
  - **[resources](VIS/Search_VIS/resources/)**: Stores assets (e.g., `car.png`, `background.png`).
  - **[search_tree](VIS/Search_VIS/search_tree/)**: Stores the search tree pkl files.
    - **[ChunkedTreeViewer.py](VIS/Search_VIS/search_tree/ChunkedTreeViewer.py)**: Manages the visualization of search trees.
    - <**Domain name**>Tree: Visualization of the state represented by a node in a search tree for specific domain.

### **📌 Single-Agent Visualization ([SA_VIS](VIS/SA_VIS/))**
- **[SleepingBeautySimulator](VIS/SA_VIS/SleepingBeautySimulator/)**

### **📌 Multi-Agent Visualization ([MA_VIS](VIS/MA_VIS/))**

- **[BlocksSimulator](VIS/MA_VIS/BlocksSimulator/)**
- **[CarsSimulator](VIS/MA_VIS/CarsSimulator/)** 
- **[MinecraftSimulator](VIS/MA_VIS/MinecraftSimulator/)** 

Each directory includes:
  - **[resources](VIS/MA_VIS/BlocksSimulator/resources/)**: Stores assets (e.g., `table.png`, `hand.png`).
  - **Simulator class**: Manages the simulation visualization.

## 🧩 Adding Visualization for a New Domain

You can simulate and visualize any custom domain by following the steps below. The **existing domains** are just an example — feel free to create your own domain with different objects, agents, actions, and logic.

---

### 1. Create PDDL Files for Your Domain

Prepare the following:

- `domain.pddl`: defines predicates and actions for your custom domain.
- `problem.pddl`: defines `:objects` for items, the `:init` state, and a `:goal`.
If you run in parallel mode, you need to put agents under `:private` section. If you run in sequential mode, you need to define your agents as objects of type `agent`.


📁 Recommended file structure:
```
examples/YourDomain/
├── domain.pddl
└── problem.pddl
```

---

### 2. Implement Visualization & Simulation Classes

Duplicate the example simulation file (`BlocksSimulation.py`) and modify it:

Update the following:

- Visualization logic: rename and adapt classes in simulator example files to suit your objects and agents.
- Action logic: in the agent's `execute()` method, implement how each action affects object state and visualization.
- Drawing logic: render your objects with custom images, shapes, or positions.

---

### 3. Run Your Domain

To integrate and run your custom domain using the simulator and GUI, follow these steps:

Update `VisController.py`:
- Import your simulator file.
- Update `main(...)` to include running option for your simulator.

  Example:
  ```python
  from PathToYourDomainSimulator import YourDomainSimulator
  ...
  def main(...):
      ...
      ...
      elif selected_domain == "YourDomain":
        simulator = YourDomainSimulator(...)

Update `gui.py`:

Add your domain to the supported list  
At the top of `gui.py`, update the `SUPPORTED_DOMAINS` list to include your domain:

```python
SUPPORTED_DOMAINS = ["Blocks", "Car", "Sleeping Beauty", "Other", "YourDomain"]
```

This ensures your domain appears in the dropdown menu under both the **"Solve"** and **"Visualize"** tabs in the GUI.

> ⚠️ No further GUI code changes are needed — once added to the list, your domain will be passed automatically to the `run()` function in `VisController.py`.


After this, your new domain will be selectable and runnable directly through the GUI.

---

### 5. (Optional) Add Resources

If your simulation includes images, add them to a folder named `resources/`:

```
resources/
├── background.png
├── agent.png
├── item.png
```

Then load them using:

```python
img_path = os.path.join("resources", "background.png")
```
---

## 🌳 Adding Search Tree Visualization for a New Domain

To visualize the search tree for a new domain, follow these steps.

### 1. Enable Domain-Specific Rendering

Open `ChunkedTreeViewer.py` and do the following:

- **Add a parser for your domain’s state format**

Just like `parse_block_state()` or `parse_car_state()`, write a new function:

```python
def parse_your_domain_state(state_vars):
    # Example: Parse state_vars (dictionary) into structured domain-specific info
    parsed = {}
    for raw_key, value in state_vars.items():
        # logic for interpreting keys like "['holding', 'agent1']"
        ...
    return parsed
```

- **Add a rendering function for the visual overlay**

Copy one of the existing rendering functions like `render_blocks_domain(...)`, and adjust it for your domain:

```python
def render_your_domain(node, surface, font, res_dir, width, height):
    state_vars = getattr(node.state, "state_vars", {})
    parsed_state = parse_your_domain_state(state_vars)

    # Draw background or images
    ...

    # Draw agents, objects, relations, etc.
    ...
```

- **Register your domain in `show_node_info(...)`**

Update the `show_node_info` function to call your renderer:

```python
def show_node_info(node):
    ...
    if DOMAIN == "blocks":
        render_blocks_domain(...)
    elif DOMAIN == "car":
        render_car_domain(...)
    elif DOMAIN == "yourdomain":
        render_your_domain(...)
```

---

### 2. Set the Domain When Calling the Viewer

Make sure your domain name is passed correctly to the `main(...)` function:

```python
from VIS.Search_VIS import ChunkedTreeViewer
ChunkedTreeViewer.main("yourdomain")
```

This is already integrated in the GUI — so just ensure the string matches what you check inside `show_node_info()`.

---

### 3. Submit the Following

When adding search tree support for a new domain, make sure to submit:

- A `parse_your_domain_state()` function
- A `render_your_domain()` function
- A `DOMAIN == "yourdomain"` case inside `show_node_info(...)`
- Optional background images or icons inside `resources/`

> Example: `resources/table.png`, `resources/car.png`, etc.

## Your domain is now ready to be visualized!

---