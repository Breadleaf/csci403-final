import psycopg2
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

def main():
    # Connect to database
    conn = (
            psycopg2.connect(
                host="localhost",
                port="5432",
                user="docker",
                password="docker",
                database="docker"
                )
            )
    cur = conn.cursor()

    # Set search path to twitch schema
    cur.execute("SET search_path TO twitch")

    # Query data
    query = """
    SELECT s.followers, s.watch_time_minutes, s.stream_time_minutes, s.peak_viewers, m.mature, m.language
    FROM statistics AS s
    JOIN channels AS c ON s.id = c.statistics_id
    JOIN metadata AS m ON c.metadata_id = m.id
    """
    cur.execute(query)
    rows = cur.fetchall()

    # Create DataFrame and handle missing values
    df = pd.DataFrame(rows, columns=["Followers", "Watch time (minutes)", "Stream time (minutes)", "Peak viewers", "Mature", "Language"])
    df = df.dropna()

    # Data preprocessing
    features = df.drop("Followers", axis=1)
    target = df["Followers"]

    numeric_features = ["Watch time (minutes)", "Stream time (minutes)", "Peak viewers"]
    categorical_features = ["Mature", "Language"]

    numeric_pipeline = Pipeline([
        ("scaler", MinMaxScaler())
    ])

    categorical_pipeline = Pipeline([
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_pipeline, numeric_features),
        ("cat", categorical_pipeline, categorical_features)
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=42
    )

    rf_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    rf_pipeline.fit(X_train, y_train)

    def predict_followers():
        # Print averages
        print(f"Average watch time: {df['Watch time (minutes)'].mean()}")
        print(f"Average stream time: {df['Stream time (minutes)'].mean()}")
        print(f"Average peak viewers: {df['Peak viewers'].mean()}")

        # Get input
        watch_time = float(input("Enter watch time (minutes): "))
        stream_time = float(input("Enter stream time (minutes): "))
        peak_viewers = int(input("Enter peak viewers: "))

        mature = -1
        while True:
            print("0: Not flagged as mature")
            print("1: Flagged as mature")
            mature = int(input("Enter mature: "))
            if mature in [0, 1]:
                break
            else:
                print("Invalid input. Please try again.")
        mature = bool(mature)

        language = -1
        while True:
            for index, language in enumerate(df["Language"].unique()):
                print(f"{index}: {language}")
            language = int(input("Enter language: "))
            if language in range(len(df["Language"].unique())):
                break
            else:
                print("Invalid input. Please try again.")
        language = df["Language"].unique()[language]

        # Make DataFrame from input
        input_df = pd.DataFrame({
            "Watch time (minutes)": [watch_time],
            "Stream time (minutes)": [stream_time],
            "Peak viewers": [peak_viewers],
            "Mature": [mature],
            "Language": [language]
        })

        # Predict followers
        prediction = rf_pipeline.predict(input_df)
        print(f"Predicted followers: {prediction[0]}")


    # Predict followers
    predict_followers()

    # Close connections to database
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
