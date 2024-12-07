from typing import Any, Dict, List, Literal, TypedDict

from numpy._typing import NDArray

from facefusion.typing import AppContext, AudioFrame, Face, FaceSet, VisionFrame

AgeModifierModel = Literal['styleganex_age']
ExpressionRestorerModel = Literal['live_portrait']
FaceDebuggerItem = Literal[
    'bounding-box', 'face-landmark-5', 'face-landmark-5/68', 'face-landmark-68', 'face-landmark-68/5', 'face-mask', 'face-detector-score', 'face-landmarker-score', 'age', 'gender', 'race']
FaceEditorModel = Literal['live_portrait']
FaceEnhancerModel = Literal[
    'codeformer', 'gfpgan_1.2', 'gfpgan_1.3', 'gfpgan_1.4', 'gpen_bfr_256', 'gpen_bfr_512', 'gpen_bfr_1024', 'gpen_bfr_2048', 'restoreformer_plus_plus']
FaceSwapperModel = Literal[
    'blendswap_256', 'ghost_1_256', 'ghost_2_256', 'ghost_3_256', 'inswapper_128', 'inswapper_128_fp16', 'simswap_256', 'simswap_unofficial_512', 'uniface_256']
FrameColorizerModel = Literal['ddcolor', 'ddcolor_artistic', 'deoldify', 'deoldify_artistic', 'deoldify_stable']
FrameEnhancerModel = Literal[
    'clear_reality_x4', 'lsdir_x4', 'nomos8k_sc_x4', 'real_esrgan_x2', 'real_esrgan_x2_fp16', 'real_esrgan_x4', 'real_esrgan_x4_fp16', 'real_hatgan_x4', 'real_esrgan_x8', 'real_esrgan_x8_fp16', 'span_kendata_x4', 'ultra_sharp_x4']
LipSyncerModel = Literal['wav2lip_96', 'wav2lip_gan_96']

FaceSwapperSet = Dict[FaceSwapperModel, List[str]]

AgeModifierInputs = TypedDict('AgeModifierInputs',
                              {
                                  'reference_faces': FaceSet,
                                  'reference_faces_2': FaceSet,
                                  'target_vision_frame': VisionFrame
                              })
ExpressionRestorerInputs = TypedDict('ExpressionRestorerInputs',
                                     {
                                         'reference_faces': FaceSet,
                                         'reference_faces_2': FaceSet,
                                         'source_vision_frame': VisionFrame,
                                         'target_vision_frame': VisionFrame
                                     })
FaceDebuggerInputs = TypedDict('FaceDebuggerInputs',
                               {
                                   'reference_faces': FaceSet,
                                   'reference_faces_2': FaceSet,
                                   'target_vision_frame': VisionFrame,
                                   'source_frame': VisionFrame,
                                   'target_frame_number': int
                               })
FaceEditorInputs = TypedDict('FaceEditorInputs',
                             {
                                 'reference_faces': FaceSet,
                                 'reference_faces_2': FaceSet,
                                 'target_vision_frame': VisionFrame
                             })
FaceEnhancerInputs = TypedDict('FaceEnhancerInputs',
                               {
                                   'reference_faces': FaceSet,
                                   'reference_faces_2': FaceSet,
                                   'target_vision_frame': VisionFrame
                               })
FaceSwapperInputs = TypedDict('FaceSwapperInputs',
                              {
                                  'reference_faces': FaceSet,
                                  'reference_faces_2': FaceSet,
                                  'source_face': Face,
                                  'source_face_2': Face,
                                  'target_vision_frame': VisionFrame,
                                  'target_frame_number': int
                              })
FrameColorizerInputs = TypedDict('FrameColorizerInputs',
                                 {
                                     'target_vision_frame': VisionFrame
                                 })
FrameEnhancerInputs = TypedDict('FrameEnhancerInputs',
                                {
                                    'target_vision_frame': VisionFrame
                                })

StyleChangerInputs = TypedDict('StyleChangerInputs',
                               {
                                   'target_vision_frame': VisionFrame
                               })
LipSyncerInputs = TypedDict('LipSyncerInputs',
                            {
                                'reference_faces': FaceSet,
                                'reference_faces_2': FaceSet,
                                'source_audio_frame': AudioFrame,
                                'source_audio_frame_2': AudioFrame,
                                'target_vision_frame': VisionFrame
                            })
ProcessorStateKey = Literal \
    [
    'age_modifier_model',
    'age_modifier_direction',
    'expression_restorer_model',
    'expression_restorer_factor',
    'face_debugger_items',
    'face_editor_model',
    'face_editor_eyebrow_direction',
    'face_editor_eye_gaze_horizontal',
    'face_editor_eye_gaze_vertical',
    'face_editor_eye_open_ratio',
    'face_editor_lip_open_ratio',
    'face_editor_mouth_grim',
    'face_editor_mouth_pout',
    'face_editor_mouth_purse',
    'face_editor_mouth_smile',
    'face_editor_mouth_position_horizontal',
    'face_editor_mouth_position_vertical',
    'face_editor_head_pitch',
    'face_editor_head_yaw',
    'face_editor_head_roll',
    'face_enhancer_model',
    'face_enhancer_blend',
    'face_swapper_model',
    'face_swapper_pixel_boost',
    'frame_colorizer_model',
    'frame_colorizer_size',
    'frame_colorizer_blend',
    'frame_enhancer_model',
    'frame_enhancer_blend',
    'lip_syncer_model'
]

ProcessorState = TypedDict('ProcessorState',
                           {
                               'age_modifier_model': AgeModifierModel,
                               'age_modifier_direction': int,
                               'expression_restorer_model': ExpressionRestorerModel,
                               'expression_restorer_factor': int,
                               'face_debugger_items': List[FaceDebuggerItem],
                               'face_editor_model': FaceEditorModel,
                               'face_editor_eyebrow_direction': float,
                               'face_editor_eye_gaze_horizontal': float,
                               'face_editor_eye_gaze_vertical': float,
                               'face_editor_eye_open_ratio': float,
                               'face_editor_lip_open_ratio': float,
                               'face_editor_mouth_grim': float,
                               'face_editor_mouth_pout': float,
                               'face_editor_mouth_purse': float,
                               'face_editor_mouth_smile': float,
                               'face_editor_mouth_position_horizontal': float,
                               'face_editor_mouth_position_vertical': float,
                               'face_editor_head_pitch': float,
                               'face_editor_head_yaw': float,
                               'face_editor_head_roll': float,
                               'face_enhancer_model': FaceEnhancerModel,
                               'face_enhancer_blend': int,
                               'face_swapper_model': FaceSwapperModel,
                               'face_swapper_pixel_boost': str,
                               'frame_colorizer_model': FrameColorizerModel,
                               'frame_colorizer_size': str,
                               'frame_colorizer_blend': int,
                               'frame_enhancer_model': FrameEnhancerModel,
                               'frame_enhancer_blend': int,
                               'lip_syncer_model': LipSyncerModel
                           })
ProcessorStateSet = Dict[AppContext, ProcessorState]
LivePortraitPitch = float
LivePortraitYaw = float
LivePortraitRoll = float
LivePortraitExpression = NDArray[Any]
LivePortraitFeatureVolume = NDArray[Any]
LivePortraitMotionPoints = NDArray[Any]
LivePortraitRotation = NDArray[Any]
LivePortraitScale = NDArray[Any]
LivePortraitTranslation = NDArray[Any]