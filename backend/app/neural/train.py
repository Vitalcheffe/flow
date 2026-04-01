"""
Neural Operator Training Pipeline

Trains a Fourier Neural Operator on simulation data.
"""

import numpy as np
from pathlib import Path
from dataclasses import dataclass

from app.neural.fno import FNOModel, FNOConfig, NeuralOperatorSolver


@dataclass
class TrainingConfig:
    epochs: int = 100
    batch_size: int = 16
    learning_rate: float = 1e-3
    train_split: float = 0.8
    save_dir: str = "./models"


def generate_training_data(
    n_samples: int = 100,
    grid_size: int = 32,
    problem: str = "poisson",
) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic training data for neural operator.

    For Poisson equation: -∇²u = f
    - Input: source term f(x,y)
    - Output: solution u(x,y)
    """
    inputs = np.zeros((n_samples, grid_size, grid_size, 3))  # x, y, f
    targets = np.zeros((n_samples, grid_size, grid_size, 1))  # u

    x = np.linspace(0, 1, grid_size)
    y = np.linspace(0, 1, grid_size)
    xx, yy = np.meshgrid(x, y)

    for i in range(n_samples):
        # Random source term
        freq = np.random.randint(1, 5)
        phase_x = np.random.uniform(0, 2 * np.pi)
        phase_y = np.random.uniform(0, 2 * np.pi)

        f = np.sin(freq * np.pi * xx + phase_x) * np.sin(freq * np.pi * yy + phase_y)

        # Exact solution of -∇²u = f with u=0 on boundary
        u = f / (freq * np.pi)**2

        inputs[i, :, :, 0] = xx
        inputs[i, :, :, 1] = yy
        inputs[i, :, :, 2] = f
        targets[i, :, :, 0] = u

    return inputs, targets


def train_neural_operator(
    config: TrainingConfig | None = None,
) -> dict:
    """Train a neural operator on generated data."""
    if config is None:
        config = TrainingConfig()

    print("Generating training data...")
    inputs, targets = generate_training_data(n_samples=200, grid_size=32)

    # Split train/test
    n_train = int(len(inputs) * config.train_split)
    train_x, test_x = inputs[:n_train], inputs[n_train:]
    train_y, test_y = targets[:n_train], targets[n_train:]

    print(f"Training samples: {n_train}")
    print(f"Test samples: {len(test_x)}")

    # Create solver
    fno_config = FNOConfig(
        modes=8,
        width=32,
        n_layers=3,
        input_dim=3,
        output_dim=1,
        learning_rate=config.learning_rate,
    )
    solver = NeuralOperatorSolver(fno_config)

    # Train
    print("\nTraining...")
    history = solver.train(train_x, train_y, epochs=config.epochs)

    # Evaluate
    print("\nEvaluating...")
    test_predictions = solver.model.predict(test_x)
    test_loss = np.mean((test_predictions - test_y) ** 2)
    print(f"Test MSE: {test_loss:.6f}")

    # Save
    save_dir = Path(config.save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = save_dir / "fno_poisson.npz"
    solver.save(str(save_path))
    print(f"Model saved to {save_path}")

    return {
        "train_loss": history["loss"][-1],
        "test_loss": float(test_loss),
        "epochs": config.epochs,
        "model_path": str(save_path),
    }


if __name__ == "__main__":
    train_neural_operator()
