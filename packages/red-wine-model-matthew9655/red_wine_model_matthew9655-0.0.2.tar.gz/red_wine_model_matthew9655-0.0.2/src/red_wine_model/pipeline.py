from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from red_wine_model.config.core import config

red_wine_pipe = Pipeline(
    [
        ("scaler", StandardScaler()),
        (
            "random_forest_classifier",
            GridSearchCV(
                RandomForestClassifier(random_state=config.m_config.random_state),
                param_grid={"n_estimators": [50, 100, 200]},
                cv=5,
            ),
        ),
    ]
)
