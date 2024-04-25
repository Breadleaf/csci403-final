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
