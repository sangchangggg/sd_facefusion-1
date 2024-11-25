import traceback

import filetype
import subprocess


import facefusion.globals
from facefusion import process_manager
from facefusion.filesystem import get_temp_frames_pattern, get_temp_output_video_path
from facefusion.typing import OutputVideoPreset, Fps, AudioBuffer
from typing import List, Optional

from ffmpeg_progress_yield import FfmpegProgress
from facefusion.ff_status import FFStatus
from facefusion.mytqdm import mytqdm
from facefusion.uis.components.job_queue import logger

TEMP_OUTPUT_VIDEO_NAME = 'temp.mp4'
LAST_VIDEO_INFO = None


def run_ffmpeg(args: List[str], show_progress: bool = False) -> bool:
    if show_progress:
        return run_ffmpeg_progress(args, "Extracting")
    else:
        return open_ffmpeg(args).wait() == 0


def open_ffmpeg(args: List[str]) -> subprocess.Popen[bytes]:
    commands = ['ffmpeg', '-hide_banner', '-loglevel', 'quiet']
    commands.extend(args)
    return subprocess.Popen(commands, stdin=subprocess.PIPE, stdout=subprocess.PIPE)


def extract_frames(target_path: str, temp_video_resolution: str, temp_video_fps: Fps) -> bool:
    temp_frames_pattern = get_temp_frames_pattern(target_path, '%04d')
    trim_frame_start = facefusion.globals.trim_frame_start
    trim_frame_end = facefusion.globals.trim_frame_end

    # Initialize FFmpeg commands
    commands = ['-hwaccel', 'auto', '-i', target_path]
    filter_string = f"scale={temp_video_resolution},fps={temp_video_fps}"

    # Add trim options
    if trim_frame_start is not None or trim_frame_end is not None:
        trim_filter = []
        if trim_frame_start is not None:
            trim_filter.append(f"start_frame={trim_frame_start}")
        if trim_frame_end is not None and trim_frame_end > 0:
            trim_filter.append(f"end_frame={trim_frame_end}")
        trim_options = ':'.join(trim_filter)
        filter_string = f"trim={trim_options},{filter_string}"

    commands.extend(['-vf', filter_string, '-vsync', '0', temp_frames_pattern])
    return run_ffmpeg(commands, show_progress=True)


def merge_video(target_path: str, output_video_resolution: str, output_video_fps: Fps) -> bool:
    temp_output_video_path = get_temp_output_video_path(target_path)
    temp_frames_pattern = get_temp_frames_pattern(target_path, '%04d')
    commands = ['-hwaccel', 'auto', '-s', str(output_video_resolution), '-r', str(output_video_fps), '-i',
                temp_frames_pattern, '-c:v', facefusion.globals.output_video_encoder]

    if facefusion.globals.output_video_encoder in ['libx264', 'libx265']:
        output_video_compression = round(51 - (facefusion.globals.output_video_quality * 0.51))
        commands.extend(['-crf', str(output_video_compression), '-preset', facefusion.globals.output_video_preset])
    if facefusion.globals.output_video_encoder in ['libvpx-vp9']:
        output_video_compression = round(63 - (facefusion.globals.output_video_quality * 0.63))
        commands.extend(['-crf', str(output_video_compression)])
    if facefusion.globals.output_video_encoder in ['h264_nvenc', 'hevc_nvenc']:
        output_video_compression = round(51 - (facefusion.globals.output_video_quality * 0.51))
        commands.extend(
            ['-cq', str(output_video_compression), '-preset', map_nvenc_preset(facefusion.globals.output_video_preset)])
    if facefusion.globals.output_video_encoder in ['h264_amf', 'hevc_amf']:
        output_video_compression = round(51 - (facefusion.globals.output_video_quality * 0.51))
        commands.extend(['-qp_i', str(output_video_compression), '-qp_p', str(output_video_compression), '-quality',
                         map_amf_preset(facefusion.globals.output_video_preset)])
    commands.extend(['-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-y', temp_output_video_path])
    return run_ffmpeg(commands)


def copy_image(target_path: str, output_path: str, temp_image_resolution: str) -> bool:
    is_webp = filetype.guess_mime(target_path) == 'image/webp'
    temp_image_compression = 100 if is_webp else 0
    commands = ['-i', target_path, '-q:v', str(temp_image_compression), '-vf', 'scale=' + str(temp_image_resolution),
                '-y', output_path]
    return run_ffmpeg(commands)


def finalize_image(output_path: str, output_image_resolution: str) -> bool:
    output_image_compression = round(31 - (facefusion.globals.output_image_quality * 0.31))
    commands = ['-i', output_path, '-q:v', str(output_image_compression), '-vf',
                'scale=' + str(output_image_resolution), '-y', output_path]
    return run_ffmpeg(commands)


def read_audio_buffer(target_path: str, sample_rate: int, total_channel: int) -> Optional[AudioBuffer]:
    commands = ['-i', target_path, '-vn', '-f', 's16le', '-acodec', 'pcm_s16le', '-ar', str(sample_rate), '-ac',
                str(total_channel), '-']
    process = open_ffmpeg(commands)
    audio_buffer, _ = process.communicate()
    if process.returncode == 0:
        return audio_buffer
    return None


def restore_audio(target_path: str, output_path: str, output_video_fps: float) -> bool:
    """
    Restores the original audio to a trimmed video.

    Args:
        target_path (str): Path to the original video with audio.
        output_path (str): Path to save the output video with restored audio.
        output_video_fps (float): Frame rate of the video to calculate time offsets.

    Returns:
        bool: True if the operation succeeds, False otherwise.
    """
    try:
        # Fetch global trim frame values
        trim_frame_start = facefusion.globals.trim_frame_start
        trim_frame_end = facefusion.globals.trim_frame_end

        # Get the temporary video path
        temp_output_video_path = get_temp_output_video_path(target_path)

        # Initialize the FFmpeg command
        commands = [
            'ffmpeg', '-hide_banner', '-loglevel', 'error',  # Suppress unnecessary output
            '-hwaccel', 'auto',  # Enable hardware acceleration
            '-i', temp_output_video_path  # Input video without audio
        ]

        if isinstance(trim_frame_start, int):
            start_time = trim_frame_start / output_video_fps
            commands.extend(['-ss', str(start_time)])
        if isinstance(trim_frame_end, int):
            end_time = trim_frame_end / output_video_fps
            commands.extend(['-to', str(end_time)])
        commands.extend(
            ['-i', target_path, '-c:v', 'copy', '-c:a', 'aac', '-map', '0:v:0',
             '-map', '1:a:0', '-shortest', '-y', output_path])

        # Run the FFmpeg command
        print(f"Restoring audio: '{' '.join(commands)}'")
        result = run_ffmpeg(commands)

        # Check if the command was successful
        if not result:
            print("FFmpeg failed. Check inputs and outputs.")
            return False

        return True
    except Exception as e:
        print(f"Error in restore_audio: {e}")
        return False


def replace_audio(target_path: str, audio_path: str, output_path: str) -> bool:
    temp_output_path = get_temp_output_video_path(target_path)
    commands = ['-hwaccel', 'auto', '-i', temp_output_path, '-i', audio_path, '-c:v', 'copy', '-af', 'apad',
                '-shortest', '-map', '0:v:0', '-map', '1:a:0', '-y', output_path]
    return run_ffmpeg(commands)


def map_nvenc_preset(output_video_preset: OutputVideoPreset) -> Optional[str]:
    if output_video_preset in ['ultrafast', 'superfast', 'veryfast']:
        return 'p1'
    if output_video_preset == 'faster':
        return 'p2'
    if output_video_preset == 'fast':
        return 'p3'
    if output_video_preset == 'medium':
        return 'p4'
    if output_video_preset == 'slow':
        return 'p5'
    if output_video_preset == 'slower':
        return 'p6'
    if output_video_preset == 'veryslow':
        return 'p7'
    return None


def map_amf_preset(output_video_preset: OutputVideoPreset) -> Optional[str]:
    if output_video_preset in ['ultrafast', 'superfast', 'veryfast']:
        return 'speed'
    if output_video_preset in ['faster', 'fast', 'medium']:
        return 'balanced'
    if output_video_preset in ['slow', 'slower', 'veryslow']:
        return 'quality'
    return None


# Custom commands for AUTO extension
def extract_audio_from_video(target_path: str) -> Optional[str]:
    audio_path = target_path.replace('.mp4', '.wav')
    commands = ['-i', target_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '2', '-y', audio_path]
    print(f"Extracting audio from video: '{' '.join(commands)}'")
    if run_ffmpeg_progress(commands):
        return audio_path

    return None


def run_ffmpeg_progress(args: List[str], description: str = "Processing") -> bool:
    commands = ['ffmpeg', '-hide_banner', '-loglevel', 'error']
    commands.extend(args)
    print(f"Executing ffmpeg: '{' '.join(commands)}'")
    status = FFStatus()
    try:
        ff = FfmpegProgress(commands)
        with mytqdm(total=100, position=1, desc=description, state=status) as pbar:
            for progress in ff.run_command_with_progress():
                pbar.update(progress - pbar.n)
        return True

    except Exception as e:
        logger.debug(f"Exception in run_ffmpeg_progress: {e} at {traceback.print_exc()}")
        return False
