import csv
import psycopg2

def insert_data(csv_filepath):
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

    with open(csv_filepath, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader) # Skip the header row

        for row in csv_reader:
            # unpack the row into variables
            channel_name, watch_time_minutes, stream_time_minutes, peak_viewers, average_viewers, followers, followers_gained, views_gained, partnered, mature, language = row

            cur.execute("""
                        INSERT INTO twitch.channels (channel_name)
                        VALUES (%s) RETURNING id;
                        """, (channel_name,))
            channel_id = cur.fetchone()[0]

            cur.execute("""
                        INSERT INTO twitch.metadata (channel_id, partnered, mature, language)
                        VALUES (%s, %s, %s, %s) RETURNING id;
                        """, (channel_id, partnered, mature, language))
            metadata_id = cur.fetchone()[0]

            cur.execute("""
                        INSERT INTO twitch.statistics (channel_id, watch_time_minutes, stream_time_minutes, peak_viewers, average_viewers, followers, followers_gained, views_gained)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
                        """, (channel_id, watch_time_minutes, stream_time_minutes, peak_viewers, average_viewers, followers, followers_gained, views_gained))
            statistics_id = cur.fetchone()[0]

            cur.execute("""
                        UPDATE twitch.channels
                        SET metadata_id = %s, statistics_id = %s
                        WHERE id = %s;
                        """, (metadata_id, statistics_id, channel_id))

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    insert_data("twitchdata-update.csv")
