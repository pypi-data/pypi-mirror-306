from mediapipe.python.solutions.pose import PoseLandmark
from pydantic import BaseModel


# 视频属性
class VideoProp(BaseModel):
    video_prop_fps: float
    video_prop_frame_count: float
    video_prop_frame_width: float
    video_prop_frame_height: float


# 帧数据
class VideoFrame(BaseModel):
    frame_index: int
    frame_timestamp: int
    frame_width: int
    frame_height: int
    # 地标
    frame_pose_landmarks: list[list[float]] | None
    frame_pose_landmarks_frame: list[list[float]] | None
    frame_pose_world_landmarks: list[list[float]] | None
    # 角度
    frame_pose_landmarks_angles_values: list[float] | None
    frame_pose_world_landmarks_angles_values: list[float] | None


# 帧数据列表
class VideoFrames(BaseModel):
    frames_index: list[int]
    frames_pose_landmarks_angles_values: list[list[float]]
    frames_pose_world_landmarks_angles_values: list[list[float]]


# 视频数据
class VideoData(BaseModel):
    video_data_prop: VideoProp
    video_data_frames: list[VideoFrame]


# 角度数据
class AnglesData(BaseModel):
    angles: list[list[PoseLandmark]]


# 视频
class MediapipePoseVideo:

    def read(self) -> bool:
        pass

    def get_angles(self) -> list:
        pass

    def get_video_prop(self) -> VideoProp:
        pass

    def get_video_frame(self) -> VideoFrame:
        pass

    def get_video_frame_image(self):
        pass

    def get_video_frames(self) -> VideoFrames:
        pass

    def close(self):
        pass
