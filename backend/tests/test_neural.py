"""Tests for neural operator."""

import numpy as np
import pytest

from app.neural.fno import FNOModel, FNOConfig, NeuralOperatorSolver, SpectralConv2d


class TestSpectralConv2d:
    def test_output_shape(self):
        layer = SpectralConv2d(8, 8, modes=4)
        x = np.random.randn(2, 8, 16, 16)
        out = layer.forward(x)
        assert out.shape == (2, 8, 16, 16)


class TestFNOModel:
    def test_predict_shape(self):
        config = FNOConfig(width=8, modes=4, n_layers=2, input_dim=3, output_dim=1)
        model = FNOModel(config)
        x = np.random.randn(1, 16, 16, 3)
        out = model.predict(x)
        assert out.shape == (1, 16, 16, 1)

    def test_batch_predict(self):
        config = FNOConfig(width=8, modes=4, n_layers=2, input_dim=3, output_dim=1)
        model = FNOModel(config)
        x = np.random.randn(3, 16, 16, 3)
        out = model.predict(x)
        assert out.shape == (3, 16, 16, 1)


class TestNeuralOperatorSolver:
    def test_predict(self):
        solver = NeuralOperatorSolver(FNOConfig(width=8, modes=4, n_layers=2))
        x = np.random.randn(16, 16, 3)
        out = solver.predict(x)
        assert out.shape == (16, 16, 1)

    def test_train_runs(self):
        solver = NeuralOperatorSolver(FNOConfig(width=8, modes=4, n_layers=2, input_dim=3, output_dim=1))
        x = np.random.randn(2, 16, 16, 3)
        y = np.random.randn(2, 16, 16, 1)
        history = solver.train(x, y, epochs=3)
        assert len(history["loss"]) == 3
        assert solver.model.trained
