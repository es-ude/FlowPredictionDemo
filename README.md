# FlowPredictionDemo
Predicting the strength of water flow based on water levels at three locations. This repo is intended to serve as a demo for our ElasticAI pipeline.


## Setup virtual environment via poetry

In case you have poetry not installed:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
(We have tested poetry version 1.8.3)

Now install virtual environment via:
```bash
poetry install
```

## Workflow

### Train neural network and generate ENv5 firmware in Python
1. Run flowpredictiondemo/main.py
2. Run the autobuild_bin_file_*.sh
3. Wait for programs to return
4. Generate the stub:
```
python -m elasticai.stubgen.main flow_prediction
```
---
As alternatives to steps `2.` and `3.`, you have the option to create your own Vivado project. Our VHDL code is not compatible with the latest version of Vivado; however, it has been successfully tested on version 2020.1. Begin by selecting the appropriate FPGA model(xc7s15ftgb196-2) during the project setup. Next, incorporate the `src` and `constraints` folders into your project. This process will allow you to synthesize and implement the bitstream successfully.

I've prepared an example project within the `vivado_proj` folder. It may not function directly on your PC, but it serves as a valuable resource for understanding the setup process, enabling you to create your own project accordingly. Furthermore, I suggest launching Vivado and using the `cd` command in the TCL console to navigate to the `vivado_proj` folder. Subsequently, run the command `source example_project.tcl` to automatically generate the Vivado project. (Note: My script is tailored to automatically include source files and select the correct FPGA models.)

Please ensure that you have transferred the `src` and `constraints` folders from your output directory to `vivado_proj` before executing this command.

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
