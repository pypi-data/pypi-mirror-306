# Description

Network Protocol Data Exfiltration Project Server - A modular approach for data exfiltration

# Installation

`pip install npdep_server`

# Usage

**From command line:**

`python -m npdep_server [-h] --config CONFIG [--logfile LOGFILE] [--purge PURGE]`

| Option | Short | Type | Default | Description |
|---|---|---|---|---|
|--config | -c | String | - | Path to Configuration File |
|--logfile | -l | String | . | Path to Log File |
|--purge | -u | String | - | The given path (all files/subfolders) will be wiped. npdep-server is not starting, if this options is given. |

# Configuration

```json
{
    "options":{
        "modulePath": "" // By providing a path, you can load modules not installed via pip
    },
    "modules": [
        {
            "name": "ExampleModule",   // Name of the module .py file located in ./src/receiver/module/*
            "options": {               // Custom options object for your specific module
                "port": 4567           // Example: Listen on port 4567
            }
        }
    ]
}
```

# Example

`python -m npdep_server -c config.json`

Given the previous configuration file `npdep_server` is going to start `ExampleModule` which is listening on port `4567`.