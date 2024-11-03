
# MolALKit: A Toolkit for Active Learning in Molecular Data.
This software package serves as a robust toolkit designed for the active learning of molecular data.

## Installation
Python 3.10 is recommended.
Check the GPU and CUDA requirements at [mgktools](https://github.com/Xiangyan93/mgktools) for marginalized graph kernel model.
```
pip install numpy==1.22.3 git+https://gitlab.com/Xiangyan93/graphdot.git@feature/xy git+https://github.com/bp-kelley/descriptastorus git+https://github.com/Xiangyan93/chemprop.git@molalkit
pip install mgktools molalkit
```

## QuickStart
GPU is required to support graph kernel. 
It will take about 10 minutes to set up the environment and run the demo.
- [Google Colab notebook](https://colab.research.google.com/drive/11thNx7RkGbGMe_TgieWCEShYy-h32Khv?usp=sharing).

## Data
**MolALKit** currently supports active learning exclusively for single-task datasets, which can be either classification or regression tasks.

### Custom Dataset
The data file must be in CSV format with a header row, structured as follows:
```
smiles,p_np
[Cl].CC(C)NCC(O)COc1cccc2ccccc12,1
C(=O)(OC(C)(C)C)CCCc1ccc(cc1)N(CCCl)CCCl,1
...
```
The following arguments are required to run the active learning 
```
--data_path <dataset.csv> --pure_columns <smiles> --target_columns <target> --dataset_type <classification/regression>
```

### Public Dataset
The toolkit incorporates several popular public datasets, such as MoleculeNet and TDC, which can be used directly `--data_public <dataset name>`.

Here is the list of available datasets:
```
from molalkit.data.datasets import AVAILABLE_DATASETS
print(AVAILABLE_DATASETS)
```

### ActiveLearning/Validation Split
Our code supports several methods of splitting data into an active learning set and a validation set. 
The active learning is used for active learning and the validation set is used for evaluating the performance of the active learning model.
* **random**  The data will be split randomly.
* **scaffold_order** With this approach, the data is split based on molecular scaffolds, ensuring that the same scaffold never appears in both the active learning and validation sets. 
The scaffold containing the most molecules is placed in the active learning set. This method aligns with the implementation in DeepChem and is independent of random seeds.
* **scaffold_random** In this method, the placement of scaffolds in either the active learning set or the validation set is done randomly. 
This split is dependent on random seeds and introduces an element of randomness into the scaffold split.

The following arguments are required for data split:
```
--split_type <random/scaffold_order/scaffold_random> --split_sizes <active learning set ratio> <validation set ratio> --seed <random seed>
```

## Machine Learning Model
The machine learning model used in this package is described in a json config file. 
Here is the list of built-in machine learning models:
```
from molalkit.models.configs import AVAILABLE_MODELS
print(AVAILABLE_MODELS)
```
The model config files are placed in [molalkit/models/configs](https://github.com/RekerLab/MolALKit/tree/main/molalkit/models/configs). 
The following arguments are required for choosing a machine learning model:
```
--model_config_selector <model_config_file>
```

## First Example
Here's an example of running active learning using MolALKit with the BACE dataset, a 50:50 scaffold split, and Random Forest as the machine learning model:
```
molalkit_run --data_public bace --metrics roc-auc mcc accuracy precision recall f1_score --learning_type explorative --model_config_selector RandomForest_Morgan_Config --split_type scaffold_order --split_sizes 0.5 0.5 --evaluate_stride 10 --seed 0 --save_dir bace
```
