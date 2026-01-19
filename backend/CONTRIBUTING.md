# Contributing to Invisor Backend

## 🐍 Python Style Guide
-   Follow **PEP 8** standards.
-   Use `black` for formatting.
-   Use `isort` for import sorting.
-   Use type hints (`typing` module) for all function arguments and return values.

## 🧪 Testing
-   Run tests using `pytest`.
-   Ensure all new endpoints have corresponding test cases in `test_api.py`.

## 📝 Commit Messages
-   Use imperative mood ("Add feature" not "Added feature").
-   Reference issue numbers if applicable.

## 🏗️ Model Integration
-   Place ML models in the `models/` directory.
-   Update `models/model_interface.py` to handle loading and inference.
-   Ensure mock fallbacks are available if models are missing.
