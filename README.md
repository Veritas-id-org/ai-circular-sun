# Solar_power_generation

# Veritas - Solar Power Generation Prediction

Photo Voltaic Solar Power has emerged as the best source of green energy in recent past in a country like India which gets a good amount of solar insolation. With the continuous development of efficient PV modules, Battery storage and Smart Grid etc. Power Generation through PV Solar Plant has gained the momentum further and has a very promising future.

The solar power plant is also known as the Photovoltaic (PV) power plant. It is a large-scale PV plant designed to produce bulk electrical power from solar radiation. The solar power plant uses solar energy to produce electrical power. Therefore, it is a conventional power plant.Solar energy can be used directly to produce electrical energy using solar PV panels.Hence, to produce electrical power on a large scale, solar PV panels are used. Below is the layout plan of photovoltaic power plant.

## Installation

Clone repo and install requirements.txt in a Python>=3.7.0 environment.

```bash
git clone https://github.com/yikai28/Solar_power_generation.git  # clone
cd Solar_power_generation.git
pip install -r requirements.txt  # install
```

## Code structure

    .
    ├── data                          # data
    ├── model  
    │   ├── model.sav                 # pre-trained model
    ├── utils  
    │   ├── prep_data.py              # prepare data class
    ├── results  
    │   ├── predictions.json  # test  # prediction results
    ├── main.py                       # main function
    ├── README.md                     # readme
    └──requirements.txt               # all the requirement packages

## Usage
Put the dataset under the data directory, follow the data structure. Otherwise you have to feed your own --img-dir and --annotations to the function
```
python main.py [-h] --mode MODE --model MODEL -generation-data-loc $GENERATION_DATA_LOC --weather-data-loc $WEATHER_DATA_LOC  --model-save-dir $MODEL_SAVE_DIR --result-save-dir $RESULT_SAVE_DIR

optional arguments:
  -h, --help                                Show this help message and exit
  --mode MODE                               Choose from ['train', 'predict']
  --model MODEL                             Choose from ['LinearRegression', RandomForestRegressor', 
                                            'DecisionTreeRegressor']
  --generation-data-loc $IMG_DIR            Generation data directory
  --weather-data-loc    $ANNOTATIONS        Weather data directory
  --model-save-dir      $EVAL_SAVE_DIR      The directory to save model
  --result-save-dir     $PRED_SAVE_DIR      The directory to save prediction result
```

## Train
```bash
[CUDA_VISIBLE_DEVICES=0] python main.py --mode train
```

## Test
Download the best model to reproduce the result: https://drive.google.com/drive/folders/1yGBUK5sYCmnvxWG7U4LO4DDbi9G7Lp6a?usp=sharing

```bash
[CUDA_VISIBLE_DEVICES=0] python main.py --mode predict
```
It will automatically generate the file under result/predictions.json 

Including the results
e.g. 
```json
{
    "Actual": {
        "40426": 0.0,
        "50974": 0.0,
        "53919": 684.9133333333,
        "2384": 0.0,
        "22014": 0.0
    },
    "Predicted": {
        "40426": -0.1119316651,
        "50974": 0.1705407994,
        "53919": 683.6713557455,
        "2384": 0.4022034689,
        "22014": 0.6117726232
    }
}
 ```