from pathlib import Path

import numpy as np

import torch
from torch.utils.data import Dataset


class FlowDataset(Dataset):
    def __init__(self, dataset_file: str | Path) -> None:
        super().__init__()
        self._data = torch.tensor(np.genfromtxt(dataset_file), dtype=torch.float32)

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, index) -> tuple[torch.Tensor, torch.Tensor]:
        return self._data[index, :-1], self._data[index, -1]
