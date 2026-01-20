import sys
try:
    import numpy
    print(f"Numpy: {numpy.__version__}")
except ImportError as e:
    print(f"Numpy Error: {e}")

try:
    import scipy
    print(f"Scipy: {scipy.__version__}")
except ImportError as e:
    print(f"Scipy Error: {e}")

try:
    import pandas
    print(f"Pandas: {pandas.__version__}")
except ImportError as e:
    print(f"Pandas Error: {e}")

try:
    import shap
    print(f"Shap: {shap.__version__}")
except ImportError as e:
    print(f"Shap Error: {e}")

try:
    import fastapi
    print(f"FastAPI: {fastapi.__version__}")
except ImportError as e:
    print(f"FastAPI Error: {e}")

try:
    import xgboost
    print(f"XGBoost: {xgboost.__version__}")
except ImportError as e:
    print(f"XGBoost Error: {e}")

try:
    import lightgbm
    print(f"LightGBM: {lightgbm.__version__}")
except ImportError as e:
    print(f"LightGBM Error: {e}")

try:
    import catboost
    print(f"CatBoost: {catboost.__version__}")
except ImportError as e:
    print(f"CatBoost Error: {e}")

try:
    import matplotlib
    print(f"Matplotlib: {matplotlib.__version__}")
except ImportError as e:
    print(f"Matplotlib Error: {e}")

try:
    import seaborn
    print(f"Seaborn: {seaborn.__version__}")
except ImportError as e:
    print(f"Seaborn Error: {e}")
