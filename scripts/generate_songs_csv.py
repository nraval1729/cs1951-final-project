import csv
import hdf5_getters as h
import os
import os.path
import numpy
import math
from decimal import *

TWOPLACES = Decimal(10) ** -2

def get_all_song_data(song_data):
	par_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
	curr_dir = par_dir + "/data/song_set2/"

	i = 0

	for filename in os.listdir(curr_dir):
		# if "h5" in filename:
		# 	print filename
		print i, " ", filename
		i += 1
		get_individual_song_data(curr_dir+filename, song_data)

def get_individual_song_data(filename, song_data):
	c = h.open_h5_file_read(filename.strip())
	c_dict = {}

	# Fucking everything
	c_dict['artist_familiarity'] = Decimal(str(h.get_artist_familiarity(c))).quantize(TWOPLACES)
	c_dict['artist_hotness'] = Decimal(str(h.get_artist_hotttnesss(c))).quantize(TWOPLACES)
	c_dict['artist_id'] = h.get_artist_id(c)

	c_dict['artist_location'] = h.get_artist_location(c)
	c_dict['artist_name'] = h.get_artist_name(c)
	c_dict['song_id'] = h.get_song_id(c)
	c_dict['song_hotness'] = Decimal(h.get_song_hotttnesss(c)).quantize(TWOPLACES)
	c_dict['sample_rate'] = Decimal(str(h.get_analysis_sample_rate(c))).quantize(TWOPLACES)
	c_dict['danceability'] = Decimal(h.get_danceability(c)).quantize(TWOPLACES)
	c_dict['duration'] = Decimal(h.get_duration(c)).quantize(TWOPLACES)
	c_dict['end_of_fade_in'] = Decimal(h.get_end_of_fade_in(c)).quantize(TWOPLACES)
	c_dict['start_of_fade_out'] = Decimal(h.get_start_of_fade_out(c)).quantize(TWOPLACES)
	c_dict['energy'] = Decimal(h.get_energy(c)).quantize(TWOPLACES)
	c_dict['key'] = h.get_key(c)
	c_dict['key_confidence'] = Decimal(h.get_key_confidence(c)).quantize(TWOPLACES)
	c_dict['loudness'] = Decimal(h.get_loudness(c)).quantize(TWOPLACES)
	c_dict['mode'] = h.get_mode(c)
	c_dict['mode_confidence'] = Decimal(h.get_mode_confidence(c)).quantize(TWOPLACES)
	c_dict['tempo'] = Decimal(h.get_tempo(c)).quantize(TWOPLACES)
	c_dict['time_signature'] = h.get_time_signature(c)
	c_dict['time_signature_confidence'] = Decimal(h.get_time_signature_confidence(c)).quantize(TWOPLACES)
	c_dict['track_id'] = h.get_track_id(c)

	# Start time of each segment. Returns an array
	# c_dict['segments_start'] = h.get_segments_start(c)
	# c_dict['segments_start_confidence'] = h.get_segments_confidence(c)
	c_dict['mean_segment_pitch'] = Decimal(numpy.mean(numpy.array(h.get_segments_pitches(c)))).quantize(TWOPLACES)
	c_dict['mean_segment_timbre'] = Decimal(numpy.mean(numpy.array(h.get_segments_timbre(c)))).quantize(TWOPLACES)
	c_dict['mean_segment_loudness_max'] = Decimal(numpy.mean(numpy.array(h.get_segments_loudness_max(c)))).quantize(TWOPLACES)
	c_dict['mean_segment_loudness_max_time'] = Decimal(numpy.mean(numpy.array(h.get_segments_loudness_max_time(c)))).quantize(TWOPLACES)
	c_dict['mean_segment_loudness_start'] = Decimal(numpy.mean(numpy.array(h.get_segments_loudness_start(c)))).quantize(TWOPLACES)
	c_dict['mean_section_start'] = Decimal(numpy.mean(numpy.array(h.get_sections_start(c)))).quantize(TWOPLACES)
	c_dict['mean_section_confidence'] = Decimal(numpy.mean(numpy.array(h.get_sections_confidence(c)))).quantize(TWOPLACES)
	c_dict['mean_beat_start'] = Decimal(numpy.mean(numpy.array(h.get_beats_start(c)))).quantize(TWOPLACES)
	c_dict['mean_beat_confidence'] = Decimal(numpy.mean(numpy.array(h.get_beats_confidence(c)))).quantize(TWOPLACES)
	c_dict['mean_bar_start'] = Decimal(numpy.mean(numpy.array(h.get_bars_start(c)))).quantize(TWOPLACES)
	c_dict['mean_bar_confidence'] = Decimal(numpy.mean(numpy.array(h.get_bars_confidence(c)))).quantize(TWOPLACES)
	c_dict['mean_tatum_start'] = Decimal(numpy.mean(numpy.array(h.get_tatums_start(c)))).quantize(TWOPLACES)
	c_dict['mean_tatum_confidence'] = Decimal(numpy.mean(numpy.array(h.get_tatums_confidence(c)))).quantize(TWOPLACES)
	c_dict['release_year'] = h.get_year(c)

	c.close()

	song_data.append(c_dict)

def write_all_song_data(song_data):
		with open("../songs.csv", "a") as s:
			writer = csv.writer(s)
			writer.writerow(['artist_familiarity', 'artist_hotness', 'artist_id', 'artist_location', 'artist_name', 'song_id', 'song_hotness', 'sample_rate', 'danceability', 'duration', 'end_of_fade_in', 'start_of_fade_out', 'energy', 'key', 'key_confidence', 'loudness', 'mode', 'mode_confidence', 'tempo', 'time_signature', 'time_signature_confidence', 'track_id', 'mean_segment_pitch', 'mean_segment_timbre', 'mean_segment_loudness_max', 'mean_segment_loudness_max_time', 'mean_segment_loudness_start', 'mean_section_start', 'mean_section_confidence', 'mean_beat_start', 'mean_beat_confidence', 'mean_bar_start', 'mean_bar_confidence', 'mean_tatum_start', 'mean_tatum_confidence', 'release_year'])

			for data in song_data:
				if (data["song_hotness"] and not math.isnan(data['song_hotness'])):
					writer.writerow([data['artist_familiarity'], data['artist_hotness'], data['artist_id'], data['artist_location'], data['artist_name'], data['song_id'], data['song_hotness'], data['sample_rate'], data['danceability'], data['duration'], data['end_of_fade_in'], data['start_of_fade_out'], data['energy'], data['key'], data['key_confidence'], data['loudness'], data['mode'], data['mode_confidence'], data['tempo'], data['time_signature'], data['time_signature_confidence'], data['track_id'], data['mean_segment_pitch'], data['mean_segment_timbre'], data['mean_segment_loudness_max'], data['mean_segment_loudness_max_time'], data['mean_segment_loudness_start'], data['mean_section_start'], data['mean_section_confidence'], data['mean_beat_start'], data['mean_beat_confidence'], data['mean_bar_start'], data['mean_bar_confidence'], data['mean_tatum_start'], data['mean_tatum_confidence'], data['release_year']])


def main():
	song_data = []

	get_all_song_data(song_data)

	write_all_song_data(song_data)

if __name__ == "__main__":
	main() 