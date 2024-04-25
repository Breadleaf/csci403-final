Bradley Hutchings

DATASET

Source:

For the dataset, I used twitch data from:
https://www.kaggle.com/datasets/aayushmishra1512/twitchdata?resource=download
This data is under the CC0: Public Domain license


Description:

The dataset contains information about the top 1000 twitch streamers.
In the dataset there are 11 columns: Channel Name, Watch time(Minutes),
Stream time(minutes), Peak viewers, Average viewers, Followers,
Followers gained, Views gained, Partnered, Mature, and Language.
I found the dataset interesting because I like to put on twitch while I do my
homework and I wanted to see what the data looked like for the top streamers.


Summary:

docker=# SET search_path TO twitch;
SET
docker=# SELECT * FROM twitch.channels LIMIT 2;
 id | channel_name | statistics_id | metadata_id 
----+--------------+---------------+-------------
  1 | xQcOW        |             1 |           1
  2 | summit1g     |             2 |           2
(2 rows)

docker=# SELECT * FROM twitch.statistics LIMIT 2;
 id | channel_id | watch_time_minutes | stream_time_minutes | peak_viewers | average_viewers | views_gained | followers | followers_gained 
----+------------+--------------------+---------------------+--------------+-----------------+--------------+-----------+------------------
  1 |          1 |         6196161750 |              215250 |       222720 |           27716 |     93036735 |   3246298 |          1734810
  2 |          2 |         6091677300 |              211845 |       310998 |           25610 |     89705964 |   5310163 |          1370184
(2 rows)

docker=# SELECT * FROM twitch.metadata LIMIT 2;
 id | channel_id | partnered | mature | language 
----+------------+-----------+--------+----------
  1 |          1 | t         | f      | English
  2 |          2 | t         | f      | English
(2 rows)


Transformations:

I wanted there two be three tables in the database: channels, statistics, and
metadata. That way if I was to make an app there would be segmentation between
the data a viewer/streamer might see (Statistics) and the data that the app might
want to modify (Metadata).

Create Table Statements:

DROP SCHEMA IF EXISTS twitch CASCADE;

CREATE SCHEMA IF NOT EXISTS twitch;

CREATE TABLE IF NOT EXISTS twitch.channels (
	id SERIAL PRIMARY KEY,
	channel_name TEXT UNIQUE NOT NULL,
	statistics_id BIGINT,
	metadata_id BIGINT
);

CREATE TABLE IF NOT EXISTS twitch.statistics (
	id SERIAL PRIMARY KEY,
	channel_id BIGINT UNIQUE NOT NULL,
	watch_time_minutes BIGINT,
	stream_time_minutes BIGINT,
	peak_viewers BIGINT,
	average_viewers BIGINT,
	views_gained BIGINT,
	followers BIGINT,
	followers_gained BIGINT
);

CREATE TABLE IF NOT EXISTS twitch.metadata (
	id SERIAL PRIMARY KEY,
	channel_id BIGINT UNIQUE NOT NULL,
	partnered BOOLEAN,
	mature BOOLEAN,
	language TEXT
);

ALTER TABLE twitch.channels
ADD CONSTRAINT fk_statistics_id
FOREIGN KEY (statistics_id)
REFERENCES twitch.statistics(id);

ALTER TABLE twitch.channels
ADD CONSTRAINT fk_metadata_id
FOREIGN KEY (metadata_id)
REFERENCES twitch.metadata(id);

ANALYSIS

Question 1:

Do mature streamers on average have more followers than non-mature streamers?

Query:

SELECT m.mature, AVG(s.followers) AS average_followers
FROM channels c
JOIN metadata m ON c.metadata_id = m.id
JOIN statistics s ON c.statistics_id = s.id
GROUP BY m.mature;

Output:

 mature |  average_followers  
--------+---------------------
 f      | 608951.937662337662
 t      | 439830.765217391304

Conclusion:

On average, mature streamers have less followers than non-mature streamers.

Why this is interesting:

This provides insight on the type of content that is popular on twitch. It seems
that non-mature streamers are more popular than mature streamers. This could be
because the majority of streaming on twitch is gaming and the mature content
is not as popular as the non-mature content.


Question 2:

Do partnered streamers tend to speak a different language than non-partnered streamers?

Query:

SET search_path TO twitch;
SET
docker=# SELECT m.partnered, m.language, COUNT(*) AS number_of_streamers
FROM channels c
JOIN metadata m on c.metadata_id = m.id
GROUP BY m.partnered, m.language
ORDER BY m.partnered, number_of_streamers DESC;

Output:

 partnered |  language  | number_of_streamers 
-----------+------------+---------------------
 f         | English    |                   9
 f         | Russian    |                   7
 f         | German     |                   1
 f         | Spanish    |                   1
 f         | Korean     |                   1
 f         | Other      |                   1
 f         | Portuguese |                   1
 f         | French     |                   1
 t         | English    |                 476
 t         | Korean     |                  76
 t         | Russian    |                  67
 t         | Spanish    |                  67
 t         | French     |                  65
 t         | Portuguese |                  60
 t         | German     |                  48
 t         | Chinese    |                  30
 t         | Turkish    |                  22
 t         | Italian    |                  17
 t         | Polish     |                  12
 t         | Thai       |                  11
 t         | Japanese   |                  10
 t         | Czech      |                   6
 t         | Arabic     |                   5
 t         | Hungarian  |                   2
 t         | Swedish    |                   1
 t         | Slovak     |                   1
 t         | Finnish    |                   1
 t         | Greek      |                   1

Conclusion:

Partnered streamers tend to speak English more than any other language while
non-partnered streamers are more concentrated in Russian and English.

Why this is interesting:

This is interesting because it shows that partnered streamers are more likely
to speak English than non-partnered streamers. This could be because other
countries have their own streaming platforms that are more popular than twitch.
