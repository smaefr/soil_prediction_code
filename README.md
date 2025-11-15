# Soil Property Prediction using Hyperspectral Data

A comprehensive machine learning framework for predicting soil chemical and physical properties from visible-near-infrared (VNIR) hyperspectral reflectance data. This repository implements multiple regression algorithms and preprocessing techniques to predict key soil properties including pH, organic carbon, clay content, and nutrient levels.

## Overview

This project uses the **ICRAF-ISRIC Soil VNIR Spectral Library** containing 4,438 soil samples with associated spectral data (350-2500nm) and measured soil properties. The library includes samples from 58 countries across Africa, Asia, Europe, North America, and South America.

### Key Features

- **Multiple ML Algorithms**: PLS, Random Forest, Neural Networks, XGBoost, and 20+ other regression models
- **Advanced Preprocessing**: PCA dimensionality reduction, spectral derivatives, standard scaling
- **Enhanced Early Stopping**: Overfitting prevention for neural networks and PLS models
- **Automated Model Comparison**: LazyRegressor integration for benchmarking multiple algorithms
- **Crop Suitability Analysis**: Agricultural optimization based on predicted soil properties
- **Comprehensive Evaluation**: R² scores, cross-validation, and performance metrics

## Repository Structure

```
.
├── notebooks/              # Jupyter notebooks for analysis
│   ├── soil-hyperspectral-prediction.ipynb
│   └── soil-hyperspectral-prediction_derivatives.ipynb
├── scripts/               # Utility scripts
│   └── combine_results.py  # Combine and analyze results from multiple runs
├── results/                # Model performance results
│   ├── results_combined.json      # Combined results from all model runs
│   └── results_latex_table.txt    # LaTeX tables for paper inclusion
├── figures/                # Visualization outputs
│   ├── hist_*.png         # Distribution plots for soil properties
│   ├── models_rsq_plot*.png       # Model comparison plots
│   └── top_models_rsq_barchart*.png  # Top model performance charts
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/smaefr/soil_prediction_code.git
cd soil_prediction_code
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Key Dependencies

- **Data Science**: numpy, pandas, scikit-learn, scipy
- **Deep Learning**: tensorflow
- **Model Comparison**: lazypredict, scikit-optimize
- **Visualization**: matplotlib, seaborn
- **Jupyter**: jupyter, ipykernel, ipywidgets

## Usage

### Data Preparation

The notebooks expect CSV files in a `csv_files/` directory with the following structure:
- `ASD Spectra.csv`: Hyperspectral reflectance data (4438 samples × 216 bands)
- `Chemical_properties.csv`: Soil chemical properties (pH, organic carbon, nutrients)
- `Physical_properties.csv`: Soil physical properties (clay, sand, silt content)
- `ICRAF sample codes.csv`: Linking table between spectral and property data

### Running Analysis

1. **Main Analysis** (Standard preprocessing):
   - Open `notebooks/soil-hyperspectral-prediction.ipynb`
   - Follow the cells to load data, train models, and evaluate performance

2. **Spectral Derivatives Analysis**:
   - Open `notebooks/soil-hyperspectral-prediction_derivatives.ipynb`
   - Uses first and second derivatives of spectral data for enhanced feature extraction

3. **Combine Results**:
   ```bash
   python scripts/combine_results.py
   ```
   This script combines results from multiple runs and generates LaTeX tables for paper inclusion.

### Example Workflow

```python
# Load data
spectra, properties, wavelengths = load_icraf_data_from_csv('csv_files')

# Create predictor with PCA preprocessing
predictor = SoilPropertyPredictor(spectra, properties, wavelengths, 
                                   use_PCA=True, nPCs=30)

# Train models for target properties
target_properties = ['Clay_Content', 'Organic_Carbon', 'pH', 'Organic_Nitrogen']

for prop in target_properties:
    # Enhanced Neural Network
    nn_model, test_r2, y_test, y_pred = predictor.enhanced_neural_network_regression(prop)
    
    # Random Forest
    rf_model, test_r2, y_test, y_pred = predictor.random_forest_regression(prop)
    
    # PLS Regression
    pls_model, test_r2, y_test, y_pred = predictor.enhanced_pls_regression(prop)
```

## Model Performance

### High-Performance Properties (R² > 0.7)
- **Clay_Content**: R² ~0.84 (Enhanced Neural Network with PCA)
- **pH**: R² ~0.72-0.77 (ExtraTreesRegressor, Enhanced Neural Network)

### Moderate-Performance Properties (R² 0.5-0.7)
- **Organic_Carbon**: R² ~0.67-0.70 (XGBRegressor with PCA)
- **Magnesium**: R² ~0.66 (Enhanced Neural Network)
- **Sodium**: R² ~0.65 (Enhanced Neural Network)
- **Calcium**: R² ~0.60 (Enhanced Neural Network, ExtraTreesRegressor)

### Challenging Properties (R² < 0.5)
- **Organic_Nitrogen**: R² ~0.44 (NuSVR with PCA)
- **Potassium**: R² ~0.29-0.34 (ExtraTreesRegressor)

## Key Components

### SoilPropertyPredictor Class
Main class handling:
- Data preprocessing (scaling, PCA transformation)
- Model training and evaluation
- Model persistence (save/load trained models)
- Cross-validation and hyperparameter optimization

### Enhanced Early Stopping
- **Neural Networks**: Learning rate reduction, model checkpointing, validation monitoring
- **PLS**: Component search optimization with early stopping
- Prevents overfitting through comprehensive patience mechanisms

### Crop Suitability Analysis
Functions for agricultural applications:
- `calculate_crop_suitability_score()`: Overall soil quality scoring
- `recommend_best_crops()`: Crop-specific recommendations
- `create_soil_improvement_plan()`: Management recommendations

## Results

Final model performance results are available in:
- `results/results_combined.json`: Complete results in JSON format
- `results/results_latex_table.txt`: LaTeX tables ready for paper inclusion

Visualizations are stored in the `figures/` directory, including:
- Distribution histograms for each soil property
- Model comparison plots (R² scores)
- Top model performance bar charts

## Citation

If you use this code in your research, please cite:

```bibtex
@software{soil_hyperspectral_prediction,
  title = {Soil Property Prediction using Hyperspectral Data},
  author = {Miller, Alexander and Basener, Bill},
  organization = {Geospatial Technology Associates},
  year = {2025},
  url = {https://github.com/smaefr/soil_prediction_code/}
}
```

## Data Source

This project uses the **ICRAF-ISRIC Soil VNIR Spectral Library**:
- Viscarra Rossel, R.A., et al. (2016). A global spectral library to characterize the world's soil. Earth-Science Reviews, 155, 198-230.
- Available at: [ICRAF-ISRIC Soil VNIR Spectral Library](https://www.cifor-icraf.org/knowledge/dataset/MFHA9C/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or issues, please open an issue on the repository.

## Acknowledgments

- ICRAF-ISRIC for providing the soil spectral library
- Contributors to the open-source libraries used in this project
