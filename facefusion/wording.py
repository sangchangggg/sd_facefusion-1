from typing import Any, Dict, Optional

WORDING: Dict[str, Any] = \
    {
        'analysing': 'Analysing',
        'choose_audio_source': 'Choose a audio for the source',
        'choose_image_or_video_target': 'Choose a image or video for the target',
        'choose_image_source': 'Choose a image for the source',
        'choose_video_target': 'Choose a video for the target',
        'clearing_temp': 'Clearing temporary resources',
        'colon': ':',
        'comma': ',',
        'conda_not_activated': 'Conda is not activated',
        'copying_image': 'Copying image with a resolution of {resolution}',
        'copying_image_failed': 'Copying image failed',
        'copying_image_succeed': 'Copying image succeed',
        'creating_temp': 'Creating temporary resources',
        'curl_not_installed': 'CURL is not installed',
        'deleting_corrupt_source': 'Deleting corrupt source for {source_file_name}',
        'downloading': 'Downloading',
        'exclamation_mark': '!',
        'extracting_frames': 'Extracting frames with a resolution of {resolution} and {fps} frames per second',
        'extracting_frames_failed': 'Extracting frames failed',
        'extracting_frames_succeed': 'Extracting frames succeed',
        'ffmpeg_not_installed': 'FFMpeg is not installed',
        'finalizing_image': 'Finalizing image with a resolution of {resolution}',
        'finalizing_image_skipped': 'Finalizing image skipped',
        'finalizing_image_succeed': 'Finalizing image succeed',
        'frame_processor_not_implemented': 'Frame processor {frame_processor} not implemented correctly',
        'frame_processor_not_loaded': 'Frame processor {frame_processor} could not be loaded',
        'job_all_deleted': 'Jobs deleted',
        'job_all_not_deleted': 'Jobs not deleted',
        'job_all_not_submitted': 'Jobs not submitted',
        'job_all_submitted': 'Jobs submitted',
        'job_created': 'Job {job_id} created',
        'job_deleted': 'Job {job_id} deleted',
        'job_not_created': 'Job {job_id} not created',
        'job_not_deleted': 'Job {job_id} not deleted',
        'job_not_submitted': 'Job {job_id} not submitted',
        'job_remix_step_added': 'Step {step_index} remixed from job {job_id}',
        'job_remix_step_not_added': 'Step {step_index} not remixed from job {job_id}',
        'job_step_added': 'Step added to job {job_id}',
        'job_step_inserted': 'Step {step_index} inserted to job {job_id}',
        'job_step_not_added': 'Step not added to job {job_id}',
        'job_step_not_inserted': 'Step {step_index} not inserted to job {job_id}',
        'job_step_not_removed': 'Step {step_index} not removed from job {job_id}',
        'job_step_removed': 'Step {step_index} removed from job {job_id}',
        'job_submitted': 'Job {job_id} submitted',
        'match_target_and_output_extension': 'Match the target and output extension',
        'merging_video': 'Merging video with a resolution of {resolution} and {fps} frames per second',
        'merging_video_failed': 'Merging video failed',
        'merging_video_succeed': 'Merging video succeed',
        'no_source_face_detected': 'No source face detected',
        'point': '.',
        'processing': 'Processing',
        'processing_image_failed': 'Processing to image failed',
        'processing_image_succeed': 'Processing to image succeed in {seconds} seconds',
        'processing_job_failed': 'Processing of job {job_id} failed',
        'processing_job_succeed': 'Processing of job {job_id} succeed',
        'processing_jobs_failed': 'Processing of all jobs failed',
        'processing_jobs_succeed': 'Processing of all job succeed',
        'processing_step': 'Processing step {step_current} of {step_total}',
        'processing_stopped': 'Processing stopped',
        'processing_video_failed': 'Processing to video failed',
        'processing_video_succeed': 'Processing to video succeed in {seconds} seconds',
        'processor_not_implemented': 'Processor {processor} not implemented correctly',
        'processor_not_loaded': 'Processor {processor} could not be loaded',
        'python_not_supported': 'Python version is not supported, upgrade to {version} or higher',
        'question_mark': '?',
        'replacing_audio_skipped': 'Replacing audio skipped',
        'replacing_audio_succeed': 'Replacing audio succeed',
        'restoring_audio_skipped': 'Restoring audio skipped',
        'restoring_audio_succeed': 'Restoring audio succeed',
        'retrying_job': 'Retrying failed job {job_id}',
        'retrying_jobs': 'Retrying all failed jobs',
        'running_job': 'Running queued job {job_id}',
        'running_jobs': 'Running all queued jobs',
        'skipping_audio': 'Skipping audio',
        'specify_image_or_video_output': 'Specify the output image or video within a directory',
        'stream_not_loaded': 'Stream {stream_mode} could not be loaded',
        'temp_frames_not_found': 'Temporary frames not found',
        'time_ago_days': '{days} days, {hours} hours and {minutes} minutes ago',
        'time_ago_hours': '{hours} hours and {minutes} minutes ago',
        'time_ago_minutes': '{minutes} minutes ago',
        'time_ago_now': 'just now',
        'ui_layout_not_implemented': 'UI layout {ui_layout} not implemented correctly',
        'ui_layout_not_loaded': 'UI layout {ui_layout} could not be loaded',
        'validating_hash_failed': 'Validating hash for {hash_file_name} failed',
        'validating_hash_succeed': 'Validating hash for {hash_file_name} succeed',
        'validating_source_failed': 'Validating source for {source_file_name} failed',
        'validating_source_succeed': 'Validating source for {source_file_name} succeed',
        'help': {
            'age_modifier_direction': 'specify the direction in which the age should be modified',
            'age_modifier_model': 'choose the model responsible for aging the face',
            'config_path': 'choose the config file to override defaults',
            'execution_device_id': 'specify the device used for processing',
            'execution_providers': 'accelerate the model inference using different providers (choices: {choices}, ...)',
            'execution_queue_count': 'specify the amount of frames each thread is processing',
            'execution_thread_count': 'specify the amount of parallel threads while processing',
            'expression_restorer_factor': 'restore factor of expression from the target face',
            'expression_restorer_model': 'choose the model responsible for restoring the expression',
            'face_analyser_order': 'specify the order in which the face analyser detects faces.',
            'face_debugger_items': 'load a single or multiple processors (choices: {choices})',
            'face_detector_angles': 'specify the angles to rotate the frame before detecting faces',
            'face_detector_model': 'choose the model responsible for detecting the faces',
            'face_detector_score': 'filter the detected faces base on the confidence score',
            'face_detector_size': 'specify the frame size provided to the face detector',
            'face_editor_eye_gaze_horizontal': 'specify the horizontal eye gaze',
            'face_editor_eye_gaze_vertical': 'specify the vertical eye gaze',
            'face_editor_eye_open_ratio': 'specify the ratio of eye opening',
            'face_editor_eyebrow_direction': 'specify the eyebrow direction',
            'face_editor_head_pitch': 'specify the head pitch',
            'face_editor_head_roll': 'specify the head roll',
            'face_editor_head_yaw': 'specify the head yaw',
            'face_editor_lip_open_ratio': 'specify the ratio of lip opening',
            'face_editor_model': 'choose the model responsible for editing the face',
            'face_editor_mouth_grim': 'specify the mouth grim',
            'face_editor_mouth_position_horizontal': 'specify the horizontal mouth position',
            'face_editor_mouth_position_vertical': 'specify the vertical mouth position',
            'face_editor_mouth_pout': 'specify the mouth pout',
            'face_editor_mouth_purse': 'specify the mouth purse',
            'face_editor_mouth_smile': 'specify the mouth smile',
            'face_enhancer_blend': 'blend the enhanced into the previous face',
            'face_enhancer_model': 'choose the model responsible for enhancing the face',
            'face_landmarker_model': 'choose the model responsible for detecting the face landmarks',
            'face_landmarker_score': 'filter the detected face landmarks base on the confidence score',
            'face_mask_blur': 'specify the degree of blur applied the box mask',
            'face_mask_padding': 'apply top, right, bottom and left padding to the box mask',
            'face_mask_regions': 'choose the facial features used for the region mask (choices: {choices})',
            'face_mask_types': 'mix and match different face mask types (choices: {choices})',
            'face_selector_age_end': 'filter the detected faces based the ending age',
            'face_selector_age_start': 'filter the detected faces based the starting age',
            'face_selector_gender': 'filter the detected faces based on their gender',
            'face_selector_mode': 'use reference based tracking or simple matching',
            'face_selector_order': 'specify the order of the detected faces',
            'face_selector_race': 'filter the detected faces based on their race',
            'face_swapper_model': 'choose the model responsible for swapping the face',
            'face_swapper_pixel_boost': 'choose the pixel boost resolution for the face swapper',
            'face_swapper_weight': 'specify the weight for the face swapper',
            'force_download': 'force automate downloads and exit',
            'frame_colorizer_blend': 'blend the colorized into the previous frame',
            'frame_colorizer_model': 'choose the model responsible for colorizing the frame',
            'frame_colorizer_size': 'specify the frame size provided to the frame colorizer',
            'frame_enhancer_blend': 'blend the enhanced into the previous frame',
            'frame_enhancer_model': 'choose the model responsible for enhancing the frame',
            'frame_processors': 'load a single or multiple frame processors. (choices: {choices}, ...)',
            'headless': 'run the program without a user interface',
            'headless_run': 'run the program in headless mode',
            'install_dependency': 'choose the variant of {dependency} to install',
            'job_add_step': 'add a step to a drafted job',
            'job_create': 'create a drafted job',
            'job_delete': 'delete a drafted, queued, failed or completed job',
            'job_delete_all': 'delete all drafted, queued, failed and completed jobs',
            'job_id': 'specify the job id',
            'job_insert_step': 'insert a step to a drafted job',
            'job_list': 'list jobs by status',
            'job_remix_step': 'remix a previous step from a drafted job',
            'job_remove_step': 'remove a step from a drafted job',
            'job_retry': 'retry a failed job',
            'job_retry_all': 'retry all failed jobs',
            'job_run': 'run a queued job',
            'job_run_all': 'run all queued jobs',
            'job_status': 'specify the job status',
            'job_submit': 'submit a drafted job to become a queued job',
            'job_submit_all': 'submit all drafted jobs to become a queued jobs',
            'jobs_path': 'specify the directory to store jobs',
            'keep_temp': 'keep the temporary resources after processing',
            'lip_syncer_model': 'choose the model responsible for syncing the lips',
            'log_level': 'adjust the message severity displayed in the terminal',
            'open_browser': 'open the browser once the program is ready',
            'output': 'specify the output file or directory',
            'output_audio_encoder': 'specify the encoder used for the audio output',
            'output_image_quality': 'specify the image quality which translates to the compression factor',
            'output_image_resolution': 'specify the image output resolution based on the target image',
            'output_path': 'specify the output image or video within a directory',
            'output_video_encoder': 'specify the encoder used for the video output',
            'output_video_fps': 'specify the video output fps based on the target video',
            'output_video_preset': 'balance fast video processing and video file size',
            'output_video_quality': 'specify the video quality which translates to the compression factor',
            'output_video_resolution': 'specify the video output resolution based on the target video',
            'reference_face_distance': 'specify the similarity between the reference face and target face',
            'reference_face_position': 'specify the position used to create the reference face',
            'reference_frame_number': 'specify the frame used to create the reference face',
            'run': 'run the program',
            'skip_audio': 'omit the audio from the target video',
            'skip_download': 'omit downloads and remote lookups',
            'skip_venv': 'skip the virtual environment check',
            'source': 'choose single or multiple source images or audios',
            'source_paths': 'choose single or multiple source images or audios',
            'step_index': 'specify the step index',
            'style_changer_model': 'choose the model responsible for changing the style',
            'style_changer_target': 'choose whether to apply the style to the source images, or target media',
            'system_memory_limit': 'limit the available RAM that can be used while processing',
            'target': 'choose single target image or video',
            'target_path': 'choose single target image or video',
            'temp_frame_format': 'specify the temporary resources format',
            'trim_frame_end': 'specify the ending frame of the target video',
            'trim_frame_start': 'specify the starting frame of the target video',
            'ui_layouts': 'launch a single or multiple UI layouts (choices: {choices}, ...)',
            'ui_workflow': 'choose the ui workflow',
            'video_memory_strategy': 'balance fast processing and low VRAM usage',
            'skip_conda': 'skip the conda environment check',
            'processors': 'load a single or multiple processors (choices: {choices}, ...)'
        },
        'about': {
            'become_a_member': 'become a member',
            'join_our_community': 'join our community',
            'read_the_documentation': 'read the documentation'
        },
        'uis': {
            'age_modifier_direction_slider': 'AGE MODIFIER DIRECTION',
            'age_modifier_model_dropdown': 'AGE MODIFIER MODEL',
            'apply_button': 'APPLY',
            'benchmark_cycles_slider': 'BENCHMARK CYCLES',
            'benchmark_results_dataframe': 'BENCHMARK RESULTS',
            'benchmark_runs_checkbox_group': 'BENCHMARK RUNS',
            'clear_button': 'CLEAR',
            'common_options_checkbox_group': 'OPTIONS',
            'donate_button': 'DONATE',
            'download_button': 'DOWNLOAD',
            'execution_providers_checkbox_group': 'EXECUTION PROVIDERS',
            'execution_queue_count_slider': 'EXECUTION QUEUE COUNT',
            'execution_thread_count_slider': 'EXECUTION THREAD COUNT',
            'expression_restorer_factor_slider': 'EXPRESSION RESTORER FACTOR',
            'expression_restorer_model_dropdown': 'EXPRESSION RESTORER MODEL',
            'face_analyser_age_dropdown': 'FACE ANALYSER AGE',
            'face_analyser_gender_dropdown': 'FACE ANALYSER GENDER',
            'face_analyser_order_dropdown': 'FACE ANALYSER ORDER',
            'face_debugger_items_checkbox_group': 'FACE DEBUGGER ITEMS',
            'face_detector_angles_checkbox_group': 'FACE DETECTOR ANGLES',
            'face_detector_model_dropdown': 'FACE DETECTOR MODEL',
            'face_detector_score_slider': 'FACE DETECTOR SCORE',
            'face_detector_size_dropdown': 'FACE DETECTOR SIZE',
            'face_editor_eye_gaze_horizontal_slider': 'FACE EDITOR EYE GAZE HORIZONTAL',
            'face_editor_eye_gaze_vertical_slider': 'FACE EDITOR EYE GAZE VERTICAL',
            'face_editor_eye_open_ratio_slider': 'FACE EDITOR EYE OPEN RATIO',
            'face_editor_eyebrow_direction_slider': 'FACE EDITOR EYEBROW DIRECTION',
            'face_editor_head_pitch_slider': 'FACE EDITOR HEAD PITCH',
            'face_editor_head_roll_slider': 'FACE EDITOR HEAD ROLL',
            'face_editor_head_yaw_slider': 'FACE EDITOR HEAD YAW',
            'face_editor_lip_open_ratio_slider': 'FACE EDITOR LIP OPEN RATIO',
            'face_editor_model_dropdown': 'FACE EDITOR MODEL',
            'face_editor_mouth_grim_slider': 'FACE EDITOR MOUTH GRIM',
            'face_editor_mouth_position_horizontal_slider': 'FACE EDITOR MOUTH POSITION HORIZONTAL',
            'face_editor_mouth_position_vertical_slider': 'FACE EDITOR MOUTH POSITION VERTICAL',
            'face_editor_mouth_pout_slider': 'FACE EDITOR MOUTH POUT',
            'face_editor_mouth_purse_slider': 'FACE EDITOR MOUTH PURSE',
            'face_editor_mouth_smile_slider': 'FACE EDITOR MOUTH SMILE',
            'face_enhancer_blend_slider': 'FACE ENHANCER BLEND',
            'face_enhancer_model_dropdown': 'FACE ENHANCER MODEL',
            'face_landmarker_model_dropdown': 'FACE LANDMARKER MODEL',
            'face_landmarker_score_slider': 'FACE LANDMARKER SCORE',
            'face_mask_blur_slider': 'FACE MASK BLUR',
            'face_mask_padding_bottom_slider': 'FACE MASK PADDING BOTTOM',
            'face_mask_padding_left_slider': 'FACE MASK PADDING LEFT',
            'face_mask_padding_right_slider': 'FACE MASK PADDING RIGHT',
            'face_mask_padding_top_slider': 'FACE MASK PADDING TOP',
            'face_mask_region_checkbox_group': 'FACE MASK REGIONS',
            'face_mask_regions_checkbox_group': 'FACE MASK REGIONS',
            'face_mask_types_checkbox_group': 'FACE MASK TYPES',
            'face_selector_age_range_slider': 'FACE SELECTOR AGE',
            'face_selector_gender_dropdown': 'FACE SELECTOR GENDER',
            'face_selector_mode_dropdown': 'FACE SELECTOR MODE',
            'face_selector_order_dropdown': 'FACE SELECTOR ORDER',
            'face_swapper_model_dropdown': 'FACE SWAPPER MODEL',
            'face_swapper_pixel_boost_dropdown': 'FACE SWAPPER PIXEL BOOST',
            'face_swapper_weight_slider': 'FACE SWAPPER WEIGHT',
            'frame_colorizer_blend_slider': 'FRAME COLORIZER BLEND',
            'frame_colorizer_model_dropdown': 'FRAME COLORIZER MODEL',
            'frame_colorizer_size_dropdown': 'FRAME COLORIZER SIZE',
            'frame_enhancer_blend_slider': 'FRAME ENHANCER BLEND',
            'frame_enhancer_model_dropdown': 'FRAME ENHANCER MODEL',
            'frame_processors_checkbox_group': 'FRAME PROCESSORS',
            'job_list_status_checkbox_group': 'JOB STATUS',
            'job_manager_job_action_dropdown': 'JOB_ACTION',
            'job_manager_job_id_dropdown': 'JOB ID',
            'job_manager_step_index_dropdown': 'STEP INDEX',
            'job_runner_job_action_dropdown': 'JOB ACTION',
            'job_runner_job_id_dropdown': 'JOB ID',
            'lip_syncer_model_dropdown': 'LIP SYNCER MODEL',
            'log_level_dropdown': 'LOG LEVEL',
            'output_audio_encoder_dropdown': 'OUTPUT AUDIO ENCODER',
            'output_image_or_video': 'OUTPUT',
            'output_image_quality_slider': 'OUTPUT IMAGE QUALITY',
            'output_image_resolution_dropdown': 'OUTPUT IMAGE RESOLUTION',
            'output_path_textbox': 'OUTPUT PATH',
            'output_video_encoder_dropdown': 'OUTPUT VIDEO ENCODER',
            'output_video_fps_slider': 'OUTPUT VIDEO FPS',
            'output_video_preset_dropdown': 'OUTPUT VIDEO PRESET',
            'output_video_quality_slider': 'OUTPUT VIDEO QUALITY',
            'output_video_resolution_dropdown': 'OUTPUT VIDEO RESOLUTION',
            'preview_frame_slider': 'PREVIEW FRAME',
            'preview_image': 'PREVIEW',
            'processors_checkbox_group': 'PROCESSORS',
            'reference_face_distance_slider': 'REFERENCE FACE DISTANCE',
            'reference_face_gallery': 'REFERENCE FACE',
            'reference_face_gallery_2': 'REFERENCE FACE 2',
            'refresh_button': 'REFRESH',
            'source_file': 'SOURCE',
            'source_file_2': 'SOURCE',
            'start_button': 'START',
            'stop_button': 'STOP',
            'style_changer_model_dropdown': 'SELECTED STYLE',
            'style_changer_target_radio': 'STYLE TARGET',
            'system_memory_limit_slider': 'SYSTEM MEMORY LIMIT',
            'target_file': 'TARGET',
            'target_url_textbox': 'TARGET URL',
            'temp_frame_format_dropdown': 'TEMP FRAME FORMAT',
            'terminal_textbox': 'TERMINAL',
            'trim_frame_end_slider': 'TRIM FRAME END',
            'trim_frame_slider': 'TRIM FRAME',
            'trim_frame_start_slider': 'TRIM FRAME START',
            'ui_workflow': 'UI WORKFLOW',
            'video_memory_strategy_dropdown': 'VIDEO MEMORY STRATEGY',
            'webcam_fps_slider': 'WEBCAM FPS',
            'webcam_image': 'WEBCAM',
            'webcam_mode_radio': 'WEBCAM MODE',
            'webcam_resolution_dropdown': 'WEBCAM RESOLUTION',
            'face_selector_race_dropdown': 'FACE SELECTOR RACE'
        }
    }


def get(key: str) -> Optional[str]:
    if '.' in key:
        section, name = key.split('.')
        if section in WORDING and name in WORDING[section]:
            value = WORDING[section][name]
            # Return Title Case version of the string
            return value.title() if isinstance(value, str) and section == "uis" else value
    if key in WORDING:
        return WORDING[key]
    return None
