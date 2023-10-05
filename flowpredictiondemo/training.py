from typing import Any
import torch
from torch.utils.data import Dataset, DataLoader


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
