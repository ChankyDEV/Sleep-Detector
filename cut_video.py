from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

ffmpeg_extract_subclip("film_2.mp4", 0.0, 10.0, targetname="cut_film_2.mp4")
