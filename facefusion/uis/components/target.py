import os.path
from typing import Tuple, Optional, List

import gradio

from facefusion import wording, state_manager
from facefusion.download import download_video
from facefusion.face_store import clear_reference_faces, clear_static_faces
from facefusion.ffmpeg import extract_audio_from_video
from facefusion.filesystem import is_image, is_video, is_url, TEMP_DIRECTORY_PATH, get_file_size
from facefusion.uis.components.face_selector import clear_selected_faces
from facefusion.uis.core import register_ui_component, get_ui_component
from facefusion.uis.typing import File, ComponentOptions
from facefusion.vision import normalize_frame_color, get_video_frame

FILE_SIZE_LIMIT = 512 * 1024 * 1024
TARGET_FILE: Optional[gradio.File] = None
TARGET_IMAGE: Optional[gradio.Image] = None
TARGET_VIDEO: Optional[gradio.Video] = None
TARGET_PATH: Optional[gradio.Text] = None
SYNC_VIDEO_LIP: Optional[gradio.Checkbox] = None
SOURCE_FILES: Optional[gradio.File] = None


def render() -> None:
    global TARGET_FILE
    global TARGET_IMAGE
    global TARGET_VIDEO
    global TARGET_PATH
    global SYNC_VIDEO_LIP
    target_path = state_manager.get_item('target_path')
    is_target_path = is_url(target_path)
    is_target_image = is_image(target_path)
    is_target_video = is_video(target_path)
    TARGET_PATH = gradio.Text(
        label="Target URL/Remote Path",
        value=target_path if is_target_path else None,
        elem_id='ff_target_path',
    )
    TARGET_FILE = gradio.File(
        label = wording.get('uis.target_file'),
        file_count='single',
        file_types=
        [
            'image',
            'video'
        ],
        value=state_manager.get_item('target_path') if is_target_image or is_target_video else None
    )
    target_image_options: ComponentOptions = \
        {
            'show_label': False,
            'visible': False
        }
    target_video_options: ComponentOptions = \
        {
            'show_label': False,
            'visible': False
        }	
    if is_target_image:
        target_image_options['value'] = TARGET_FILE.value.get('path')
        target_image_options['visible'] = True
    if is_target_video:
        if get_file_size(state_manager.get_item('target_path')) > FILE_SIZE_LIMIT:
            preview_vision_frame = normalize_frame_color(get_video_frame(state_manager.get_item('target_path')))
            target_image_options['value'] = preview_vision_frame
            target_image_options['visible'] = True
        else:
            target_video_options['value'] = TARGET_FILE.value.get('path')
            target_video_options['visible'] = True
    TARGET_IMAGE = gradio.Image(**target_image_options)
    TARGET_VIDEO = gradio.Video(**target_video_options)
    SYNC_VIDEO_LIP = gradio.Checkbox(
        label="Sync Lips to Audio",
        value=state_manager.get_item("sync_video_lip") and is_target_video,
        visible=is_target_video and "lip_syncer" in state_manager.get_item("frame_processors"),
        elem_id='sync_video_lip'
    )
    register_ui_component('target_image', TARGET_IMAGE)
    register_ui_component('target_video', TARGET_VIDEO)
    register_ui_component('target_file', TARGET_FILE)
    register_ui_component('sync_video_lip', SYNC_VIDEO_LIP)


def listen() -> None:
    TARGET_PATH.input(update_from_path, inputs=TARGET_PATH,
                      outputs=[TARGET_IMAGE, TARGET_VIDEO, TARGET_PATH, TARGET_FILE])
    TARGET_FILE.change(update, inputs=TARGET_FILE, outputs=[TARGET_IMAGE, TARGET_VIDEO, TARGET_PATH, SYNC_VIDEO_LIP])
    global SOURCE_FILES
    SOURCE_FILES = get_ui_component('source_file')
    SYNC_VIDEO_LIP.change(update_sync_video_lip, inputs=[SYNC_VIDEO_LIP, SOURCE_FILES], outputs=[SOURCE_FILES])


def update_from_path(path: str) -> Tuple[gradio.update, gradio.update, gradio.update, gradio.update]:
    # Returns gr.Image, gr.Video, gr.Text, gr.Checkbox
    out_image = gradio.update(visible=False)
    out_video = gradio.update(visible=False)
    out_path = gradio.update(visible=False)
    out_file = gradio.update(visible=True)

    root_path = state_manager.get_item('restricted_path') if state_manager.get_item('restricted_path') else "/mnt/private"
    abs_path = os.path.abspath(path)
    if not abs_path.startswith(root_path) and not abs_path.startswith(TEMP_DIRECTORY_PATH) and not is_url(path):
        path = None

    if is_url(path):
        print(f"Downloading video from {path}")
        path = download_video(path)

    if not path:
        out_path = gradio.update(value=None, visible=True)
        return out_image, out_video, out_path, out_file

    if is_image(path):
        state_manager.set_item('target_path', path)
        out_image = gradio.update(value=path, visible=True)
        out_file = gradio.update(value=path, visible=True)

    elif is_video(path):
        print(f"Video path: {path}")
        state_manager.set_item('target_path', path)
        out_video = gradio.update(value=path, visible=True)
        out_file = gradio.update(value=path, visible=True)

    else:
        state_manager.set_item('target_path', None)
    return out_image, out_video, out_path, out_file


def update(file: File) -> Tuple[gradio.Image, gradio.Video, gradio.Text, gradio.Checkbox]:
    # Returns gr.Image, gr.Video, gr.Text, gr.Checkbox
    clear_reference_faces()
    clear_static_faces()
    clear_selected_faces()
    file_path = file.name if file else None
    if file_path and is_image(file_path):
        state_manager.set_item('target_path', file_path)
        return (gradio.update(value=file_path, visible=False),
                gradio.update(value=file_path, visible=True),
                gradio.update(visible=False),
                gradio.update(visible=False))
    if file_path and is_video(file_path):
        state_manager.set_item('target_path', file_path)
        return (gradio.update(value=file_path, visible=False),
                gradio.update(value=file_path, visible=True),
                gradio.update(visible=False),
                gradio.update(visible=True))
    state_manager.clear_item('target_path')
    return (gradio.update(value=None, visible=False),
            gradio.update(value=None, visible=False),
            gradio.update(visible=True),
            gradio.update(visible=False))


def update_sync_video_lip(sync_video_lip: bool, files: List[File]) -> None:
    state_manager.set_item("sync_video_lip", sync_video_lip)
    if sync_video_lip:
        target_video_path = state_manager.get_item('target_path')
        if target_video_path and is_video(target_video_path) and os.path.exists(target_video_path):
            file_names = [file.name for file in files] if files else []
            target_video_extension = os.path.splitext(target_video_path)[1]
            audio_path = target_video_path.replace(target_video_extension, '.mp3')
            if not os.path.exists(audio_path):
                audio_path = extract_audio_from_video(target_video_path)
            if audio_path not in file_names:
                file_names.append(audio_path)
            return gradio.update(value=file_names)
    return gradio.update()
