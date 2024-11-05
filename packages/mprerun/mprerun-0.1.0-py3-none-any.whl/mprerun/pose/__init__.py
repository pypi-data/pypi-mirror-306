from .mediapipe_pose import ANGLE_DEFINES
from .mediapipe_pose_config import MediapipePoseAngleConfig
from .mediapipe_pose_config import MediapipePoseConfig
from .mediapipe_pose_config import MediapipePoseVideoConfig
from .mediapipe_pose_video import AnglesData
from .mediapipe_pose_video import MediapipePoseVideo
from .mediapipe_pose_video_base import MediapipePoseVideoBase
from .mediapipe_pose_video_data import MediapipePoseVideoData
from .mediapipe_pose_video_viewer import show


# 入口
def main(pose: MediapipePoseConfig):
    if pose is not None:
        angles = get_angles(pose.angle)
        mv1 = get_mediapipe_pose_video(pose.video1, angles)
        mv2 = get_mediapipe_pose_video(pose.video2, angles)
        viewer = pose.viewer
        if mv1 is not None or mv2 is not None:
            show(mv1, mv2, viewer)


def get_mediapipe_pose_video(video: MediapipePoseVideoConfig, angles: list):
    if (video is not None
            and video.model_path is not None
            and video.video_path is not None
            and video.video_frames_size is not None):
        return MediapipePoseVideoBase(
            video.model_path,
            video.video_path,
            video.video_frames_size,
            angles)

    if (video is not None
            and video.video_data_path is not None
            and video.video_frames_size is not None):
        return MediapipePoseVideoData(
            video.video_data_path,
            video.video_frames_size,
            angles)

    return None


def get_angles(angle: MediapipePoseAngleConfig):
    if (angle is not None
            and angle.angles_path is not None):
        with open(angle.angles_path, "r") as file:
            content = file.read()
            data = AnglesData.model_validate_json(content)
            return data.angles

    return ANGLE_DEFINES
