from dataclasses import dataclass
import torch


@dataclass(frozen=True)
class Normalizer:
    minimum: float
    maximum: float

    @staticmethod
    def from_data(data: torch.Tensor) -> "Normalizer":
        return Normalizer(minimum=float(data.min()), maximum=float(data.max()))

    def normalize(self, data: torch.Tensor) -> torch.Tensor:
        return (data - self.minimum) / (self.maximum - self.minimum)

    def rescale(self, data: torch.Tensor) -> torch.Tensor:
        return data * (self.maximum - self.minimum) + self.minimum
