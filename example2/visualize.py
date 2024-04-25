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
    SELECT s.watch_time_minutes, s.stream_time_minutes
    FROM statistics AS s
    JOIN channels AS c ON s.id = c.statistics_id
    JOIN metadata AS m ON c.metadata_id = m.id
    """
    cur.execute(query)
    rows = cur.fetchall()

    # Create DataFrame and handle missing values
    df = pd.DataFrame(rows, columns=["Watch time (minutes)", "Stream time (minutes)"])
    df = df.dropna()

    # Normalize data
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(df)
    df_normalized = pd.DataFrame(normalized_data, columns=["Normalized Watch time (minutes)", "Normalized Stream time (minutes)"])

    # Setup Plot
    fig, ax = plt.subplots()

    # Scatter plot
    sc = ax.scatter(df_normalized["Normalized Watch time (minutes)"], df_normalized["Normalized Stream time (minutes)"], marker="o")

    # Calculate trend line
    z = np.polyfit(df_normalized["Normalized Watch time (minutes)"], df_normalized["Normalized Stream time (minutes)"], 1)
    p = np.poly1d(z)
    ax.plot(df_normalized["Normalized Watch time (minutes)"], p(df_normalized["Normalized Watch time (minutes)"]), "r--")

    # Annotate each data point
    annot = ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points", bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(ind):
        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = f"Watch: {df.iloc[ind['ind'][0]]['Watch time (minutes)']}\nStream: {df.iloc[ind['ind'][0]]['Stream time (minutes)']}"
        annot.set_text(text)
        annot.get_bbox_patch().set_alpha(0.4)

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)

    # Set axis labels
    ax.set_xlabel("Normalized Watch time (minutes)")
    ax.set_ylabel("Normalized Stream time (minutes)")

    # Display plot
    plt.show()

    # Close connections to database
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
