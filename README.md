# FlowPredictionDemo
Predicting the strength of water flow based on water levels at three locations. This repo is intended to serve as a demo for our ElasticAI pipeline.


## Setup Virtual-Environment via poetry

In case you have peotry not installed
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Now install virtual environment via 
```bash
poetry install
```

## Workflow

### Python
1. Go in flow
2. Execute main.py
3. Execute the autobuild_bin_file_.sh
4. Wait for files to return
5. Generate the stub
```
python -m elasticai.stubgen.main flow_prediction
```

### C-Runtime
6. Clone [elasticAi.runtime.env5repo](https://github.com/es-ude/enV5-base-project)
7. Build your own application in the repository
8. Include generated stub files in project and CMakeList

### Hardware test
9. Power on the board
10. Flash the RP2040
11. Depending on your application the binfile ...
    1. is flashed by you via MQTT and HTTP-Get. Make sure to provide the file with a HTTP-server.
    2. can be flashed via USB by yourself.
12. Now the device should work like your application says. 


