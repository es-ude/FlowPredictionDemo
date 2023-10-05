from pathlib import Path

import torch
from torch.utils.data import random_split, TensorDataset, Dataset
import matplotlib.pyplot as plt

from elasticai.creator.file_generation.on_disk_path import OnDiskPath

from flowpredictiondemo.flow_dataset import FlowDataset
from flowpredictiondemo.model import FlowPredictionModel
from flowpredictiondemo.normalizer import Normalizer
from flowpredictiondemo.training import train

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DATA_DIR = Path("data")
OUTPUTS_DIR = Path("outputs")


def load_datasets(
    dataset_path: Path,
) -> tuple[TensorDataset, TensorDataset, Normalizer, Normalizer]:
    def normalize_dataset(
        ds: Dataset, sample_normalizer: Normalizer, label_normalizer: Normalizer
    ) -> TensorDataset:
        samples, labels = ds[:]
        return TensorDataset(
            sample_normalizer.normalize(samples), label_normalizer.normalize(labels)
        )

    ds_train, ds_val = random_split(
        FlowDataset(dataset_path),
        lengths=[0.8, 0.2],
        generator=torch.Generator().manual_seed(12),
    )

    sample_normalizer = Normalizer.from_data(ds_train[:][0])
    label_normalizer = Normalizer.from_data(ds_train[:][1])

    ds_train = normalize_dataset(ds_train, sample_normalizer, label_normalizer)
    ds_val = normalize_dataset(ds_val, sample_normalizer, label_normalizer)

    return ds_train, ds_val, sample_normalizer, label_normalizer


def evaluate_mean_squared_error(
    model: torch.nn.Module, ds: Dataset, label_normalizer: Normalizer
) -> float:
    samples, labels = ds[:]
    mse = torch.nn.MSELoss()
    model.to(DEVICE)
    samples = samples.to(DEVICE)
    predictions = label_normalizer.rescale(model(samples).flatten())
    labels = label_normalizer.rescale(labels.to(DEVICE))
    return mse(predictions, labels).item()


def save_training_history(
    train_losses: list[float], val_losses: list[float], output_path: Path
) -> None:
    epochs = list(range(1, len(train_losses) + 1))
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(epochs, train_losses, label="Train")
    ax.plot(epochs, val_losses, label="Val")
    ax.set_title("Train History")
    ax.set_xlabel("Epochs")
    ax.set_ylabel("Training Loss (MSE on normalized values)")
    ax.legend()
    fig.savefig(output_path)


def main() -> None:
    OUTPUTS_DIR.mkdir(exist_ok=True)

    ds_train, ds_val, _, label_normalizer = load_datasets(
        dataset_path=DATA_DIR / "flow_data.csv"
    )

    combinations = [
        (8, 7),
        (8, 6),
        (8, 5),
        (8, 4),
        (6, 5),
        (6, 4),
    ]

    mse_losses = []
    fxp_configs = []
    for total_bits, frac_bits in combinations:
        model = FlowPredictionModel(total_bits, frac_bits)

        train_losses, val_losses = train(
            model=model,
            train_data=ds_train,
            val_data=ds_val,
            batch_size=100,
            epochs=300,
            learning_rate=1e-3,
            device=DEVICE,
        )

        mse_losses.append(evaluate_mean_squared_error(model, ds_val, label_normalizer))
        fxp_configs.append(f"T{total_bits}F{frac_bits}")

        save_training_history(
            train_losses,
            val_losses,
            output_path=OUTPUTS_DIR / f"train_history_{fxp_configs[-1]}.png",
        )

    for config, loss in zip(fxp_configs, mse_losses):
        print(f"{config}: {loss:.04f}")

    # destination = OnDiskPath(name="build", parent=str(OUTPUTS_DIR))
    # design = model.create_design(name="flow_pred_model")
    # design.save_to(destination)


if __name__ == "__main__":
    main()
