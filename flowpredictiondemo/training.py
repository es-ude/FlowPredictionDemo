from pathlib import Path
from typing import Any
import torch
from matplotlib import pyplot as plt
from torch.utils.data import Dataset, DataLoader, TensorDataset, random_split

from flowpredictiondemo.flow_dataset import FlowDataset
from flowpredictiondemo.normalizer import Normalizer


def train(
    model: torch.nn.Module,
    train_data: Dataset,
    val_data: Dataset,
    batch_size: int,
    epochs: int,
    learning_rate: float,
    device: Any,
) -> tuple[list[float], list[float]]:
    train_losses, val_losses = [], []

    dl_train = DataLoader(train_data, batch_size=batch_size, shuffle=True)
    dl_val = DataLoader(val_data, batch_size=batch_size, shuffle=False)

    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    loss_fn = torch.nn.MSELoss()
    model = model.to(device)

    for epoch in range(1, epochs + 1):
        model.train()

        running_loss = 0

        for samples, labels in dl_train:
            samples = samples.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()

            predictions = model(samples)
            loss = loss_fn(predictions.flatten(), labels)
            loss.backward()

            optimizer.step()

            running_loss += loss.item()

        train_losses.append(running_loss / len(dl_train))

        model.eval()

        running_loss = 0

        for samples, labels in dl_val:
            samples = samples.to(device)
            labels = labels.to(device)

            predictions = model(samples)
            loss = loss_fn(predictions.flatten(), labels)

            running_loss += loss.item()

        val_losses.append(running_loss / len(dl_val))

        print(
            f"[Epoch {epoch}/{epochs}] train_loss: {train_losses[-1]:.04f} ; val_loss: {val_losses[-1]:.04f}"
        )

    return train_losses, val_losses


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def load_datasets(
    dataset_path: Path,
) -> tuple[TensorDataset, TensorDataset]:
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

    return ds_train, ds_val


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


def prepare_data_and_train(model):

    ds_train, ds_val = load_datasets(dataset_path=DATA_DIR / "flow_data.csv")

    train_losses, val_losses = train(
        model=model,
        train_data=ds_train,
        val_data=ds_val,
        batch_size=100,
        epochs=250,
        learning_rate=1e-3,
        device=DEVICE,
    )

    save_training_history(
        train_losses, val_losses, output_path=OUTPUTS_DIR / "train_history.png"
    )


DATA_DIR = Path("data")
OUTPUTS_DIR = Path("outputs")
