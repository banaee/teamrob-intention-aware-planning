# TeamRob Intention-Aware Planning Framework

Separating cognitive algorithms (IR + Planning) from simulator implementations (Mesa + ROS).

## Structure

- `shared/` - Simulator-agnostic cognitive layer
- `mesa_sim/` - Mesa embodiment (discrete simulation)
- `ros_sim/` - ROS embodiment (real-world deployment)
- `configs/` - YAML task definitions

### workflow overview

### xxx

## Pre-Requisites

### Set Up VE, Activate, and Install Dependencies (later can be containerized with Docker or Apptainer)

```bash
python3 -m venv home/python-ens/tr-env
source home/python-ens/tr-env/bin/activate
pip install -r requirements.txt
```

### Generate Domain Configuration

The simulation requires a domain configuration file that defines the environment layout (shelves, items, zones, etc.).

**If `configs/domain.yaml` does not exist, generate it:**

```bash
# Option 1: Generate test domain (hardcoded test data)
python3 scripts/domain_assembler.py

# Option 2: Parse from Gazebo export (when available)
python3 scripts/domain_assembler.py --input scripts/gazebo_export.json
```

**Output:** `configs/domain.yaml`

**Note:** For initial testing, Option 1 generates a minimal test environment. Once you have a Gazebo world export, use Option 2 to generate the domain from actual simulation data.

## Running Simulations

### Mesa Simulation

blah blah.