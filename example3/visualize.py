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
    SELECT average_viewers, followers_gained
    FROM statistics
    """
    cur.execute(query)
    rows = cur.fetchall()

    # Create DataFrame and handle missing values
    df = pd.DataFrame(rows, columns=["Average Viewers", "Followers Gained"])
    df.dropna(inplace=True)

    # Setup plot
    fig, ax = plt.subplots()

    # Scatter plot
    sc = ax.scatter(df["Average Viewers"], df["Followers Gained"], alpha=0.6)

    # Calculate and plot trend line
    z = np.polyfit(df["Average Viewers"], df["Followers Gained"], 1)
    p = np.poly1d(z)
    plt.plot(df["Average Viewers"], p(df["Average Viewers"]), "r--")

    # Annotate correlation coefficient
    correlation = df.corr().iloc[0, 1]
    plt.annotate(f"Correlation: {correlation:.2f}", xy=(0.05, 0.95), xycoords='axes fraction', fontsize=12, backgroundcolor='white')

    # Set axis labels and plot title
    ax.set_xlabel("Average Viewers")
    ax.set_ylabel("Followers Gained")
    ax.set_title("Relationship Between Average Viewers and Followers Gained")

    # Display plot
    plt.show()

    # Close connections to database
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
