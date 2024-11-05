from .mediapipe_pose_video import MediapipePoseVideo
from .mediapipe_pose_video import VideoData
from .mediapipe_pose_video import VideoFrame
from .mediapipe_pose_video import VideoFrames
from .mediapipe_pose_video import VideoProp


# 视频数据
class MediapipePoseVideoData(MediapipePoseVideo):

    def __init__(self, video_data_path: str, video_frames_size: int, angles: list):
        self.video_data_path = video_data_path
        self.video_frames_size = video_frames_size
        self.angles = angles

        with open(video_data_path, "r") as file:
            content = file.read()
            self.video_data = VideoData.model_validate_json(content)
            self.video_data_prop = self.video_data.video_data_prop
            self.video_data_frames = self.video_data.video_data_frames

            # 视频属性
            self.video_prop = self.video_data_prop

            # 帧数据
            self.index = 0
            self.video_frame = None
            self.video_frame_image = None

            # 帧数据列表
            self.video_frames = VideoFrames(
                frames_index=[],
                frames_pose_landmarks_angles_values=[],
                frames_pose_world_landmarks_angles_values=[])

    def read(self) -> bool:
        if self.index < len(self.video_data_frames):
            self.video_frame = self.video_data_frames[self.index]
            self.index += 1

            # 帧数据列表
            if (self.video_frames is not None
                    and self.video_frame.frame_pose_landmarks_angles_values is not None
                    and self.video_frame.frame_pose_world_landmarks_angles_values is not None):
                self.video_frames.frames_index.append(self.video_frame.frame_index)
                self.video_frames.frames_pose_landmarks_angles_values.append(
                    self.video_frame.frame_pose_landmarks_angles_values)
                self.video_frames.frames_pose_world_landmarks_angles_values.append(
                    self.video_frame.frame_pose_world_landmarks_angles_values)

                if len(self.video_frames.frames_index) > self.video_frames_size:
                    self.video_frames.frames_index.pop(0)
                    self.video_frames.frames_pose_landmarks_angles_values.pop(0)
                    self.video_frames.frames_pose_world_landmarks_angles_values.pop(0)

            return True

        return False

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
