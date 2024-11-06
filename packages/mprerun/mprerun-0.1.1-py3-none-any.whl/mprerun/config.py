from mprerun.pose.mediapipe_pose_config import MediapipePoseConfig
from pydantic import BaseModel


# 全局配置
class Config(BaseModel):
    pose: MediapipePoseConfig | None = None


def read_config(filename: str) -> Config:
    with open(filename, "r") as file:
        content = file.read()
        config = Config.model_validate_json(content)
        return config
