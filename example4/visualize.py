import psycopg2
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np  # Import numpy for the regression line

def main():
    # Connect to database
    conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="docker",
            password="docker",
            database="docker"
            )
    cur = conn.cursor()

    # Set search path to twitch schema
    cur.execute("SET search_path TO twitch")

    # Query data using a subquery to select name, peak_viewers, and views_gained
    query = """
    SELECT c.channel_name, s.peak_viewers, s.views_gained
    FROM (SELECT id, peak_viewers, views_gained FROM statistics) AS s
    JOIN channels AS c ON s.id = c.statistics_id
    """
    cur.execute(query)
    rows = cur.fetchall()

    # Create DataFrame and handle missing values
    df = pd.DataFrame(rows, columns=["Name", "Peak Viewers", "Views Gained"])
    df.dropna(inplace=True)

    # Setup plot
    fig, ax = plt.subplots()

    # Scatter plot
    sc = ax.scatter(df["Peak Viewers"], df["Views Gained"], alpha=0.6)

    # Calculate linear regression
    slope, intercept = np.polyfit(df["Peak Viewers"], df["Views Gained"], 1)
    x_vals = np.array(ax.get_xlim())
    y_vals = intercept + slope * x_vals
    ax.plot(x_vals, y_vals, '--', color="red", label=f"y = {slope:.2f}x + {intercept:.2f}")

    # Annotating each data point
    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(ind):
        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = f"{df.iloc[ind['ind'][0]]['Name']}:\nPeak Viewers: {df.iloc[ind['ind'][0]]['Peak Viewers']}\nViews Gained: {df.iloc[ind['ind'][0]]['Views Gained']}"
        annot.set_text(text)
        annot.get_bbox_patch().set_alpha(0.9)

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

    # Set axis labels and plot title
    ax.set_xlabel("Peak Viewers")
    ax.set_ylabel("Views Gained")
    ax.set_title("Relationship Between Peak Viewers and Views Gained")
    ax.legend()

    # Display plot
    plt.show()

    # Close connections to database
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
