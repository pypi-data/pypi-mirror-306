from pydantic import BaseModel
from pydantic import ConfigDict


# 角度配置
class MediapipePoseAngleConfig(BaseModel):
    angles_path: str | None = None


# 视频配置
class MediapipePoseVideoConfig(BaseModel):
    model_path: str | None = None
    video_path: str | None = None
    video_data_path: str | None = None
    video_frames_size: int | None = 100

    # 设置保护命名空间为空(避免警告)
    model_config = ConfigDict(
        protected_namespaces=()
    )


# 显示配置
class MediapipePoseViewerConfig(BaseModel):
    image_show: bool | None = True
    image_quality: int | None = 10


# 姿势配置
class MediapipePoseConfig(BaseModel):
    angle: MediapipePoseAngleConfig | None = None
    video1: MediapipePoseVideoConfig | None = None
    video2: MediapipePoseVideoConfig | None = None
    viewer: MediapipePoseViewerConfig | None = None
