import os
import platform
import threading
from argparse import ArgumentParser
from typing import Any, List, Literal, Optional

import numpy
import onnx
import onnxruntime
from onnx import numpy_helper

import facefusion.globals
import facefusion.processors.frame.core as frame_processors
from facefusion import logger, wording, config
from facefusion.content_analyser import clear_content_analyser
from facefusion.download import conditional_download, is_download_done
from facefusion.face_analyser import get_one_face, get_average_face, get_many_faces, find_similar_faces, \
    clear_face_analyser
from facefusion.face_helper import warp_face_by_kps, paste_back
from facefusion.face_masker import clear_face_occluder, create_static_box_mask, create_occlusion_mask, \
    create_region_mask, clear_face_parser
from facefusion.face_store import get_reference_faces
from facefusion.ff_status import update_status, FFStatus
from facefusion.filesystem import is_file, is_image, are_images, is_video, resolve_relative_path
from facefusion.job_params import JobParams
from facefusion.processors.frame import choices as frame_processors_choices
from facefusion.processors.frame import globals as frame_processors_globals
from facefusion.typing import Face, Frame, Update_Process, ProcessMode, OptionsWithModel, Embedding, \
    FaceSet, ModelSet, Padding
from facefusion.vision import read_image, read_static_image, read_static_images, write_image
from modules.paths_internal import models_path

FRAME_PROCESSOR = None
JOB = JobParams()
MODEL_MATRIX = None
FACE_RECOGNITION = "reference"
EXECUTION_THREAD_COUNT = 1
REFERENCE_FACE_DISTANCE = 0.6
REFERENCE_FACE_POSITION = "center"
REFERENCE_FRAME_NUMBER = 0
REFERENCE_FACE_DICT = {}

THREAD_LOCK: threading.Lock = threading.Lock()
NAME = __name__.upper()
MODELS: ModelSet = \
    {
        'blendswap_256':
            {
                'type': 'blendswap',
                'url': 'https://github.com/facefusion/facefusion-assets/releases/download/models/blendswap_256.onnx',
                'path': resolve_relative_path('../.assets/models/blendswap_256.onnx'),
                'template': 'ffhq_512',
                'size': (512, 256),
                'mean': [0.0, 0.0, 0.0],
                'standard_deviation': [1.0, 1.0, 1.0]
            },
        'inswapper_128':
            {
                'type': 'inswapper',
                'url': 'https://github.com/facefusion/facefusion-assets/releases/download/models/inswapper_128.onnx',
                'path': resolve_relative_path('../.assets/models/inswapper_128.onnx'),
                'template': 'arcface_128_v2',
                'size': (128, 128),
                'mean': [0.0, 0.0, 0.0],
                'standard_deviation': [1.0, 1.0, 1.0]
            },
        'inswapper_128_fp16':
            {
                'type': 'inswapper',
                'url': 'https://github.com/facefusion/facefusion-assets/releases/download/models/inswapper_128_fp16.onnx',
                'path': resolve_relative_path('../.assets/models/inswapper_128_fp16.onnx'),
                'template': 'arcface_128_v2',
                'size': (128, 128),
                'mean': [0.0, 0.0, 0.0],
                'standard_deviation': [1.0, 1.0, 1.0]
            },
        'simswap_256':
            {
                'type': 'simswap',
                'url': 'https://github.com/facefusion/facefusion-assets/releases/download/models/simswap_256.onnx',
                'path': resolve_relative_path('../.assets/models/simswap_256.onnx'),
                'template': 'arcface_112_v1',
                'size': (112, 256),
                'mean': [0.485, 0.456, 0.406],
                'standard_deviation': [0.229, 0.224, 0.225]
            },
        'simswap_512_unofficial':
            {
                'type': 'simswap',
                'url': 'https://github.com/facefusion/facefusion-assets/releases/download/models/simswap_512_unofficial.onnx',
                'path': resolve_relative_path('../.assets/models/simswap_512_unofficial.onnx'),
                'template': 'arcface_112_v1',
                'size': (112, 512),
                'mean': [0.0, 0.0, 0.0],
                'standard_deviation': [1.0, 1.0, 1.0]
            }
    }
OPTIONS: Optional[OptionsWithModel] = None


def get_frame_processor() -> Any:
    global FRAME_PROCESSOR

    with THREAD_LOCK:
        if FRAME_PROCESSOR is None:
            model_path = get_options('model').get('path')
            model_url = get_options('model').get('url')
            conditional_download(os.path.dirname(model_path), [model_url])
            FRAME_PROCESSOR = onnxruntime.InferenceSession(model_path, providers=["CUDAExecutionProvider"])
    return FRAME_PROCESSOR


def clear_frame_processor() -> None:
    global FRAME_PROCESSOR

    FRAME_PROCESSOR = None


def get_model_matrix() -> Any:
    global MODEL_MATRIX

    with THREAD_LOCK:
        if MODEL_MATRIX is None:
            model_path = get_options('model').get('path')
            model = onnx.load(model_path)
            MODEL_MATRIX = numpy_helper.to_array(model.graph.initializer[-1])
    return MODEL_MATRIX


def clear_model_matrix() -> None:
    global MODEL_MATRIX

    MODEL_MATRIX = None


def get_options(key: Literal['model']) -> Any:
    global OPTIONS

    if OPTIONS is None:
        OPTIONS = \
            {
                'model': MODELS[frame_processors_globals.face_swapper_model]
            }
    return OPTIONS.get(key)


def set_options(key: Literal['model'], value: Any) -> None:
    global OPTIONS

    OPTIONS[key] = value


def register_args(program: ArgumentParser) -> None:
    if platform.system().lower() == 'darwin':
        face_swapper_model_fallback = 'inswapper_128'
    else:
        face_swapper_model_fallback = 'inswapper_128_fp16'
    program.add_argument('--face-swapper-model', help = wording.get('frame_processor_model_help'), default = config.get_str_value('frame_processors.face_swapper_model', face_swapper_model_fallback), choices = frame_processors_choices.face_swapper_models)


def apply_args(program: ArgumentParser) -> None:
    args = program.parse_args()
    frame_processors_globals.face_swapper_model = args.face_swapper_model
    if args.face_swapper_model == 'blendswap_256':
        facefusion.globals.face_recognizer_model = 'arcface_blendswap'
    if args.face_swapper_model == 'inswapper_128' or args.face_swapper_model == 'inswapper_128_fp16':
        facefusion.globals.face_recognizer_model = 'arcface_inswapper'
    if args.face_swapper_model == 'simswap_256' or args.face_swapper_model == 'simswap_512_unofficial':
        facefusion.globals.face_recognizer_model = 'arcface_simswap'


def pre_check() -> bool:
    download_directory_path = os.path.join(models_path, 'facefusion')
    model_url = get_options('model').get('url')
    conditional_download(download_directory_path, [model_url])
    return True


def post_check() -> bool:
    model_url = get_options('model').get('url')
    model_path = get_options('model').get('path')
    if not facefusion.globals.skip_download and not is_download_done(model_url, model_path):
        logger.error(wording.get('model_download_not_done') + wording.get('exclamation_mark'), NAME)
        return False
    elif not is_file(model_path):
        update_status(f"Can't find model: {model_path}")
        return False
    return True


def pre_process(mode: ProcessMode) -> bool:
    if not are_images(facefusion.globals.source_paths):
        logger.error(wording.get('select_image_source') + wording.get('exclamation_mark'), NAME)
        return False
    for source_frame in read_static_images(facefusion.globals.source_paths):
        if not get_one_face(source_frame):
            logger.error(wording.get('no_source_face_detected') + wording.get('exclamation_mark'), NAME)
            return False
    if mode in ['output', 'preview'] and not is_image(facefusion.globals.target_path) and not is_video(
            facefusion.globals.target_path):
        logger.error(wording.get('select_image_or_video_target') + wording.get('exclamation_mark'), NAME)
        return False
    if mode == 'output' and not facefusion.globals.output_path:
        logger.error(wording.get('select_file_or_directory_output') + wording.get('exclamation_mark'), NAME)
        return False
    return True


def post_process() -> None:
    read_static_image.cache_clear()
    if facefusion.globals.video_memory_strategy == 'strict' or facefusion.globals.video_memory_strategy == 'moderate':
        clear_frame_processor()
        clear_model_matrix()
    if facefusion.globals.video_memory_strategy == 'strict':
        clear_face_analyser()
        clear_content_analyser()
        clear_face_occluder()
        clear_face_parser()


def update_padding(padding: Padding, frame_number: int) -> Padding:
    if frame_number == -1:
        print("No frame number...")
        return padding

    disabled_times = facefusion.globals.mask_disabled_times
    enabled_times = facefusion.globals.mask_enabled_times

    # Get the latest start frame that is less than or equal to the current frame number
    latest_disabled_frame = max([frame for frame in disabled_times if frame <= frame_number], default=None)

    # Get the latest end frame that is less than or equal to the current frame number
    latest_enabled_frame = max([frame for frame in enabled_times if frame <= frame_number], default=None)

    # Determine if the current frame number is within a padding interval
    if latest_disabled_frame is not None and (
            latest_enabled_frame is None or latest_disabled_frame > latest_enabled_frame):
        # The latest keyframe is a start frame without a corresponding end frame, keep current padding
        new_padding = (0, 0, 0, 0)
        return new_padding
    return padding


def swap_face(source_face: Face, target_face: Face, temp_frame: Frame, frame_number=-1) -> Frame:
    model_template = get_options('model').get('template')
    model_size = get_options('model').get('size')
    crop_frame, affine_matrix = warp_face_by_kps(temp_frame, target_face.kps, model_template, model_size)
    padding = facefusion.globals.face_mask_padding
    padding = update_padding(padding, frame_number)
    crop_mask_list = []
    if 'box' in facefusion.globals.face_mask_types:
        crop_mask_list.append(create_static_box_mask(crop_frame.shape[:2][::-1], facefusion.globals.face_mask_blur,
                                                     padding))
    if 'occlusion' in facefusion.globals.face_mask_types:
        crop_mask_list.append(create_occlusion_mask(crop_frame))
    crop_frame = prepare_crop_frame(crop_frame)
    crop_frame = apply_swap(source_face, crop_frame)
    crop_frame = normalize_crop_frame(crop_frame)
    if 'region' in facefusion.globals.face_mask_types:
        crop_mask_list.append(create_region_mask(crop_frame, facefusion.globals.face_mask_regions))
    crop_mask = numpy.minimum.reduce(crop_mask_list).clip(0, 1)
    temp_frame = paste_back(temp_frame, crop_frame, crop_mask, affine_matrix)
    return temp_frame


def apply_swap(source_face : Face, crop_frame : Frame) -> Frame:
    frame_processor = get_frame_processor()
    model_type = get_options('model').get('type')
    frame_processor_inputs = {}

    for frame_processor_input in frame_processor.get_inputs():
        if frame_processor_input.name == 'source':
            if model_type == 'blendswap':
                frame_processor_inputs[frame_processor_input.name] = prepare_source_frame(source_face)
            else:
                frame_processor_inputs[frame_processor_input.name] = prepare_source_embedding(source_face)
        if frame_processor_input.name == 'target':
            frame_processor_inputs[frame_processor_input.name] = crop_frame  # type: ignore[assignment]
    crop_frame = frame_processor.run(None, frame_processor_inputs)[0][0]
    return crop_frame


def prepare_source_frame(source_face: Face) -> Frame:
    source_frame = read_static_image(facefusion.globals.source_paths[0])
    source_frame, _ = warp_face_by_kps(source_frame, source_face.kps, 'arcface_112_v2', (112, 112))
    source_frame = source_frame[:, :, ::-1] / 255.0
    source_frame = source_frame.transpose(2, 0, 1)
    source_frame = numpy.expand_dims(source_frame, axis=0).astype(numpy.float32)
    return source_frame


def prepare_source_embedding(source_face: Face) -> Embedding:
    model_type = get_options('model').get('type')
    if model_type == 'inswapper':
        model_matrix = get_model_matrix()
        source_embedding = source_face.embedding.reshape((1, -1))
        source_embedding = numpy.dot(source_embedding, model_matrix) / numpy.linalg.norm(source_embedding)
    else:
        source_embedding = source_face.normed_embedding.reshape(1, -1)
    return source_embedding


def prepare_crop_frame(crop_frame: Frame) -> Frame:
    model_mean = get_options('model').get('mean')
    model_standard_deviation = get_options('model').get('standard_deviation')
    crop_frame = crop_frame[:, :, ::-1] / 255.0
    crop_frame = (crop_frame - model_mean) / model_standard_deviation
    crop_frame = crop_frame.transpose(2, 0, 1)
    crop_frame = numpy.expand_dims(crop_frame, axis=0).astype(numpy.float32)
    return crop_frame


def normalize_crop_frame(crop_frame: Frame) -> Frame:
    crop_frame = crop_frame.transpose(1, 2, 0)
    crop_frame = (crop_frame * 255.0).round()
    crop_frame = crop_frame[:, :, ::-1]
    return crop_frame


def get_reference_frame(source_face: Face, target_face: Face, temp_frame: Frame) -> Frame:
    return swap_face(source_face, target_face, temp_frame)


def process_frame(source_face: Face, reference_faces: FaceSet, temp_frame: Frame, frame_number: int = -1) -> Frame:
    if 'reference' in facefusion.globals.face_selector_mode:
        similar_faces = find_similar_faces(temp_frame, reference_faces, facefusion.globals.reference_face_distance)
        if similar_faces:
            for similar_face in similar_faces:
                temp_frame = swap_face(source_face, similar_face, temp_frame, frame_number)
    if 'one' in facefusion.globals.face_selector_mode:
        target_face = get_one_face(temp_frame)
        if target_face:
            temp_frame = swap_face(source_face, target_face, temp_frame, frame_number)
    if 'many' in facefusion.globals.face_selector_mode:
        many_faces = get_many_faces(temp_frame)
        if many_faces:
            for target_face in many_faces:
                temp_frame = swap_face(source_face, target_face, temp_frame, frame_number)
    return temp_frame


def process_frames(source_paths: List[str], temp_frame_paths: List[str], update_progress: Update_Process,
                   status: FFStatus) -> None:
    source_frames = read_static_images(source_paths)
    source_face = get_average_face(source_frames)
    reference_faces = get_reference_faces() if 'reference' in facefusion.globals.face_selector_mode else None
    for temp_frame_path in temp_frame_paths:
        if status.cancelled:
            return temp_frame_paths
        temp_frame = read_image(temp_frame_path)
        frame_number = int(os.path.splitext(os.path.basename(temp_frame_path))[0])
        result_frame = process_frame(source_face, reference_faces, temp_frame, frame_number)
        write_image(temp_frame_path, result_frame)
        update_progress()
        if status.job_current % 120 == 0:
            status.update_preview(temp_frame_path)
    return temp_frame_paths


def process_image(source_paths: List[str], target_path: str, output_path: str) -> None:
    source_frames = read_static_images(source_paths)
    source_face = get_average_face(source_frames)
    reference_faces = get_reference_faces() if 'reference' in facefusion.globals.face_selector_mode else None
    target_frame = read_static_image(target_path)
    result_frame = process_frame(source_face, reference_faces, target_frame)
    write_image(output_path, result_frame)


def process_video(source_path: str, temp_frame_paths: List[str], status) -> None:
    frame_processors.multi_process_frames(source_path, temp_frame_paths, process_frames, status)