## Experimental template for ML competitions

## Features
- Portable Kaggle-like environment with Docker
- Experiment management with Hydra
- Experiment scripts files are managed by folder for each major version
- Experiment parameter settings are managed as files for each minor version
  - Experiment scripts and experimental parameter settings are managed locally in the same folder.

## Config management with Hydra
- Config is defiend using dataclass instead of yaml and dict
- Environment-dependent configurations common to all scripts are defined in EnvConfig in utils/env.py
- Settings that vary from script to script are managed by placing them as `exp/{minor_exp_name}.yaml` in the folder
(`{major_exp_name}`) where the executable scripts are located.
- Overwrite at runtime with `exp={minor_exp_name}`
- Ensure that the experiment can be reproduced using a combination of `{major_exp_name}` and `{minor_exp_name}`.

## Structure
```text
.
├── experiments
├── input
├── notebook
├── output
├── tools
├── utils
├── Dockerfile
├── Dockerfile.cpu
├── LICENSE
├── Makefile
├── README.md
├── compose.cpu.yaml
└── compose.yaml
```

## Docker build environment

```sh
# build image
make build

# to run the jupyter lab
make jupyter

# in order to start on CPU, use CPU=1 or CPU=True
```

## How to run the script

```sh
# python experiments/{major_version_name}/run.py exp={minor_version_name}

python experiments/exp000_sample/run.py
python experiments/exp000_sample/run.py exp=001
```
