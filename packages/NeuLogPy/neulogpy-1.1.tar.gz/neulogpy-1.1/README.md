
# NeuLogPy loggin module

This project provides a Python-based framework for managing and interacting with NeuLog sensors. It includes functionalities for setting up sensor experiments, retrieving and storing sensor data, and visualizing real-time data.

## Project Structure

```
packaging
├── config
│   ├── sensors.yaml             # Configuration file with sensor definitions
├── core
│   ├── api_client.py            # API client for interacting with the NeuLog server
│   ├── services                 # Services for experiment and sensor management
│       ├── experiment_service.py   # Handles experiment setup, start, and stop
│       ├── sensor_service.py       # Manages sensor retrieval, addition, and listing
├── models
│   ├── sensor.py                # Pydantic models defining sensor schema
├── tests                        # Test suite
│   ├── core
│       ├── test_api_client.py   # Tests for the API client
│       ├── test_experiment_service.py  # Tests for experiment service
│       ├── test_sensor_service.py   # Tests for sensor service
├── utils
│   └── file_loader.py           # Utility function for loading YAML files
└── README.md                    # Project documentation
```

## Installation

To get started, clone this repository and install the required dependencies:

```bash
git clone <repository-url>
cd NeuLog
pip install -r requirements.txt
```

## Configuration

The `config/sensors.yaml` file defines the sensors available in the system. Each sensor has properties like `code`, `unit`, and `description`. Modify this file to add new sensors or update existing configurations.

Example structure of `sensors.yaml`:

```yaml
sensors:
  Temperature:
    code: "TEMP"
    unit: "°C"
    description: "Measures temperature"
  CO2:
    code: "CO2"
    unit: "ppm"
    description: "Measures carbon dioxide levels"
```

## Usage

### Starting an Experiment

To start a new experiment with specified sensors, use the `NeuLog` interface in `NeuLog.py`.

```python
from core.services.experiment_service import ExperimentService

# Example of setting up and starting an experiment
experiment_service = ExperimentService()
experiment_service.start_experiment(
    sensors=[("Temperature", "TEMP")],
    rate=8,
    samples=1000
)
```

### Real-Time Data Visualization

The `test.py` script includes a visualization example using Matplotlib. This script retrieves real-time data from a respiration sensor and plots it dynamically.

```bash
python test.py
```

This script initializes an experiment, collects data samples, and plots them in real time. Modify parameters like `sensor_type`, `sensor_id`, `rate`, and `samples` within `test.py` to customize the experiment.

### Combining Files

To generate a single combined Python file with the directory structure and content, run `combiner.py`:

```bash
python scripts/combine_files.py
```

This will output a `combined_module.py` file containing all the code and directory comments for easy review.

## Running Tests

Tests are organized in the `tests` directory and use the `pytest` framework. To run the tests, use:

```bash
pytest tests/
```

Tests include:
- **API client tests** to verify interaction with the NeuLog server.
- **Sensor and Experiment service tests** to check sensor management and experiment lifecycle functionality.

## Key Modules

- **core/api_client.py**: Manages HTTP requests to the NeuLog API.
- **core/services/experiment_service.py**: Configures and manages experiments.
- **core/services/sensor_service.py**: Manages sensor registry and metadata.
- **models/sensor.py**: Defines sensor schema and validation.
- **utils/file_loader.py**: Loads YAML configurations for sensor metadata.

## Contributing

Contributions are welcome! Please open issues to discuss potential improvements or submit pull requests.

---

## License

This project is licensed under the MIT License.

