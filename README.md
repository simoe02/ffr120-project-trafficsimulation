# Traffic simulation of Gothenburg road network
Course project in the course FFR120 Simulation of Complex Systems. Traffic is simulated using real world road data from Gothenburg, Sweden (data supplied by Trafikverket at https://lastkajen.trafikverket.se/). Vehicles are simlated with car following logic, A* routing and individual behavior parameters. Data of congestion metrics is captured during simulation and can be analysed and visualised in plots.


## Repository layout

The code expects to be run **as modules from the repo root**, using cross-folder absolute imports. Organize the provided files like this:

```
ffr120-project-trafficsimulation/
├── data/sim_data/              # Data generated from simulation runs stored here
├── data_analysis/              # Code for data analysis and plotting
├── driver_behavior
│   ├── router.py               # A-star routing
│   └── vehicle.py              # Vehicle logic
├── network
│   ├── intersection.py     
│   ├── network.py              # Road network graph implementation (uses intersection.py and road.py as building blocks)
│   ├── road.py
│   └── road_data
│       ├── data.gpkg           # Data from Trafikverket
│       ├── gpkg_to_json.py
│       └── create_sub_data.py  # Creates smaller road networks from box coordinates
├── simulation.py               # Main simulation
├── visualizer.py               # PyQtGraph visualization
└── main.py                     # Main program for running simulation
```

## Setup

### 1. Dependencies

Dependencies are declared in `pyproject.toml` (requires Python ≥ 3.14). Install with [`uv`](https://docs.astral.sh/uv/):

```bash
uv sync
```

Or with pip:

```bash
pip install -e .
```


### 2. Using PyPy3

For faster runtime, use PyPy3 interpreter (installed seperately at https://pypy.org). Note that PyPy does not support PyQtGraph, so it cant be run with visalisation.


## Usage

### Running simulation
Run simulation with `run_simulation()` (for data collection) or `run_with_visualisation()` (for cool visualisation) in `main.py`. Saved data can be analysed and plotted with programs in `data_analysis/`.