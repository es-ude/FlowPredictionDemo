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
---
As alternatives to steps `2.` and `3.`, you have the option to create your own Vivado project. Our VHDL code is not compatible with the latest version of Vivado; however, it has been successfully tested on version 2020.1. Begin by selecting the appropriate FPGA model(xc7s15ftgb196-2) during the project setup. Next, incorporate the `src` and `constraints` folders into your project. This process will allow you to synthesize and implement the bitstream successfully.

I've prepared an example project within the `vivado_proj` folder. It may not function directly on your PC, but it serves as a valuable resource for understanding the setup process, enabling you to create your own project accordingly. Furthermore, I suggest launching Vivado and using the `cd` command in the TCL console to navigate to the `vivado_proj` folder. Subsequently, run the command `source example_project.tcl` to automatically generate the Vivado project. (Note: My script is tailored to automatically include source files and select the correct FPGA models.)

Please ensure that you have transferred the `src` and `constraints` folders from your output directory to `vivado_proj` before executing this command.

4. Upload the generated bitstream to the FPGA, you may use vivado to do so or you can use [ElasticNodeBitstreamFlasher](https://github.com/SuperChange001/ElasticNodeBitstreamFlasher).

### C-Runtime

5. Generate the stub:
```
poetry update # make sure to have the latest version of elasticai-stubgen
python -m elasticai.stubgen.main flow_prediction
```
once the stub is generated, you can find two files in the root directory: `flow_prediction.h` and `flow_prediction.c`.

6. Copy them to the `src` directory, we have prepared scripts to auto build uf2 files for RP2040.

7. prepare submodules for building:
```
git submodule update --init --recursive
```
8. Build the project:
```
mkdir build && cd build
cmake ..
cmake --build . -j4 --clean-first
```
9. Upload `out/main.uf2` to the RP2040


Alternatively, you can use the generated stub files in the `env5-base-project`:
- Clone or fork [elasticAi.runtime.env5-base-project](https://github.com/es-ude/enV5-base-project)
- Develop your own application in that repository
- Include generated stub files in project and as a library in CMakeLists.txt
- Follow build instructions from [elasticAi.runtime.env5-base-project](https://github.com/es-ude/enV5-base-project)

### Hardware test
10. use screen to connect to the serial port of the RP2040
```
screen /dev/ttyACM0 # on linux, ttyACM0 can be different on your system

screen /dev/cu.usbmodem143401 # on mac
```
You will see outputs exactly like the following: 
```
[HWTEST-MIDDLEWARE: runTest] Trure: 38, Predicted: 40
[HWTEST-MIDDLEWARE: runTest] Trure: 38, Predicted: 40
[HWTEST-MIDDLEWARE: runTest] Trure: 38, Predicted: 40
[HWTEST-MIDDLEWARE: runTest] Trure: 63, Predicted: 65
[HWTEST-MIDDLEWARE: runTest] Trure: 63, Predicted: 65
[HWTEST-MIDDLEWARE: runTest] Trure: 63, Predicted: 65
```
Note: The predicted value can be different from the true value since the model on FPGA has quantization errors, plus the training process is random, so your model can be different from ours.

## What are the next steps?
- You can modify the `src/Main.c` to add more functionalities to the application or conduct more tests.
- You can modify the neural network model in `flowpredictiondemo/main.py` and re-run the training process.
- You change the training process, e.g., use more or fewer epochs, and the model's performance should be varied.
- You can change to a new dataset; maybe it provides more input data points, so you should also change the `flow_prediction.idl` accordingly.