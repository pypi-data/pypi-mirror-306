import cv2 as cv
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import PoseLandmarker
from mediapipe.tasks.python.vision import PoseLandmarkerOptions
from mediapipe.tasks.python.vision import RunningMode

from .mediapipe_pose import calculate_pose_landmarks_angles_values
from .mediapipe_pose import calculate_pose_world_landmarks_angles_values
from .mediapipe_pose import get_pose_landmarks_angles
from .mediapipe_pose import get_pose_landmarks_frame
from .mediapipe_pose import get_pose_world_landmarks_angles
from .mediapipe_pose import read_pose_landmarks
from .mediapipe_pose import read_pose_world_landmarks
from .mediapipe_pose_video import MediapipePoseVideo
from .mediapipe_pose_video import VideoFrame
from .mediapipe_pose_video import VideoFrames
from .mediapipe_pose_video import VideoProp


# 视频文件
class MediapipePoseVideoBase(MediapipePoseVideo):

    def __init__(self, model_path: str, video_path: str, video_frames_size: int, angles: list):
        self.model_path = model_path
        self.video_path = video_path
        self.video_frames_size = video_frames_size
        self.angles = angles

        # 模型
        self.pose_landmarker = PoseLandmarker.create_from_options(PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=self.model_path),
            running_mode=RunningMode.VIDEO))

        # 视频
        self.video_cap = cv.VideoCapture(self.video_path)
        video_prop_fps = self.video_cap.get(cv.CAP_PROP_FPS)
        video_prop_frame_count = self.video_cap.get(cv.CAP_PROP_FRAME_COUNT)
        video_prop_frame_width = self.video_cap.get(cv.CAP_PROP_FRAME_WIDTH)
        video_prop_frame_height = self.video_cap.get(cv.CAP_PROP_FRAME_HEIGHT)

        # 视频属性
        self.video_prop = VideoProp(
            video_prop_fps=video_prop_fps,
            video_prop_frame_count=video_prop_frame_count,
            video_prop_frame_width=video_prop_frame_width,
            video_prop_frame_height=video_prop_frame_height)

        # 帧数据
        self.video_frame = None
        self.video_frame_image = None

        # 帧数据列表
        self.video_frames = VideoFrames(
            frames_index=[],
            frames_pose_landmarks_angles_values=[],
            frames_pose_world_landmarks_angles_values=[])

    def read(self) -> bool:
        ret, frame = self.video_cap.read()
        if ret:
            pos_index = self.video_cap.get(cv.CAP_PROP_POS_FRAMES)
            pos_timestamp = self.video_cap.get(cv.CAP_PROP_POS_MSEC)

            frame_index = int(pos_index)
            frame_timestamp = int(pos_timestamp)
            frame_width = int(self.video_prop.video_prop_frame_width)
            frame_height = int(self.video_prop.video_prop_frame_height)

            # 检测帧
            pose_landmarker_result = self.pose_landmarker.detect_for_video(
                mp.Image(image_format=mp.ImageFormat.SRGB, data=frame),
                frame_timestamp)

            # 读取地标
            frame_pose_landmarks = read_pose_landmarks(pose_landmarker_result)
            frame_pose_world_landmarks = read_pose_world_landmarks(pose_landmarker_result)
            frame_pose_landmarks_frame = get_pose_landmarks_frame(
                frame_pose_landmarks,
                frame_width,
                frame_height)

            # 获取角度坐标
            pose_landmarks_angles = get_pose_landmarks_angles(
                frame_pose_landmarks,
                self.angles)
            pose_world_landmarks_angles = get_pose_world_landmarks_angles(
                frame_pose_world_landmarks,
                self.angles)

            # 计算角度值
            frame_pose_landmarks_angles_values = calculate_pose_landmarks_angles_values(
                pose_landmarks_angles)
            frame_pose_world_landmarks_angles_values = calculate_pose_world_landmarks_angles_values(
                pose_world_landmarks_angles)

            self.video_frame = VideoFrame(
                frame_index=frame_index,
                frame_timestamp=frame_timestamp,
                frame_width=frame_width,
                frame_height=frame_height,
                frame_pose_landmarks=frame_pose_landmarks,
                frame_pose_landmarks_frame=frame_pose_landmarks_frame,
                frame_pose_world_landmarks=frame_pose_world_landmarks,
                frame_pose_landmarks_angles_values=frame_pose_landmarks_angles_values,
                frame_pose_world_landmarks_angles_values=frame_pose_world_landmarks_angles_values)

            self.video_frame_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            # 帧数据列表
            if (self.video_frames is not None
                    and frame_pose_landmarks_angles_values is not None
                    and frame_pose_world_landmarks_angles_values is not None):
                self.video_frames.frames_index.append(frame_index)
                self.video_frames.frames_pose_landmarks_angles_values.append(
                    frame_pose_landmarks_angles_values)
                self.video_frames.frames_pose_world_landmarks_angles_values.append(
                    frame_pose_world_landmarks_angles_values)

                if len(self.video_frames.frames_index) > self.video_frames_size:
                    self.video_frames.frames_index.pop(0)
                    self.video_frames.frames_pose_landmarks_angles_values.pop(0)
                    self.video_frames.frames_pose_world_landmarks_angles_values.pop(0)

        return ret

    def get_angles(self) -> list:
        return self.angles

    def get_video_prop(self) -> VideoProp:
        return self.video_prop

    def get_video_frame(self) -> VideoFrame:
        return self.video_frame

    def get_video_frame_image(self):
        return self.video_frame_image

    def get_video_frames(self) -> VideoFrames:
        return self.video_frames

    def close(self):
        self.pose_landmarker.close()
        self.video_cap.release()
