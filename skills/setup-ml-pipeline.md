---
name: setup-ml-pipeline
description: Production ML pipeline with MLflow tracking, feature store, model serving via FastAPI, A/B testing, and drift detection
---

# Setup ML Pipeline

Production-ready ML pipeline kurar:
- MLflow experiment tracking + model registry
- Feature store (Feast)
- Model serving (FastAPI + BentoML)
- A/B testing framework
- Data drift detection (Evidently)
- Automated retraining triggers

## Usage
```
#setup-ml-pipeline <sklearn|pytorch|tensorflow>
```

## pipeline/train.py
```python
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
import optuna

mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
mlflow.set_experiment("my-experiment")

def objective(trial: optuna.Trial, X_train, y_train) -> float:
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 50, 500),
        "max_depth": trial.suggest_int("max_depth", 3, 10),
        "learning_rate": trial.suggest_float("learning_rate", 1e-4, 0.3, log=True),
        "subsample": trial.suggest_float("subsample", 0.6, 1.0),
    }
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", GradientBoostingClassifier(**params, random_state=42)),
    ])
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring="roc_auc")
    return scores.mean()

def train(X_train, y_train, X_test, y_test):
    with mlflow.start_run():
        study = optuna.create_study(direction="maximize")
        study.optimize(lambda t: objective(t, X_train, y_train), n_trials=50)

        best_params = study.best_params
        mlflow.log_params(best_params)

        model = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", GradientBoostingClassifier(**best_params, random_state=42)),
        ])
        model.fit(X_train, y_train)

        metrics = {
            "roc_auc": roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]),
            "accuracy": model.score(X_test, y_test),
        }
        mlflow.log_metrics(metrics)

        signature = infer_signature(X_train, model.predict(X_train))
        mlflow.sklearn.log_model(model, "model", signature=signature,
                                  registered_model_name="my-model")

        return model, metrics
```

## serving/app.py
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.pyfunc
import pandas as pd
import numpy as np
from prometheus_client import Counter, Histogram, generate_latest
import time

app = FastAPI(title="ML Model Serving API")

model = mlflow.pyfunc.load_model(f"models:/my-model/Production")

PREDICTION_COUNTER = Counter("predictions_total", "Total predictions", ["model_version"])
PREDICTION_LATENCY = Histogram("prediction_latency_seconds", "Prediction latency")

class PredictRequest(BaseModel):
    features: dict[str, float | int | str]

class PredictResponse(BaseModel):
    prediction: float
    probability: float
    model_version: str

@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    start = time.time()
    try:
        df = pd.DataFrame([request.features])
        proba = model.predict(df)
        prediction = float(proba[0])

        PREDICTION_COUNTER.labels(model_version="production").inc()
        PREDICTION_LATENCY.observe(time.time() - start)

        return PredictResponse(
            prediction=round(prediction),
            probability=prediction,
            model_version="production",
        )
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@app.get("/metrics")
async def metrics():
    return generate_latest()

@app.get("/health")
async def health():
    return {"status": "ok"}
```

## monitoring/drift_detection.py
```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.metrics import DatasetDriftMetric
import pandas as pd
import json

def detect_drift(reference_data: pd.DataFrame, current_data: pd.DataFrame) -> dict:
    report = Report(metrics=[
        DataDriftPreset(),
        TargetDriftPreset(),
        DatasetDriftMetric(),
    ])
    report.run(reference_data=reference_data, current_data=current_data)
    result = json.loads(report.json())

    drift_detected = result["metrics"][2]["result"]["dataset_drift"]
    drift_share = result["metrics"][2]["result"]["share_of_drifted_columns"]

    if drift_detected:
        trigger_retraining(drift_share)

    return {"drift_detected": drift_detected, "drift_share": drift_share}

def trigger_retraining(drift_share: float):
    """Trigger retraining pipeline via Airflow/Prefect/Kubeflow"""
    import httpx
    httpx.post(
        f"{os.environ['ORCHESTRATOR_URL']}/api/v1/dags/retrain/dagRuns",
        json={"conf": {"drift_share": drift_share}},
        headers={"Authorization": f"Bearer {os.environ['ORCHESTRATOR_TOKEN']}"},
    )
```
