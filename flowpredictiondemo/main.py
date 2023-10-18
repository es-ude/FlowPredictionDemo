from functools import partial

import torch
from elasticai.creator.file_generation.on_disk_path import OnDiskPath
from elasticai.creator.vhdl.system_integrations.firmware_env5 import (
    FirmwareENv5,
)

from elasticai.creator.nn.sequential import Sequential
from elasticai.creator.nn.fixed_point import Linear
from elasticai.creator.nn.fixed_point import ReLU
from elasticai.creator.nn.fixed_point import quantize

from flowpredictiondemo.training import prepare_data_and_train, OUTPUTS_DIR


class SWWrapperForQuantization(torch.nn.Module):
    def __init__(self, wrapped: Sequential):
        super().__init__()
        self.wrapped = wrapped
        self.total_bits = wrapped.total_bits
        self.frac_bits = wrapped.frac_bits
        self.quantization = partial(quantize, total_bits=self.total_bits, frac_bits=self.frac_bits)

    def forward(self, x):
        return self.quantization(self.wrapped(self.quantization(x)))


class FlowPredictionModel(Sequential):
    def __init__(self, total_bits: int, frac_bits: int) -> None:
        self.total_bits = total_bits
        self.frac_bits = frac_bits
        super().__init__(
            Linear(
                in_features=3,
                out_features=10,
                bias=True,
                total_bits=total_bits,
                frac_bits=frac_bits,
            ),
            ReLU(total_bits=total_bits),
            Linear(
                in_features=10,
                out_features=1,
                bias=True,
                total_bits=total_bits,
                frac_bits=frac_bits,
            ),
        )


def main() -> None:
    OUTPUTS_DIR.mkdir(exist_ok=True)

    model_for_hw = FlowPredictionModel(total_bits=8, frac_bits=6)
    model_for_training = SWWrapperForQuantization(model_for_hw)
    prepare_data_and_train(model_for_training)
    destination = OnDiskPath(name="build", parent=str(OUTPUTS_DIR))
    design = model_for_hw.create_design("network")
    design.save_to(destination.create_subpath("srcs"))
    firmware = FirmwareENv5(design, x_num_values=3, y_num_values=1, id=66)
    firmware.save_to(destination)


if __name__ == "__main__":
    main()
