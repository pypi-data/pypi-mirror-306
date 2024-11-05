import math

from mediapipe.python.solutions.pose import PoseLandmark
from mediapipe.tasks.python.vision import PoseLandmarkerResult

# 默认角度
ANGLE_DEFINES = [
    # 左大臂
    [PoseLandmark.LEFT_SHOULDER, PoseLandmark.LEFT_ELBOW,
     PoseLandmark.LEFT_SHOULDER, PoseLandmark.RIGHT_SHOULDER],
    [PoseLandmark.LEFT_SHOULDER, PoseLandmark.LEFT_ELBOW,
     PoseLandmark.LEFT_SHOULDER, PoseLandmark.LEFT_HIP],
    # 右大臂
    [PoseLandmark.RIGHT_SHOULDER, PoseLandmark.RIGHT_ELBOW,
     PoseLandmark.RIGHT_SHOULDER, PoseLandmark.LEFT_SHOULDER],
    [PoseLandmark.RIGHT_SHOULDER, PoseLandmark.RIGHT_ELBOW,
     PoseLandmark.RIGHT_SHOULDER, PoseLandmark.RIGHT_HIP],
    # 左大腿
    [PoseLandmark.LEFT_HIP, PoseLandmark.LEFT_KNEE,
     PoseLandmark.LEFT_HIP, PoseLandmark.RIGHT_HIP],
    [PoseLandmark.LEFT_HIP, PoseLandmark.LEFT_KNEE,
     PoseLandmark.LEFT_HIP, PoseLandmark.LEFT_SHOULDER],
    # 右大腿
    [PoseLandmark.RIGHT_HIP, PoseLandmark.RIGHT_KNEE,
     PoseLandmark.RIGHT_HIP, PoseLandmark.LEFT_HIP],
    [PoseLandmark.RIGHT_HIP, PoseLandmark.RIGHT_KNEE,
     PoseLandmark.RIGHT_HIP, PoseLandmark.RIGHT_SHOULDER],
    # 左小臂
    [PoseLandmark.LEFT_ELBOW, PoseLandmark.LEFT_SHOULDER,
     PoseLandmark.LEFT_ELBOW, PoseLandmark.LEFT_WRIST],
    # 右小臂
    [PoseLandmark.RIGHT_ELBOW, PoseLandmark.RIGHT_SHOULDER,
     PoseLandmark.RIGHT_ELBOW, PoseLandmark.RIGHT_WRIST],
    # 左小腿
    [PoseLandmark.LEFT_KNEE, PoseLandmark.LEFT_HIP,
     PoseLandmark.LEFT_KNEE, PoseLandmark.LEFT_ANKLE],
    # 右小腿
    [PoseLandmark.RIGHT_KNEE, PoseLandmark.RIGHT_HIP,
     PoseLandmark.RIGHT_KNEE, PoseLandmark.RIGHT_ANKLE]]


# 读取骨骼点2D坐标
def read_pose_landmarks(result: PoseLandmarkerResult):
    if result.pose_landmarks is not None and len(result.pose_landmarks) > 0:
        landmarks = [result.pose_landmarks[0][lm] for lm in PoseLandmark]
        return [(lm.x, lm.y, lm.z) for lm in landmarks]

    return None


# 读取骨骼点3D坐标
def read_pose_world_landmarks(result: PoseLandmarkerResult):
    if result.pose_world_landmarks is not None and len(result.pose_world_landmarks) > 0:
        landmarks = [result.pose_world_landmarks[0][lm] for lm in PoseLandmark]
        return [(lm.x, lm.y, lm.z) for lm in landmarks]

    return None


# 获取骨骼点2D坐标(帧相对坐标)
def get_pose_landmarks_frame(pose_landmarks: list, width: int, height: int):
    if pose_landmarks is not None and len(pose_landmarks) > 0:
        return [(width * lm[0], height * lm[1]) for lm in pose_landmarks]

    return None


# 获取角度骨骼点2D坐标
def get_pose_landmarks_angles(pose_landmarks: list, angles: list):
    if pose_landmarks is not None and len(pose_landmarks) > 0:
        pose_landmarks_angles = []
        for define in angles:
            pose_landmarks_angles.append([
                pose_landmarks[define[0]],
                pose_landmarks[define[1]],
                pose_landmarks[define[2]],
                pose_landmarks[define[3]]])

        return pose_landmarks_angles

    return None


# 获取角度骨骼点3D坐标
def get_pose_world_landmarks_angles(pose_world_landmarks: list, angles: list):
    if pose_world_landmarks is not None and len(pose_world_landmarks) > 0:
        pose_world_landmarks_angles = []
        for define in angles:
            pose_world_landmarks_angles.append([
                pose_world_landmarks[define[0]],
                pose_world_landmarks[define[1]],
                pose_world_landmarks[define[2]],
                pose_world_landmarks[define[3]]])

        return pose_world_landmarks_angles

    return None


# 计算角度骨骼点2D坐标角度值
def calculate_pose_landmarks_angles_values(pose_landmarks_angles: list):
    if pose_landmarks_angles is not None and len(pose_landmarks_angles) > 0:
        pose_landmarks_angles_values = []
        for landmarks in pose_landmarks_angles:
            pose_landmarks_angles_values.append(calculate_pose_landmarks_angle(
                landmarks[0],
                landmarks[1],
                landmarks[2],
                landmarks[3]))

        return pose_landmarks_angles_values

    return None


# 计算角度骨骼点3D坐标角度值
def calculate_pose_world_landmarks_angles_values(pose_world_landmarks_angles: list):
    if pose_world_landmarks_angles is not None and len(pose_world_landmarks_angles) > 0:
        pose_world_landmarks_angles_values = []
        for landmarks in pose_world_landmarks_angles:
            pose_world_landmarks_angles_values.append(calculate_pose_world_landmarks_angle(
                landmarks[0],
                landmarks[1],
                landmarks[2],
                landmarks[3]))

        return pose_world_landmarks_angles_values

    return None


# 计算2D坐标夹角
def calculate_pose_landmarks_angle(
        landmark1: list,
        landmark2: list,
        landmark3: list,
        landmark4: list):
    a = [landmark2[0] - landmark1[0],
         landmark2[1] - landmark1[1],
         landmark2[2] - landmark1[2]]
    b = [landmark4[0] - landmark3[0],
         landmark4[1] - landmark3[1],
         landmark4[2] - landmark3[2]]

    dot_product = sum([a[i] * b[i] for i in range(3)])
    anorm = math.sqrt(sum([a[i] ** 2 for i in range(3)]))
    bnorm = math.sqrt(sum([b[i] ** 2 for i in range(3)]))
    if anorm == 0 or bnorm == 0:
        return 0

    radian = math.acos(dot_product / (anorm * bnorm))
    angle = math.degrees(radian)
    # angle = round(angle)
    return angle


# 计算3D坐标夹角
# 0-180
def calculate_pose_world_landmarks_angle(
        landmark1: list,
        landmark2: list,
        landmark3: list,
        landmark4: list):
    a = [landmark2[0] - landmark1[0],
         landmark2[1] - landmark1[1],
         landmark2[2] - landmark1[2]]
    b = [landmark4[0] - landmark3[0],
         landmark4[1] - landmark3[1],
         landmark4[2] - landmark3[2]]

    dot_product = sum([a[i] * b[i] for i in range(3)])
    anorm = math.sqrt(sum([a[i] ** 2 for i in range(3)]))
    bnorm = math.sqrt(sum([b[i] ** 2 for i in range(3)]))
    if anorm == 0 or bnorm == 0:
        return 0

    radian = math.acos(dot_product / (anorm * bnorm))
    angle = math.degrees(radian)
    # angle = round(angle)
    return angle
