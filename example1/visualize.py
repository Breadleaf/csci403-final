import psycopg2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

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
    SELECT s.followers, s.watch_time_minutes, s.stream_time_minutes, m.language
    FROM statistics AS s
    JOIN channels AS c ON s.id = c.statistics_id
    JOIN metadata AS m ON c.metadata_id = m.id
    """
    cur.execute(query)
    rows = cur.fetchall()

    # Create DataFrame and handle missing values
    df = pd.DataFrame(rows, columns=["Followers", "Watch time (minutes)", "Stream time (minutes)", "Language"])
    df = df.dropna()

    # Normalize data
    scaler = MinMaxScaler()
    df[["Followers", "Watch time (minutes)", "Stream time (minutes)"]] = scaler.fit_transform(df[["Followers", "Watch time (minutes)", "Stream time (minutes)"]])

    # Setup 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Color mapping based on language
    colors = {
            "Italian": "#FF6347",
            "English": "#4682B4",
            "Other": "#32CD32",
            "Greek": "#FFD700",
            "Spanish": "#6A5ACD",
            "German": "#FF4500",
            "Czech": "#DA70D6",
            "Arabic": "#B8860B",
            "Turkish": "#A0522D",
            "Chinese": "#40E0D0",
            "French": "#FF69B4",
            "Polish": "#00FA9A",
            "Swedish": "#F4A460",
            "Thai": "#800080",
            "Hungarian": "#008080",
            "Russian": "#DC143C",
            "Korean": "#00BFFF",
            "Japanese": "#696969",
            "Slovak": "#2E8B57",
            "Finnish": "#B22222",
            "Portuguese": "#FFDAB9"
            }
    df["Color"] = df["Language"].map(colors)

    # Scatter plot
    sc = ax.scatter(df["Followers"], df["Watch time (minutes)"], df["Stream time (minutes)"], c=df["Color"], marker="o")

    # Legend Setup
    labels = list(colors.keys())
    handles = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=color, label=language) for language, color in colors.items()]
    ax.legend(handles=handles, title="Languages", loc="center left", bbox_to_anchor=(1, 0.5))

    # Set axis labels
    ax.set_xlabel("Normalized Followers")
    ax.set_ylabel("Normalized Watch time (minutes)")
    ax.set_zlabel("Normalized Stream time (minutes)")

    # Display plot
    plt.show()

    # Close connections to database
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
