# scaleup-optimizers

`scaleup-optimizers` is a Python library for hyperparameter optimization using scalable algorithms. It integrates Bayesian optimization techniques to handle both small-scale (Experiment System) and large-scale (Production System) machine learning models.

## Problem Statement

Training and optimizing large-scale machine learning models presents several challenges:

- Computational Cost: Direct hyperparameter optimization on large models is extremely expensive in terms of both time and computational resources.
- Limited Iterations: Due to resource constraints, we can only perform a small number of optimization iterations on large models.
- Inefficient Search: Traditional approaches may waste valuable compute exploring suboptimal regions of the hyperparameter space.

## Description

This library is designed to help you efficiently optimize hyperparameters of machine learning models using Bayesian Optimization technique. It provides tools for working with both small-scale (e.g., experimental) and large-scale (e.g., production) systems, the large-scale leverages optimization history from small-scale.

## Architecture

The library consists of two main components:

### 1. SmallScaleOptimizer

- Performs initial Bayesian optimization on a smaller version of the model (Experiment System)
- Minimizes the objective function through multiple iterations
- Collects optimization history (best_params, X_iters, Y_iters) to inform the second stage
- Uses Small Scale Gaussian Process with acquisition functions

### 2. LargeScaleOptimizer

- Leverages optimization history from SmallScaleOptimizer
- Incorporates transfer learning to warm-start the optimization process
- Efficiently explores promising regions of the hyperparameter space
- Uses Large Scale Gaussian Process with acquisition functions

### Parameters

#### SmallScaleOptimizer

`objective_function`: callable function of Small Model to be optimized. Should take a list of parameters as input and return a scalar value to be minimized.

`search_space`: list of skopt.space objects. List defining the parameter search space using skopt space objects.

`acq_func` : str, default='EI'. The acquisition function to use for selecting next points. Options ('EI', 'PI', 'UCB')

`n_steps` : int, default=10. Number of optimization steps to perform after initialization.

`n_initial_points` : int, default=1. Number of random points to evaluate before starting the optimization. Only used if `X_init` and `Y_init` are not provided.

`X_init` : array-like, shape (n_small_samples, n_dimensions) optional. Initial parameter combinations.

`Y_init` : list, optional. Objective function values for initial points. Required to provide `X_init`.

#### LargeScaleOptimizer

`objective_function`: callable function of Large Model to be optimized. Should take a list of parameters (the numbers of parameter must be the same as Small Model) as input and return a scalar value to be minimized.

`search_space`: list of skopt.space objects. List defining the parameter search space using skopt space objects. (Use the same space for both Model).

`best_params`: list. Best parameters found from Small Model optimization runs. Used to initialize the transfer learning process. These parameters should be in the same format and order as defined in the search space.

`X_iters_small` : array-like, shape (n_small_samples, n_dimensions). A subset of Small Model optimization iterations' parameters. These represent the most relevant or important points from previous optimization runs. Used to warm start the Large Model optimization.

`Y_iters_small` : list, shape (n_small_samples). Objective function values corresponding to X_iters_small. These are the evaluation results from Small Model optimization runs.

`gp` and `gpL`: You can specify the alpha (numerical stability) and kernel length scale or bounds using SmallScaleGaussianProcess and LargeScaleGaussianProcess.

```python
from scaleup_bo.surrogate_models import SmallScaleGaussianProcess, LargeScaleGaussianProcess

gp = SmallScaleGaussianProcess(kernel=RBF(1.0, (1e-5, 100)), alpha=0.1)
gpL = LargeScaleGaussianProcess(kernel=RBF(0.5, (1e-3, 10)), alpha=0.01)
```

## Installation

### scaleup-optimizer requires

- `numpy>=1.21.0`
- `scipy>=1.10.0`
- `scikit-optimize>=0.8.1`
- `matplotlib>=3.4.0`

### Install via pip

You can install the library from PyPI or your local environment:

#### From PyPI

```bash
pip install scaleup-optimizers

```

## Getting Started

### Define the Experiment Model and decide on parameters to optimize then define objective function to minimize.

#### Load Dataset

```python
import numpy as np
import torch
import torch.nn as nn
import torchvision.datasets as datasets
from torch.utils.data import Subset
from torch.utils.data import DataLoader,random_split
import torchvision.transforms as transforms

data_transform = transforms.ToTensor()

train_dataset = datasets.FashionMNIST(root="datasets", train=True, transform=data_transform, download=True)
test_dataset = datasets.FashionMNIST(root="datasets", train=False, transform=data_transform, download=True)

# Calculate 5% of the datasets
test_subset_size = int(0.05 * len(test_dataset))
test_subset, _ = random_split(test_dataset, [test_subset_size, len(test_dataset) - test_subset_size])

train_data_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_data_loader = DataLoader(test_subset, batch_size=64, shuffle=True)
test_data_loader_L = DataLoader(test_dataset, batch_size=64, shuffle=True)
```

#### Define Experiment Model

```python
class ModelS(nn.Module):
    def __init__(self, dropout_rate=0.2, conv_kernel_size=3, pool_kernel_size=2):
        super(ModelS, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 64, kernel_size=conv_kernel_size, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=pool_kernel_size),
            self.merge_channels(64, 32),
        )

        self._compute_linear_input_size()

        self.classifier = nn.Sequential(
            nn.Dropout(dropout_rate),
            nn.Linear(self.linear_input_size, 10),
            nn.LogSoftmax(dim=1),
        )

    def merge_channels(self, in_channels, out_channels):
        assert in_channels == 2 * out_channels, "in_channels should be twice out_channels"
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1),
        )

    def _compute_linear_input_size(self):
        with torch.no_grad():
            dummy_input = torch.zeros(1, 1, 28, 28)
            features_output = self.features(dummy_input)
            num_channels, height, width = features_output.size()[1:]
            self.linear_input_size = num_channels * height * width

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

nll_loss = nn.NLLLoss()

# Select the device on which to perform the calculation.
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Transfer the model to the device that will perform the calculation.
model = ModelS().to(device)
# Create an Optimizer.
optim = torch.optim.Adam(model.parameters())

def train(model, device, data_loader, optim):
    model.train()

    total_loss = 0
    total_correct = 0
    for data, target in data_loader:
        # Transfer the data and labels to the device performing the calculation.
        data, target = data.to(device), target.to(device)

        # Sequential propagation.
        output = model(data)

        loss = nll_loss(output, target)
        total_loss += float(loss)

        # Reverse propagation or backpropagation
        optim.zero_grad()
        loss.backward()

        # Update parameters.
        optim.step()

        # The class with the highest probability is the predictive label.
        pred_target = output.argmax(dim=1)

        total_correct += int((pred_target == target).sum())

    avg_loss = total_loss / len(data_loader.dataset)
    accuracy = total_correct / len(data_loader.dataset)

    return avg_loss, accuracy

def test(model, device, data_loader):
    model.eval()

    with torch.no_grad():
        total_loss = 0
        total_correct = 0
        for data, target in data_loader:
            data, target = data.to(device), target.to(device)

            output = model(data)

            loss = nll_loss(output, target)
            total_loss += float(loss)

            pred_target = output.argmax(dim=1)

            total_correct += int((pred_target == target).sum())

    avg_loss = total_loss / len(data_loader.dataset)
    accuracy = total_correct / len(data_loader.dataset)

    return avg_loss, accuracy
```

#### Define Objective Function

```python
def objective_function_S(params):
    dropout_rate, learning_rate, conv_kernel_size, pool_kernel_size = params

    conv_kernel_size = int(conv_kernel_size)
    pool_kernel_size = int(pool_kernel_size)

    model = ModelS(dropout_rate=dropout_rate, conv_kernel_size=conv_kernel_size, pool_kernel_size=pool_kernel_size).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    n_epochs = 20
    patience = 5
    min_val_loss = float('inf')
    epochs_no_improve = 0

    for epoch in range(n_epochs):
        train_loss, train_accuracy = train(model, device, train_data_loader, optimizer)
        val_loss, val_accuracy = test(model, device, test_data_loader)

        # Check if validation loss has improved
        if val_loss < min_val_loss:
            min_val_loss = val_loss
            epochs_no_improve = 0
        else:
            epochs_no_improve += 1

        if epochs_no_improve >= patience:
            print(f"Early stopping at epoch {epoch+1}")
            break

    return min_val_loss
```

#### Define bound of search space (Unified for both Experiment and Production System)

```python
# List of hyperparameters to optimize.
# For each hyperparameter, we specify:
# - The bounds within which values will be selected.
# - The corresponding parameter name as recognized by scikit-learn.
# - The sampling distribution to guide value selection.
#   For instance, the learning rate uses a 'log-uniform' distribution.

from skopt.space import Real, Integer, Categorical

search_space = [
    Real(0.1, 1, name='dropout_rate'),
    Real(0.0001, 10, name='learning_rate', prior='log-uniform'),

    Integer(1, 10, name='conv_kernel_size'),
    Integer(1, 3, name='pool_kernel_size'),
]
```

#### Optimize Experiment System Over 10 Iteration

```python
from scaleup_bo import SmallScaleOptimizer

small_optimizer = SmallScaleOptimizer(objective_function_S, search_space, n_steps=10, n_initial_points=1)

# Collect history from SmallScaleOptimizer
best_params_s = small_optimizer.best_params
best_hyperparameters = dict(zip(['dropout_rate', 'learning_rate', 'conv_kernel_size', 'pool_kernel_size'], best_params_s))
print("Best Hyperparameter of Small Model: ", best_hyperparameters)

X_iters_small = small_optimizer.X_iters
print('X_iters_small: ', X_iters_small)

Y_iters_small = small_optimizer.Y_iters
print('Y_iters_small: ', Y_iters_small)

```

#### Output
```bash
Best Hyperparameter of Small Model: {'dropout_rate': 0.3002150723, 'learning_rate': 0.0007667914, 'conv_kernel_size': 6, 'pool_kernel_size': 3}

X_iters_small: array([[0.7803350320816986, 9.083817128074404, 4, 3],
       [0.1, 0.0001, 10, 5],
       [0.2757733648, 0.0369179854, 2, 4],
       [0.2364062706, 0.0002389496, 3, 3],
       [0.9509629778, 0.0134669852, 3, 5],
       [0.6484239182, 0.1599534102, 2, 5],
       [0.9573643447, 0.4342609034, 6, 5],
       [0.4850212168, 0.1077820534, 4, 4],
       [0.3002150723, 0.0007667914, 6, 3],
       [0.4913776109, 0.0010069987, 5, 3],
       [0.3353326913, 0.0079244646, 7, 4]])

Y_iters_small: array([0.0417628 , 0.00486325, 0.00528098, 0.00400994, 0.00927958,
       0.01945705, 0.03691163, 0.00989952, 0.00375851, 0.00390017,
       0.0042957 ])
```

#### Plot Performance
```python
from scaleup_bo.plots import plot_performance

plot_performance(small_optimizer)
```
![Figure : Plot Performance of Small Scale Optimizer](https://drive.google.com/file/d/1T7AvIKneih-x_7Z8P5TeuYveAik1XoN8/view?usp=drive_link)

#### Plot Evaluation 
```bash
from scaleup_bo.plots import custom_plot_evaluation

custom_plot_evaluation(small_optimizer)
```
![Figure : Plot Evaluation of Small Scale Optimizer](https://drive.google.com/file/d/1mo9yUg0yj_WDDZjUG_PdWgh4ZTTms2ig/view?usp=drive_link)

### Define the Production Model to optimize and the parameters are the same as Experiment System then define objective function to minimize using history leverage from Experiment System

#### Define Production Model

```python
class ModelL(nn.Module):
    def __init__(self, dropout_rate=0.2, conv_kernel_size=1, pool_kernel_size=2):
        super(ModelL, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=conv_kernel_size, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=pool_kernel_size, stride=2),
            nn.Conv2d(32, 64, kernel_size=conv_kernel_size, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=pool_kernel_size, stride=2),
        )

        self._compute_linear_input_size()

        self.classifier = nn.Sequential(
            nn.Dropout(dropout_rate),
            nn.Linear(self.linear_input_size, 128),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(128, 10),
            nn.LogSoftmax(dim=1),
        )

    def _compute_linear_input_size(self):
        with torch.no_grad():
            dummy_input = torch.zeros(1, 1, 28, 28)
            features_output = self.features(dummy_input)
            num_channels, height, width = features_output.size()[1:]
            self.linear_input_size = num_channels * height * width

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

# Transfer the model to the device that will perform the calculation.
modelL = ModelL().to(device)

# Create an Optimizer for ModelL
optimL = torch.optim.Adam(modelL.parameters())

```

#### Define Objective Function

```python

def objective_function_L(params):
    dropout_rate, learning_rate, conv_kernel_size, pool_kernel_size = params

    conv_kernel_size = int(conv_kernel_size)
    pool_kernel_size = int(pool_kernel_size)

    modelL = ModelL(dropout_rate=dropout_rate, conv_kernel_size=conv_kernel_size, pool_kernel_size=pool_kernel_size).to(device)
    optimizer = torch.optim.Adam(modelL.parameters(), lr=learning_rate)

    n_epochs = 30
    patience = 5
    min_val_loss = float('inf')
    epochs_no_improve = 0

    for epoch in range(n_epochs):
        train_loss, train_accuracy = train(modelL, device, train_data_loader, optimizer)
        val_loss, val_accuracy = test(modelL, device, test_data_loader_L)

        # Check if validation loss has improved
        if val_loss < min_val_loss:
            min_val_loss = val_loss
            epochs_no_improve = 0
        else:
            epochs_no_improve += 1

        if epochs_no_improve >= patience:
            print(f"Early stopping at epoch {epoch+1}")
            break

    return min_val_loss
```

#### Optimize Production System Over 10 Iteration

```python
from scaleup_bo import LargeScaleOptimizer

large_optimizer = LargeScaleOptimizer(objective_function_L, search_space, best_params=best_params_s, X_iters_small=X_iters_small, Y_iters_small=Y_iters_small,  n_steps=10)

best_params_l = large_optimizer.best_params
best_hyperparameters_l = dict(zip(['dropout_rate', 'learning_rate', 'conv_kernel_size', 'pool_kernel_size'], best_params_s))
print("Best Hyperparameter of Large Model: ", best_hyperparameters_l)

best_score_l = large_optimizer.best_score
print("Best score of Large Model: ", best_score_l)
```

#### Output
```bash
Best Hyperparameter of Large Model: {'dropout_rate': 0.300215072, 'learning_rate': 0.0007667914, 'conv_kernel_size': 6, 'pool_kernel_size': 3}

Best score of Large Model: 0.0035434851370751857
```

#### Plot Performance
```python
from scaleup_bo.plots import plot_performance

plot_performance(large_optimizer)
```
![Figure : Plot Performance of Large Scale Optimizer](https://drive.google.com/file/d/1zOxOg0G_jG11D-zJGCyWN4SWbjY4IDLf/view?usp=drive_link)

#### Plot Evaluation 
```python
from scaleup_bo.plots import custom_plot_evaluation

custom_plot_evaluation(large_optimizer)
```
![Figure : Plot Evaluation of Large Scale Optimizer](https://drive.google.com/file/d/1xWM8QCFTTTSMtVxIeVXRbW02LZUWp2cL/view)