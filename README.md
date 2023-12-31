# FlowPredictionDemo
Predicting the strength of water flow based on water levels at three locations. This repo is intended to serve as a demo for our ElasticAI pipeline.


## Setup virtual environment via poetry

In case you have poetry not installed:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Now install virtual environment via:
```bash
poetry install
```

## Workflow

### Train neural network and generate ENv5 firmware in Python
1. Run flowpredictiondemo/main.py
3. Run the autobuild_bin_file_*.sh
4. Wait for programs to return
5. Generate the stub:
```
python -m elasticai.stubgen.main flow_prediction
```

### C-Runtime
6. Clone or fork [elasticAi.runtime.env5-base-project](https://github.com/es-ude/enV5-base-project)
7. Develop your own application in that repository
8. Include generated stub files in project and as a library in CMakeLists.txt
9. Follow build instructions from [elasticAi.runtime.env5-base-project](https://github.com/es-ude/enV5-base-project)

### Hardware test
9. Power on the board
10. Flash the RP2040
11. Depending on your application the binfile ...
    1. is flashed by you via MQTT and HTTP-Get. Make sure to provide the file with a HTTP server.
    2. can be flashed via USB by yourself.
12. Now the device should work like your application says!
