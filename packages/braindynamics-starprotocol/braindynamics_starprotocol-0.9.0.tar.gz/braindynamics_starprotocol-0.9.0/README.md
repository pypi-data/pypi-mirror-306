# BrainDynamics package demo

## Requirements

- python (tested for 3.12 and later versions)
- C/C++ compiler (e.g. gcc on Linux or Visual C++ Build Tools on Windows)

## Setting up

### 1) Set up virtual python environment using python or conda.

For example:

```
python -m venv braindynamics_env
```

OR via Anaconda:

```
conda create --name braindynamics_env python=3.x
```

### 2) Install package from TestPyPi

Make sure to include the original PyPi link after the --extra-index-url, otherwise the dependencies won't be found on TestPyPi, and the install will fail.

```
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple braindynamics-pbalazs
```

Link to the TestPyPi project site for release history: https://test.pypi.org/project/braindynamics-pbalazs/
