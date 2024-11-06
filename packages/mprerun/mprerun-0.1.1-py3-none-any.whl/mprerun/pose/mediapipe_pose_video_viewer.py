import numpy as np
import rerun as rr
import rerun.blueprint as rrb
from loguru import logger
from mediapipe.python.solutions.pose import POSE_CONNECTIONS
from mediapipe.python.solutions.pose import PoseLandmark
from mprerun.dtw import dtw_distance

from .mediapipe_pose_config import MediapipePoseViewerConfig
from .mediapipe_pose_video import MediapipePoseVideo


# 显示
def show(mv1: MediapipePoseVideo, mv2: MediapipePoseVideo, viewer: MediapipePoseViewerConfig):
    # 初始化 Rerun SDK
    rr.init("mediapipe_pose_video_viewer")

    # 启动 Rerun Viewer
    rr.spawn(default_blueprint=rrb.Blueprint(
        rrb.Vertical(
            rrb.Horizontal(
                rrb.Spatial2DView(origin="/video1/video2d/frame", name="Video1 2D Frame"),
                rrb.Spatial3DView(origin="/video1/video2d/pose", name="Video1 2D Pose"),
                rrb.Spatial3DView(origin="/video1/video3d/pose", name="Video1 3D Pose"),
                rrb.TextDocumentView(origin="/video1/angles", name="Video1 Angles"),
                rrb.TextDocumentView(origin="/video1/properties", name="Video1 Properties")
            ),
            rrb.Horizontal(
                rrb.Spatial2DView(origin="/video2/video2d/frame", name="Video2 2D Frame"),
                rrb.Spatial3DView(origin="/video2/video2d/pose", name="Video2 2D Pose"),
                rrb.Spatial3DView(origin="/video2/video3d/pose", name="Video2 3D Pose"),
                rrb.TextDocumentView(origin="/video2/angles", name="Video2 Angles"),
                rrb.TextDocumentView(origin="/video2/properties", name="Video2 Properties")
            ),
            rrb.TimeSeriesView(origin="/distance2d", name="Distance 2D"),
            rrb.TimeSeriesView(origin="/distance3d", name="Distance 3D")
        ),
        rrb.TimePanel(expanded=False),
        rrb.SelectionPanel(expanded=False),
        rrb.BlueprintPanel(expanded=False)
    ))

    # 骨骼点连接
    rr.log("/",
           rr.AnnotationContext(
               rr.ClassDescription(
                   info=rr.AnnotationInfo(id=1, label="Pose"),
                   keypoint_annotations=[rr.AnnotationInfo(id=lm.value, label=lm.name) for lm in PoseLandmark],
                   keypoint_connections=POSE_CONNECTIONS,
               )),
           static=True)

    # 指定观察坐标系
    rr.log("/video1/video2d/pose", rr.ViewCoordinates.RIGHT_HAND_Y_DOWN, static=True)
    rr.log("/video1/video3d/pose", rr.ViewCoordinates.RIGHT_HAND_Y_DOWN, static=True)
    rr.log("/video2/video2d/pose", rr.ViewCoordinates.RIGHT_HAND_Y_DOWN, static=True)
    rr.log("/video2/video3d/pose", rr.ViewCoordinates.RIGHT_HAND_Y_DOWN, static=True)

    # 距离曲线样式
    rr.log("distance2d/normalized_distance",
           rr.SeriesPoint(
               color=[255, 0, 0],
               name="normalized_distance",
               marker="circle",
               marker_size=1),
           static=True)

    # 距离曲线样式
    rr.log("distance3d/normalized_distance",
           rr.SeriesPoint(
               color=[255, 0, 0],
               name="normalized_distance",
               marker="circle",
               marker_size=1),
           static=True)

    # 视频属性
    if mv1 is not None:
        rr.log("/video1/properties",
               rr.TextDocument(
                   video_properties_text(mv1),
                   media_type=rr.MediaType.MARKDOWN),
               static=True)

    # 视频属性
    if mv2 is not None:
        rr.log("/video2/properties",
               rr.TextDocument(
                   video_properties_text(mv2),
                   media_type=rr.MediaType.MARKDOWN),
               static=True)

    # 循环读取帧
    while True:
        ret1 = False
        ret2 = False
        if mv1 is not None:
            ret1 = mv1.read()
        if mv2 is not None:
            ret2 = mv2.read()

        # 结束退出
        if not ret1 and not ret2:
            break

        if ret1:
            video_frame = mv1.get_video_frame()
        else:
            video_frame = mv2.get_video_frame()

        # 设置帧索引和时间戳
        rr.set_time_sequence("frame_index", video_frame.frame_index)
        rr.set_time_seconds("frame_timestamp", video_frame.frame_timestamp / 1000)

        # 进度日志
        if video_frame.frame_index % 1800 == 0:
            logger.info("pose video frame index: {}", video_frame.frame_index)

        if ret1:
            if viewer.image_show and mv1.get_video_frame_image() is not None:
                rr.log("/video1/video2d/frame", rr.Image(mv1.get_video_frame_image())
                       .compress(jpeg_quality=viewer.image_quality))

            video_frame = mv1.get_video_frame()
            if video_frame.frame_pose_landmarks_frame is not None:
                rr.log("/video1/video2d/frame/points", rr.Points2D(
                    video_frame.frame_pose_landmarks_frame,
                    keypoint_ids=PoseLandmark,
                    class_ids=1,
                    radii=10))

            if video_frame.frame_pose_landmarks is not None:
                rr.log("/video1/video2d/pose/points", rr.Points3D(
                    video_frame.frame_pose_landmarks,
                    keypoint_ids=PoseLandmark,
                    class_ids=1,
                    radii=0.01))

            if video_frame.frame_pose_world_landmarks is not None:
                rr.log("/video1/video3d/pose/points", rr.Points3D(
                    video_frame.frame_pose_world_landmarks,
                    keypoint_ids=PoseLandmark,
                    class_ids=1,
                    radii=0.02))

            rr.log("/video1/angles", rr.TextDocument(
                frame_angles_text(mv1),
                media_type=rr.MediaType.MARKDOWN))

        else:
            # 清除数据
            rr.log("/video1", rr.Clear(recursive=True))

        if ret2:
            if viewer.image_show and mv2.get_video_frame_image() is not None:
                rr.log("/video2/video2d/frame", rr.Image(mv2.get_video_frame_image())
                       .compress(jpeg_quality=viewer.image_quality))

            video_frame = mv2.get_video_frame()
            if video_frame.frame_pose_landmarks_frame is not None:
                rr.log("/video2/video2d/frame/points", rr.Points2D(
                    video_frame.frame_pose_landmarks_frame,
                    keypoint_ids=PoseLandmark,
                    class_ids=1,
                    radii=10))

            if video_frame.frame_pose_landmarks is not None:
                rr.log("/video2/video2d/pose/points", rr.Points3D(
                    video_frame.frame_pose_landmarks,
                    keypoint_ids=PoseLandmark,
                    class_ids=1,
                    radii=0.01))

            if video_frame.frame_pose_world_landmarks is not None:
                rr.log("/video2/video3d/pose/points", rr.Points3D(
                    video_frame.frame_pose_world_landmarks,
                    keypoint_ids=PoseLandmark,
                    class_ids=1,
                    radii=0.02))

            rr.log("/video2/angles", rr.TextDocument(
                frame_angles_text(mv2),
                media_type=rr.MediaType.MARKDOWN))

        else:
            # 清除数据
            rr.log("/video2", rr.Clear(recursive=True))

        # 计算距离
        if ret1 and ret2:
            mv1_video_frames = mv1.get_video_frames()
            mv2_video_frames = mv2.get_video_frames()

            if (mv1_video_frames.frames_pose_landmarks_angles_values is not None
                    and mv2_video_frames.frames_pose_landmarks_angles_values is not None
                    and len(mv1_video_frames.frames_pose_landmarks_angles_values) > 0
                    and len(mv2_video_frames.frames_pose_landmarks_angles_values) > 0):
                # 角度数相等才能计算距离
                mv1_angles_size = len(mv1_video_frames.frames_pose_landmarks_angles_values[0])
                mv2_angles_size = len(mv2_video_frames.frames_pose_landmarks_angles_values[0])
                if mv1_angles_size == mv2_angles_size:
                    mv1_values = np.array(mv1_video_frames.frames_pose_landmarks_angles_values)
                    mv2_values = np.array(mv2_video_frames.frames_pose_landmarks_angles_values)
                    distance, normalized_distance = dtw_distance(mv1_values, mv2_values)
                    rr.log("distance2d/normalized_distance", rr.Scalar(normalized_distance))

            if (mv1_video_frames.frames_pose_world_landmarks_angles_values is not None
                    and mv2_video_frames.frames_pose_world_landmarks_angles_values is not None
                    and len(mv1_video_frames.frames_pose_world_landmarks_angles_values) > 0
                    and len(mv2_video_frames.frames_pose_world_landmarks_angles_values) > 0):
                # 角度数相等才能计算距离
                mv1_angles_size = len(mv1_video_frames.frames_pose_world_landmarks_angles_values[0])
                mv2_angles_size = len(mv2_video_frames.frames_pose_world_landmarks_angles_values[0])
                if mv1_angles_size == mv2_angles_size:
                    mv1_values = np.array(mv1_video_frames.frames_pose_world_landmarks_angles_values)
                    mv2_values = np.array(mv2_video_frames.frames_pose_world_landmarks_angles_values)
                    distance, normalized_distance = dtw_distance(mv1_values, mv2_values)
                    rr.log("distance3d/normalized_distance", rr.Scalar(normalized_distance))

    # 关闭
    if mv1 is not None:
        mv1.close()
    if mv2 is not None:
        mv2.close()


# 角度数据文本
def frame_angles_text(mv: MediapipePoseVideo):
    text = "|Angle|2D|3D|\n"
    text += "|-|-|-|\n"

    angles = mv.get_angles()
    video_frame = mv.get_video_frame()
    if angles is not None:
        for i in range(len(angles)):
            define = angles[i]
            text += f"|{define[0].value}-{define[1].value}={define[2].value}-{define[3].value}|"
            if video_frame.frame_pose_landmarks_angles_values is not None:
                text += f"{video_frame.frame_pose_landmarks_angles_values[i]}"
            text += "|"
            if video_frame.frame_pose_world_landmarks_angles_values is not None:
                text += f"{video_frame.frame_pose_world_landmarks_angles_values[i]}"
            text += "|\n"

    return text


# 视频属性文本
def video_properties_text(mv: MediapipePoseVideo):
    text = "|Property|Value|\n"
    text += "|-|-|\n"

    video_prop = mv.get_video_prop()
    if video_prop is not None:
        text += f"|video_prop_fps|{video_prop.video_prop_fps}|\n"
        text += f"|video_prop_frame_count|{video_prop.video_prop_frame_count}|\n"
        text += f"|video_prop_frame_width|{video_prop.video_prop_frame_width}|\n"
        text += f"|video_prop_frame_height|{video_prop.video_prop_frame_height}|\n"

    return text
