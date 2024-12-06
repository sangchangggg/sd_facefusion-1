from facefusion import state_manager
from facefusion.filesystem import is_image, is_video, list_directory
from facefusion.jobs import job_store
from facefusion.normalizer import normalize_fps, normalize_padding
from facefusion.processors.core import get_processors_modules
from facefusion.typing import ApplyStateItem, Args
from facefusion.vision import create_image_resolutions, create_video_resolutions, detect_image_resolution, \
    detect_video_fps, detect_video_resolution, pack_resolution


def reduce_step_args(args: Args) -> Args:
    step_args = \
        {
            key: args[key] for key in args if key in job_store.get_step_keys()
        }
    return step_args


def collect_step_args() -> Args:
    step_args = \
        {
            key: state_manager.get_item(key) for key in job_store.get_step_keys()  # type:ignore[arg-type]
        }
    return step_args


def collect_job_args() -> Args:
    job_args = \
        {
            key: state_manager.get_item(key) for key in job_store.get_job_keys()  # type:ignore[arg-type]
        }
    return job_args


def apply_args(args: Args, apply_state_item: ApplyStateItem) -> None:
    # general
    apply_state_item('command', args.get('command'))
    # paths
    apply_state_item('jobs_path', args.get('jobs_path'))
    apply_state_item('source_paths', args.get('source_paths'))
    apply_state_item('target_path', args.get('target_path'))
    apply_state_item('output_path', args.get('output_path'))
    # face detector
    apply_state_item('face_detector_model', args.get('face_detector_model'))
    apply_state_item('face_detector_size', args.get('face_detector_size'))
    apply_state_item('face_detector_angles', args.get('face_detector_angles'))
    apply_state_item('face_detector_score', args.get('face_detector_score'))
    # face landmarker
    apply_state_item('face_landmarker_model', args.get('face_landmarker_model'))
    apply_state_item('face_landmarker_score', args.get('face_landmarker_score'))
    # face selector
    state_manager.init_item('face_selector_mode', args.get('face_selector_mode'))
    state_manager.init_item('face_selector_order', args.get('face_selector_order'))
    state_manager.init_item('face_selector_age_start', args.get('face_selector_age_start'))
    state_manager.init_item('face_selector_age_end', args.get('face_selector_age_end'))
    state_manager.init_item('face_selector_gender', args.get('face_selector_gender'))
    state_manager.init_item('face_selector_race', args.get('face_selector_race'))
    state_manager.init_item('reference_face_position', args.get('reference_face_position'))
    state_manager.init_item('reference_face_distance', args.get('reference_face_distance'))
    state_manager.init_item('reference_frame_number', args.get('reference_frame_number'))
    # face masker
    apply_state_item('face_mask_types', args.get('face_mask_types'))
    apply_state_item('face_mask_blur', args.get('face_mask_blur'))
    apply_state_item('face_mask_padding', normalize_padding(args.get('face_mask_padding')))
    apply_state_item('face_mask_regions', args.get('face_mask_regions'))
    # frame extraction
    apply_state_item('trim_frame_start', args.get('trim_frame_start'))
    apply_state_item('trim_frame_end', args.get('trim_frame_end'))
    apply_state_item('temp_frame_format', args.get('temp_frame_format'))
    apply_state_item('keep_temp', args.get('keep_temp'))
    # output creation
    apply_state_item('output_image_quality', args.get('output_image_quality'))
    if is_image(args.get('target_path')):
        output_image_resolution = detect_image_resolution(args.get('target_path'))
        output_image_resolutions = create_image_resolutions(output_image_resolution)
        if args.get('output_image_resolution') in output_image_resolutions:
            apply_state_item('output_image_resolution', args.get('output_image_resolution'))
        else:
            apply_state_item('output_image_resolution', pack_resolution(output_image_resolution))
    apply_state_item('output_audio_encoder', args.get('output_audio_encoder'))
    apply_state_item('output_video_encoder', args.get('output_video_encoder'))
    apply_state_item('output_video_preset', args.get('output_video_preset'))
    apply_state_item('output_video_quality', args.get('output_video_quality'))
    if is_video(args.get('target_path')):
        output_video_resolution = detect_video_resolution(args.get('target_path'))
        output_video_resolutions = create_video_resolutions(output_video_resolution)
        if args.get('output_video_resolution') in output_video_resolutions:
            apply_state_item('output_video_resolution', args.get('output_video_resolution'))
        else:
            apply_state_item('output_video_resolution', pack_resolution(output_video_resolution))
    if args.get('output_video_fps') or is_video(args.get('target_path')):
        output_video_fps = normalize_fps(args.get('output_video_fps')) or detect_video_fps(args.get('target_path'))
        apply_state_item('output_video_fps', output_video_fps)
    apply_state_item('skip_audio', args.get('skip_audio'))
    # processors
    available_processors = list_directory('facefusion/processors/modules')
    apply_state_item('processors', args.get('processors'))
    for processor_module in get_processors_modules(available_processors):
        processor_module.apply_args(args, apply_state_item)
    # uis
    apply_state_item('open_browser', args.get('open_browser'))
    apply_state_item('ui_layouts', args.get('ui_layouts'))
    apply_state_item('ui_workflow', args.get('ui_workflow'))
    # execution
    apply_state_item('execution_device_id', args.get('execution_device_id'))
    apply_state_item('execution_providers', args.get('execution_providers'))
    apply_state_item('execution_thread_count', args.get('execution_thread_count'))
    apply_state_item('execution_queue_count', args.get('execution_queue_count'))
    # memory
    apply_state_item('video_memory_strategy', args.get('video_memory_strategy'))
    apply_state_item('system_memory_limit', args.get('system_memory_limit'))
    # misc
    apply_state_item('skip_download', args.get('skip_download'))
    apply_state_item('log_level', args.get('log_level'))
    # jobs
    apply_state_item('job_id', args.get('job_id'))
    apply_state_item('job_status', args.get('job_status'))
    apply_state_item('step_index', args.get('step_index'))


def apply_globals(globals_dict: dict, init: bool = True) -> None:
    keys = [
        # general
        'command',
        # paths
        'jobs_path', 'source_paths', 'target_path', 'output_path',
        # face detector
        'face_detector_model', 'face_detector_size', 'face_detector_angles', 'face_detector_score',
        # face landmarker
        'face_landmarker_model', 'face_landmarker_score',
        # face selector
        'face_selector_mode', 'face_selector_order', 'face_selector_age_start',
        'face_selector_age_end', 'face_selector_gender', 'face_selector_race',
        'reference_face_position', 'reference_face_distance', 'reference_frame_number',
        # face masker
        'face_mask_types', 'face_mask_blur', 'face_mask_padding', 'face_mask_regions',
        # frame extraction
        'trim_frame_start', 'trim_frame_end', 'temp_frame_format', 'keep_temp',
        # output creation
        'output_image_quality', 'output_image_resolution', 'output_audio_encoder',
        'output_video_encoder', 'output_video_preset', 'output_video_quality',
        'output_video_resolution', 'output_video_fps', 'skip_audio',
        # processors
        'processors',
        # uis
        'open_browser', 'ui_layouts', 'ui_workflow',
        # execution
        'execution_device_id', 'execution_providers', 'execution_thread_count', 'execution_queue_count',
        # memory
        'video_memory_strategy', 'system_memory_limit',
        # misc
        'skip_download', 'log_level',
        # jobs
        'job_id', 'job_status', 'step_index'
    ]

    for key in keys:
        if key in globals_dict:
            value = globals_dict[key]
            if key == 'face_mask_padding':
                value = normalize_padding(value)
            elif key == 'output_video_fps':
                value = normalize_fps(value)
            elif key == 'output_image_resolution' and 'target_path' in globals_dict and is_image(
                    globals_dict['target_path']):
                output_image_resolution = detect_image_resolution(globals_dict['target_path'])
                output_image_resolutions = create_image_resolutions(output_image_resolution)
                if value not in output_image_resolutions:
                    value = pack_resolution(output_image_resolution)
            elif key == 'output_video_resolution' and 'target_path' in globals_dict and is_video(
                    globals_dict['target_path']):
                output_video_resolution = detect_video_resolution(globals_dict['target_path'])
                output_video_resolutions = create_video_resolutions(output_video_resolution)
                if value not in output_video_resolutions:
                    value = pack_resolution(output_video_resolution)
            elif key == 'output_video_fps' or (key == 'output_video_fps' and is_video(globals_dict['target_path'])):
                value = value or detect_video_fps(globals_dict['target_path'])

            if init:
                state_manager.init_item(key, value)
            else:
                state_manager.set_item(key, value)
        else:
            print(f"Key {key} not found in globals_dict.")

