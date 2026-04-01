"""
Fourier Neural Operator (FNO) for accelerated physics simulation.

Reference: "Fourier Neural Operator for Parametric Partial Differential Equations"
(Li et al., ICLR 2021)

Uses PyTorch when available, falls back to numpy for inference.
"""

import numpy as np
from dataclasses import dataclass
from pathlib import Path

try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


@dataclass
class FNOConfig:
    modes: int = 12
    width: int = 64
    n_layers: int = 4
    input_dim: int = 3
    output_dim: int = 1
    learning_rate: float = 1e-3


class SpectralConv2d:
    """2D Fourier layer (numpy implementation)."""

    def __init__(self, in_channels: int, out_channels: int, modes: int):
        self.modes = modes
        scale = 1 / (in_channels * out_channels)
        self.weights = (
            np.random.randn(in_channels, out_channels, modes, modes) * scale
            + 1j * np.random.randn(in_channels, out_channels, modes, modes) * scale
        )

    def forward(self, x: np.ndarray) -> np.ndarray:
        batch, channels, height, width = x.shape
        x_ft = np.fft.rfft2(x)

        out_ft = np.zeros_like(x_ft, dtype=complex)
        m = self.modes
        out_ft[:, :, :m, :m] = np.einsum("bchw,coph->bopw", x_ft[:, :, :m, :m], self.weights[:, :, :m, :m])

        return np.fft.irfft2(out_ft, s=(height, width))


class FNOModel:
    """Fourier Neural Operator model (numpy fallback)."""

    def __init__(self, config: FNOConfig):
        self.config = config
        self.spectral_layers = [
            SpectralConv2d(config.width, config.width, config.modes)
            for _ in range(config.n_layers)
        ]
        self.fc_weights = np.random.randn(config.input_dim, config.width) * 0.01
        self.fc_out = np.random.randn(config.width, config.output_dim) * 0.01
        self._trained = False

    def predict(self, x: np.ndarray) -> np.ndarray:
        batch, height, width, channels = x.shape

        # Project input to width dimension
        x_flat = x.reshape(batch * height * width, channels)
        h = x_flat @ self.fc_weights
        h = h.reshape(batch, height, width, self.config.width)

        # Permute to (batch, channels, height, width) for FFT
        h = np.transpose(h, (0, 3, 1, 2))

        # Apply spectral layers with residual connections
        for layer in self.spectral_layers:
            h_spectral = layer.forward(h)
            h = h + np.maximum(h_spectral, 0)  # residual + ReLU

        # Project to output
        h = np.transpose(h, (0, 2, 3, 1))
        h_flat = h.reshape(batch * height * width, self.config.width)
        out = h_flat @ self.fc_out
        return out.reshape(batch, height, width, self.config.output_dim)

    @property
    def trained(self):
        return self._trained

    @trained.setter
    def trained(self, value):
        self._trained = value


class NeuralOperatorSolver:
    """High-level interface for neural operator simulation."""

    def __init__(self, config: FNOConfig | None = None):
        self.config = config or FNOConfig()
        self.model = FNOModel(self.config)

    def train(self, input_data: np.ndarray, target_data: np.ndarray, epochs: int = 100) -> dict:
        """Train using gradient-free optimization (numpy fallback)."""
        history = {"loss": [], "epoch": []}
        best_loss = float("inf")
        best_weights = None

        for epoch in range(epochs):
            predictions = self.model.predict(input_data)
            loss = float(np.mean((predictions - target_data) ** 2))

            history["loss"].append(loss)
            history["epoch"].append(epoch)

            if loss < best_loss:
                best_loss = loss
                best_weights = {
                    "fc_weights": self.model.fc_weights.copy(),
                    "fc_out": self.model.fc_out.copy(),
                    "spectral": [l.weights.copy() for l in self.model.spectral_layers],
                }

            if epoch % 20 == 0:
                print(f"Epoch {epoch}/{epochs}, Loss: {loss:.6f}")

            # Simple perturbation-based optimization
            noise_scale = 0.001 * (1 - epoch / epochs)
            self.model.fc_weights += np.random.randn(*self.model.fc_weights.shape) * noise_scale
            self.model.fc_out += np.random.randn(*self.model.fc_out.shape) * noise_scale

        # Restore best weights
        if best_weights:
            self.model.fc_weights = best_weights["fc_weights"]
            self.model.fc_out = best_weights["fc_out"]
            for i, w in enumerate(best_weights["spectral"]):
                self.model.spectral_layers[i].weights = w

        self.model.trained = True
        return history

    def predict(self, input_data: np.ndarray) -> np.ndarray:
        x = input_data[np.newaxis, ...] if input_data.ndim == 3 else input_data
        return self.model.predict(x)[0]

    def save(self, path: str):
        np.savez(path, fc_weights=self.model.fc_weights, fc_out=self.model.fc_out)

    def load(self, path: str):
        data = np.load(path)
        self.model.fc_weights = data["fc_weights"]
        self.model.fc_out = data["fc_out"]
        self.model.trained = True
