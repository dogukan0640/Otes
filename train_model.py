import pandas as pd
import lightgbm as lgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

MODEL_PATH = "model.pkl"

def train_lightgbm_model():
    df = pd.read_csv("signals_enriched.csv")
    df = df.dropna()
    df['target'] = (df['confidence_score'] > 70).astype(int)

    features = ['rsi', 'atr']
    X = df[features]
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = lgb.LGBMClassifier()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model eğitildi. Doğruluk oranı: {accuracy:.2f}")

    joblib.dump(model, MODEL_PATH)
    return accuracy

if __name__ == "__main__":
    acc = train_lightgbm_model()
