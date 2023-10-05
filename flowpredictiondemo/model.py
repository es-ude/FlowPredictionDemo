from elasticai.creator.nn.sequential import Sequential
from elasticai.creator.nn.fixed_point import Linear
from elasticai.creator.nn.fixed_point import ReLU


class FlowPredictionModel(Sequential):
    def __init__(self, total_bits: int, frac_bits: int) -> None:
        super().__init__(
            Linear(
                in_features=3,
                out_features=10,
                bias=True,
                total_bits=total_bits,
                frac_bits=frac_bits,
            ),
            ReLU(total_bits=16),
            Linear(
                in_features=10,
                out_features=1,
                bias=True,
                total_bits=total_bits,
                frac_bits=frac_bits,
            ),
        )
