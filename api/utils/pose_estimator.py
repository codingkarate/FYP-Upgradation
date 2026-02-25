# import cv2
# import mediapipe as mp
# import numpy as np
# import tempfile
# import math
# import os

# mp_pose = mp.solutions.pose


# # -----------------------------
# # Utility: Angle calculation
# # -----------------------------
# def calculate_angle(a, b, c):
#     a = np.array(a)
#     b = np.array(b)
#     c = np.array(c)

#     radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
#               np.arctan2(a[1] - b[1], a[0] - b[0])
#     angle = abs(radians * 180.0 / np.pi)

#     if angle > 180:
#         angle = 360 - angle

#     return angle


# # -----------------------------
# # Posture checks (6 exercises)
# # -----------------------------
# def check_squat_posture(lm):
#     hip = [lm[23].x, lm[23].y]
#     knee = [lm[25].x, lm[25].y]
#     ankle = [lm[27].x, lm[27].y]

#     angle = calculate_angle(hip, knee, ankle)

#     if angle < 70:
#         return {"fault": "Squat too deep", "risk": 65}
#     elif angle > 160:
#         return {"fault": "Insufficient squat depth", "risk": 55}
#     return {"fault": "Good posture", "risk": 25}


# def check_lunge_posture(lm):
#     hip = [lm[23].x, lm[23].y]
#     knee = [lm[25].x, lm[25].y]
#     ankle = [lm[27].x, lm[27].y]

#     angle = calculate_angle(hip, knee, ankle)

#     if angle < 75:
#         return {"fault": "Knee bending too much", "risk": 60}
#     elif angle > 160:
#         return {"fault": "Shallow lunge", "risk": 50}
#     return {"fault": "Good posture", "risk": 25}


# def check_pushup_posture(lm):
#     shoulder = [lm[11].x, lm[11].y]
#     elbow = [lm[13].x, lm[13].y]
#     wrist = [lm[15].x, lm[15].y]

#     angle = calculate_angle(shoulder, elbow, wrist)

#     if angle < 40:
#         return {"fault": "Elbow over-bending", "risk": 70}
#     elif angle > 170:
#         return {"fault": "Incomplete pushup", "risk": 55}
#     return {"fault": "Good posture", "risk": 30}


# def check_bridge_posture(lm):
#     shoulder = [lm[11].x, lm[11].y]
#     hip = [lm[23].x, lm[23].y]
#     knee = [lm[25].x, lm[25].y]

#     angle = calculate_angle(shoulder, hip, knee)

#     if angle < 150:
#         return {"fault": "Hips not lifted enough", "risk": 60}
#     elif angle > 185:
#         return {"fault": "Lower back overextension", "risk": 70}
#     return {"fault": "Good posture", "risk": 25}


# def check_leg_raise_posture(lm):
#     hip = [lm[23].x, lm[23].y]
#     knee = [lm[25].x, lm[25].y]
#     ankle = [lm[27].x, lm[27].y]

#     angle = calculate_angle(hip, knee, ankle)

#     if angle < 160:
#         return {"fault": "Knees bending during leg raise", "risk": 55}
#     return {"fault": "Good posture", "risk": 25}


# def check_mountain_climber_posture(lm):
#     shoulder = [lm[11].x, lm[11].y]
#     hip = [lm[23].x, lm[23].y]
#     ankle = [lm[27].x, lm[27].y]

#     angle = calculate_angle(shoulder, hip, ankle)

#     if angle < 150:
#         return {"fault": "Hips sagging", "risk": 65}
#     elif angle > 185:
#         return {"fault": "Hips too high", "risk": 60}
#     return {"fault": "Good posture", "risk": 30}


# # -----------------------------
# # Posture evaluator
# # -----------------------------
# def evaluate_posture(exercise, lm):
#     checks = {
#         "Jumping Squats": check_squat_posture,
#         "Lunges": check_lunge_posture,
#         "Pushups": check_pushup_posture,
#         "Bridges": check_bridge_posture,
#         "Leg Raises": check_leg_raise_posture,
#         "Mountain Climbers": check_mountain_climber_posture,
#     }

#     return checks.get(
#         exercise,
#         lambda _: {"fault": "Unknown exercise", "risk": 0}
#     )(lm)


# # -----------------------------
# # Suggestions
# # -----------------------------
# def get_suggestions(fault):
#     return {
#         "Good posture": ["Maintain current form"],
#         "Hips sagging": ["Engage core", "Keep body aligned"],
#         "Incomplete pushup": ["Lower chest more", "Control movement"],
#     }.get(fault, ["Perform controlled movements"])


# # -----------------------------
# # ✅ SINGLE ENTRY POINT
# # -----------------------------
# # def analyze_exercise_video(video_path, exercise_name):
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
#         for chunk in video_file.chunks():
#             tmp.write(chunk)
#         video_path = tmp.name

#     cap = cv2.VideoCapture(video_path)
#     pose = mp_pose.Pose()

#     total_frames = 0
#     improper_frames = 0
#     fault_counter = {}

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         total_frames += 1
#         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = pose.process(image)

#         if results.pose_landmarks:
#             lm = results.pose_landmarks.landmark
#             result = evaluate_posture(exercise_name, lm)

#             if result["risk"] > 40:
#                 improper_frames += 1
#                 fault_counter[result["fault"]] = fault_counter.get(result["fault"], 0) + 1

#     cap.release()
#     pose.close()
#     os.remove(video_path)

#     if total_frames == 0:
#         return {
#             "exercise": exercise_name,
#             "risk_percent": 0,
#             "fault": "No pose detected",
#             "suggestions": ["Ensure full body is visible"]
#         }

#     risk_percent = int((improper_frames / total_frames) * 100)
#     final_fault = max(fault_counter, key=fault_counter.get) if fault_counter else "Good posture"

#     return {
#         "exercise": exercise_name,
#         "risk_percent": risk_percent,
#         "fault": final_fault,
#         "suggestions": get_suggestions(final_fault),
#         "status": "analysis complete"
#     }

# def calculate_movement(prev_lm, curr_lm, indices):
#     movement = 0
#     for idx in indices:
#         movement += abs(curr_lm[idx].y - prev_lm[idx].y)
#     return movement

# def calculate_movement(prev_lm, curr_lm, indices):
#     movement = 0.0
#     for i in indices:
#         dx = curr_lm[i].x - prev_lm[i].x
#         dy = curr_lm[i].y - prev_lm[i].y
#         movement += (dx**2 + dy**2) ** 0.5
#     return movement

# MOTION_THRESHOLDS = {
#     "Jumping Squats": 0.015,
#     "Lunges": 0.012,
#     "Pushups": 0.008,
#     "Bridges": 0.006,
#     "Leg Raises": 0.005,
#     "Mountain Climbers": 0.02,
# }

# def detect_rep(exercise, lm, rep_state):
#     """
#     Returns:
#     - new_rep_state
#     - rep_completed (True / False)
#     """

#     # -------------------------------
#     # 1️⃣ Jumping Squats
#     # -------------------------------
#     if exercise == "Jumping Squats":
#         hip = [lm[23].x, lm[23].y]
#         knee = [lm[25].x, lm[25].y]
#         ankle = [lm[27].x, lm[27].y]

#         knee_angle = calculate_angle(hip, knee, ankle)

#         if knee_angle < 90 and rep_state == "up":
#             return "down", False
#         elif knee_angle > 160 and rep_state == "down":
#             return "up", True

#     # -------------------------------
#     # 2️⃣ Lunges
#     # -------------------------------
#     elif exercise == "Lunges":
#         hip = [lm[23].x, lm[23].y]
#         knee = [lm[25].x, lm[25].y]
#         ankle = [lm[27].x, lm[27].y]

#         knee_angle = calculate_angle(hip, knee, ankle)

#         if knee_angle < 95 and rep_state == "up":
#             return "down", False
#         elif knee_angle > 165 and rep_state == "down":
#             return "up", True

#     # -------------------------------
#     # 3️⃣ Pushups
#     # -------------------------------
#     elif exercise == "Pushups":
#         shoulder = [lm[11].x, lm[11].y]
#         elbow = [lm[13].x, lm[13].y]
#         wrist = [lm[15].x, lm[15].y]

#         elbow_angle = calculate_angle(shoulder, elbow, wrist)

#         if elbow_angle < 90 and rep_state == "up":
#             return "down", False
#         elif elbow_angle > 160 and rep_state == "down":
#             return "up", True

#     # -------------------------------
#     # 4️⃣ Bridges
#     # -------------------------------
#     elif exercise == "Bridges":
#         shoulder = [lm[11].x, lm[11].y]
#         hip = [lm[23].x, lm[23].y]
#         knee = [lm[25].x, lm[25].y]

#         hip_angle = calculate_angle(shoulder, hip, knee)

#         if hip_angle < 150 and rep_state == "up":
#             return "down", False
#         elif hip_angle > 170 and rep_state == "down":
#             return "up", True

#     # -------------------------------
#     # 5️⃣ Leg Raises
#     # -------------------------------
#     elif exercise == "Leg Raises":
#         hip = [lm[23].x, lm[23].y]
#         knee = [lm[25].x, lm[25].y]
#         ankle = [lm[27].x, lm[27].y]

#         leg_angle = calculate_angle(hip, knee, ankle)

#         if leg_angle < 120 and rep_state == "down":
#             return "up", True
#         elif leg_angle > 160 and rep_state == "up":
#             return "down", False

#     # -------------------------------
#     # 6️⃣ Mountain Climbers
#     # -------------------------------
#     elif exercise == "Mountain Climbers":
#         hip = [lm[23].x, lm[23].y]
#         knee = [lm[25].x, lm[25].y]

#         knee_lift = abs(knee[1] - hip[1])  # vertical knee movement

#         if knee_lift > 0.12 and rep_state == "down":
#             return "up", True
#         elif knee_lift < 0.08 and rep_state == "up":
#             return "down", False

#     return rep_state, False

# def body_is_horizontal(lm):
#     shoulder_y = lm[11].y
#     hip_y = lm[23].y
#     return abs(shoulder_y - hip_y) < 0.15

# def analyze_video(video_path, exercise_name):
#     cap = cv2.VideoCapture(video_path)
#     pose = mp_pose.Pose()

#     total_frames = 0
#     motion_frames = 0
#     improper_frames = 0
#     fault_counter = {}

#     prev_landmarks = None

#     # -------- CONFIGURATION --------
#     MIN_MOTION_RATIO = 0.25
#     INVALID_EX_THRESHOLD = 0.35

#     motion_indices = [11, 13, 15, 23, 25, 27]

#     exercise_match_frames = 0
#     valid_pose_frames = 0

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         total_frames += 1
#         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = pose.process(image)

#         if not results.pose_landmarks:
#             continue

#         lm = results.pose_landmarks.landmark
#         valid_pose_frames += 1

#         # -------- MOTION DETECTION --------
#         if prev_landmarks:
#             movement = calculate_movement(prev_landmarks, lm, motion_indices)
#             threshold = MOTION_THRESHOLDS.get(exercise_name, 0.01)
#             if movement > threshold:
#                 motion_frames += 1

#         prev_landmarks = lm

#         # -------- EXERCISE VALIDATION --------
#         if exercise_name == "Squats":
#             angle = calculate_angle(
#                 [lm[23].x, lm[23].y],
#                 [lm[25].x, lm[25].y],
#                 [lm[27].x, lm[27].y]
#             )
#             if angle < 120:
#                 exercise_match_frames += 1

#         elif exercise_name == "Lunges":
#             hip_y = lm[23].y
#             knee_y = lm[25].y
#             if knee_y > hip_y:
#                 exercise_match_frames += 1

#         elif exercise_name == "Pushups":
#             elbow_angle = calculate_angle(
#                 [lm[11].x, lm[11].y],
#                 [lm[13].x, lm[13].y],
#                 [lm[15].x, lm[15].y]
#             )
#             if elbow_angle < 110 and body_is_horizontal(lm):
#                 exercise_match_frames += 1

#         elif exercise_name == "Bridges":
#             angle = calculate_angle(
#                 [lm[11].x, lm[11].y],
#                 [lm[23].x, lm[23].y],
#                 [lm[25].x, lm[25].y]
#             )
#             if angle > 150:
#                 exercise_match_frames += 1

#         elif exercise_name == "Leg Raises":
#             angle = calculate_angle(
#                 [lm[23].x, lm[23].y],
#                 [lm[25].x, lm[25].y],
#                 [lm[27].x, lm[27].y]
#             )
#             if angle > 160:
#                 exercise_match_frames += 1

#         elif exercise_name == "Mountain Climbers":
#             angle = calculate_angle(
#                 [lm[11].x, lm[11].y],
#                 [lm[23].x, lm[23].y],
#                 [lm[27].x, lm[27].y]
#             )
#             if 150 < angle < 185:
#                 exercise_match_frames += 1

#         # -------- POSTURE ANALYSIS --------
#         result = evaluate_posture(exercise_name, lm)
#         if result["risk"] > 40:
#             improper_frames += 1
#             fault_counter[result["fault"]] = fault_counter.get(result["fault"], 0) + 1

#     cap.release()
#     pose.close()

#     if os.path.exists(video_path):
#         os.remove(video_path)

#     # -------- NO PERSON --------
#     if valid_pose_frames == 0:
#         return {
#             "status": "no_pose",
#             "message": "No person detected in the video",
#         }

#     # -------- NO EXERCISE --------
#     if motion_frames < total_frames * MIN_MOTION_RATIO:
#         return {
#             "status": "exercise_not_detected",
#             "message": "No exercise movement detected",
#         }

#     # -------- INVALID EXERCISE --------
#     if exercise_match_frames < valid_pose_frames * INVALID_EX_THRESHOLD:
#         return {
#             "status": "invalid_exercise",
#             "message": "Uploaded video does not match the selected exercise",
#         }

#     # -------- FINAL ANALYSIS --------
#     risk_percent = int((improper_frames / total_frames) * 100)
#     final_fault = max(fault_counter, key=fault_counter.get) if fault_counter else "Good posture"
#     confidence = max(0, 100 - risk_percent)

#     return {
#         "exercise": exercise_name,
#         "status": "analysis_complete",
#         "risk_percent": risk_percent,
#         "fault": final_fault,
#         "suggestions": get_suggestions(final_fault),
#         "confidence": confidence
#     }

import cv2
import mediapipe as mp
import numpy as np
import tempfile
import math
import os

mp_pose = mp.solutions.pose


# -----------------------------
# Utility: Angle calculation
# -----------------------------
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
              np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle


# -----------------------------
# Posture checks (6 exercises)
# -----------------------------
def check_squat_posture(lm):
    hip = [lm[23].x, lm[23].y]
    knee = [lm[25].x, lm[25].y]
    ankle = [lm[27].x, lm[27].y]

    angle = calculate_angle(hip, knee, ankle)

    if angle < 70:
        return {"fault": "Squat too deep", "risk": 65}
    elif angle > 160:
        return {"fault": "Insufficient squat depth", "risk": 55}
    return {"fault": "Good posture", "risk": 25}


def check_lunge_posture(lm):
    hip = [lm[23].x, lm[23].y]
    knee = [lm[25].x, lm[25].y]
    ankle = [lm[27].x, lm[27].y]

    angle = calculate_angle(hip, knee, ankle)

    if angle < 75:
        return {"fault": "Knee bending too much", "risk": 60}
    elif angle > 160:
        return {"fault": "Shallow lunge", "risk": 50}
    return {"fault": "Good posture", "risk": 25}


def check_pushup_posture(lm):
    shoulder = [lm[11].x, lm[11].y]
    elbow = [lm[13].x, lm[13].y]
    wrist = [lm[15].x, lm[15].y]

    angle = calculate_angle(shoulder, elbow, wrist)

    if angle < 40:
        return {"fault": "Elbow over-bending", "risk": 70}
    elif angle > 170:
        return {"fault": "Incomplete pushup", "risk": 55}
    return {"fault": "Good posture", "risk": 30}


def check_bridge_posture(lm):
    shoulder = [lm[11].x, lm[11].y]
    hip = [lm[23].x, lm[23].y]
    knee = [lm[25].x, lm[25].y]

    angle = calculate_angle(shoulder, hip, knee)

    if angle < 150:
        return {"fault": "Hips not lifted enough", "risk": 60}
    elif angle > 185:
        return {"fault": "Lower back overextension", "risk": 70}
    return {"fault": "Good posture", "risk": 25}


def check_leg_raise_posture(lm):
    hip = [lm[23].x, lm[23].y]
    knee = [lm[25].x, lm[25].y]
    ankle = [lm[27].x, lm[27].y]

    angle = calculate_angle(hip, knee, ankle)

    if angle < 160:
        return {"fault": "Knees bending during leg raise", "risk": 55}
    return {"fault": "Good posture", "risk": 25}


def check_mountain_climber_posture(lm):
    shoulder = [lm[11].x, lm[11].y]
    hip = [lm[23].x, lm[23].y]
    ankle = [lm[27].x, lm[27].y]

    angle = calculate_angle(shoulder, hip, ankle)

    if angle < 150:
        return {"fault": "Hips sagging", "risk": 65}
    elif angle > 185:
        return {"fault": "Hips too high", "risk": 60}
    return {"fault": "Good posture", "risk": 30}


# -----------------------------
# Posture evaluator
# -----------------------------
def evaluate_posture(exercise, lm):
    checks = {
        "Squats": check_squat_posture,
        "Lunges": check_lunge_posture,
        "Pushups": check_pushup_posture,
        "Bridges": check_bridge_posture,
        "Leg Raises": check_leg_raise_posture,
        "Mountain Climbers": check_mountain_climber_posture,
    }

    return checks.get(
        exercise,
        lambda _: {"fault": "Unknown exercise", "risk": 0}
    )(lm)


# -----------------------------
# Suggestions
# -----------------------------
def get_suggestions(fault):
    return {
        "Good posture": ["Maintain current form"],
        "Hips sagging": ["Engage core", "Keep body aligned"],
        "Incomplete pushup": ["Lower chest more", "Control movement"],
    }.get(fault, ["Perform controlled movements"])


# -----------------------------
# ✅ SINGLE ENTRY POINT
# -----------------------------
# def analyze_exercise_video(video_path, exercise_name):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        for chunk in video_file.chunks():
            tmp.write(chunk)
        video_path = tmp.name

    cap = cv2.VideoCapture(video_path)
    pose = mp_pose.Pose()

    total_frames = 0
    improper_frames = 0
    fault_counter = {}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        total_frames += 1
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            result = evaluate_posture(exercise_name, lm)

            if result["risk"] > 40:
                improper_frames += 1
                fault_counter[result["fault"]] = fault_counter.get(result["fault"], 0) + 1

    cap.release()
    pose.close()
    os.remove(video_path)

    if total_frames == 0:
        return {
            "exercise": exercise_name,
            "risk_percent": 0,
            "fault": "No pose detected",
            "suggestions": ["Ensure full body is visible"]
        }

    risk_percent = int((improper_frames / total_frames) * 100)
    final_fault = max(fault_counter, key=fault_counter.get) if fault_counter else "Good posture"

    return {
        "exercise": exercise_name,
        "risk_percent": risk_percent,
        "fault": final_fault,
        "suggestions": get_suggestions(final_fault),
        "status": "analysis complete"
    }

def calculate_movement(prev_lm, curr_lm, indices):
    movement = 0
    for idx in indices:
        movement += abs(curr_lm[idx].y - prev_lm[idx].y)
    return movement

def calculate_movement(prev_lm, curr_lm, indices):
    movement = 0.0
    for i in indices:
        dx = curr_lm[i].x - prev_lm[i].x
        dy = curr_lm[i].y - prev_lm[i].y
        movement += (dx**2 + dy**2) ** 0.5
    return movement

MOTION_THRESHOLDS = {
    "Squats": 0.015,
    "Lunges": 0.012,
    "Pushups": 0.008,
    "Bridges": 0.006,
    "Leg Raises": 0.005,
    "Mountain Climbers": 0.02,
}

def detect_rep(exercise, lm, rep_state):
    """
    Returns:
    - new_rep_state
    - rep_completed (True / False)
    """

    # -------------------------------
    # 1️⃣ Squats
    # -------------------------------
    if exercise == "Squats":
        hip = [lm[23].x, lm[23].y]
        knee = [lm[25].x, lm[25].y]
        ankle = [lm[27].x, lm[27].y]

        knee_angle = calculate_angle(hip, knee, ankle)

        if knee_angle < 90 and rep_state == "up":
            return "down", False
        elif knee_angle > 160 and rep_state == "down":
            return "up", True

    # -------------------------------
    # 2️⃣ Lunges
    # -------------------------------
    elif exercise == "Lunges":
        hip = [lm[23].x, lm[23].y]
        knee = [lm[25].x, lm[25].y]
        ankle = [lm[27].x, lm[27].y]

        knee_angle = calculate_angle(hip, knee, ankle)

        if knee_angle < 95 and rep_state == "up":
            return "down", False
        elif knee_angle > 165 and rep_state == "down":
            return "up", True

    # -------------------------------
    # 3️⃣ Pushups
    # -------------------------------
    elif exercise == "Pushups":
        shoulder = [lm[11].x, lm[11].y]
        elbow = [lm[13].x, lm[13].y]
        wrist = [lm[15].x, lm[15].y]

        elbow_angle = calculate_angle(shoulder, elbow, wrist)

        if elbow_angle < 90 and rep_state == "up":
            return "down", False
        elif elbow_angle > 160 and rep_state == "down":
            return "up", True

    # -------------------------------
    # 4️⃣ Bridges
    # -------------------------------
    elif exercise == "Bridges":
        shoulder = [lm[11].x, lm[11].y]
        hip = [lm[23].x, lm[23].y]
        knee = [lm[25].x, lm[25].y]

        hip_angle = calculate_angle(shoulder, hip, knee)

        if hip_angle < 150 and rep_state == "up":
            return "down", False
        elif hip_angle > 170 and rep_state == "down":
            return "up", True

    # -------------------------------
    # 5️⃣ Leg Raises
    # -------------------------------
    elif exercise == "Leg Raises":
        hip = [lm[23].x, lm[23].y]
        knee = [lm[25].x, lm[25].y]
        ankle = [lm[27].x, lm[27].y]

        leg_angle = calculate_angle(hip, knee, ankle)

        if leg_angle < 120 and rep_state == "down":
            return "up", True
        elif leg_angle > 160 and rep_state == "up":
            return "down", False

    # -------------------------------
    # 6️⃣ Mountain Climbers
    # -------------------------------
    elif exercise == "Mountain Climbers":
        hip = [lm[23].x, lm[23].y]
        knee = [lm[25].x, lm[25].y]

        knee_lift = abs(knee[1] - hip[1])  # vertical knee movement

        if knee_lift > 0.12 and rep_state == "down":
            return "up", True
        elif knee_lift < 0.08 and rep_state == "up":
            return "down", False

    return rep_state, False


def analyze_video(video_path, exercise_name):
    cap = cv2.VideoCapture(video_path)
    pose = mp_pose.Pose()

    total_frames = 0
    motion_frames = 0
    improper_frames = 0
    fault_counter = {}

    prev_landmarks = None

    # -------- CONFIGURATION --------
    MIN_MOTION_RATIO = 0.25          # Problem 1 fix
    INVALID_EX_THRESHOLD = 0.15      # Problem 2 fix

    motion_indices = [11, 13, 15, 23, 25, 27]

    # Exercise-specific validation counters
    exercise_match_frames = 0
    valid_pose_frames = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        total_frames += 1
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        if not results.pose_landmarks:
            continue

        lm = results.pose_landmarks.landmark
        valid_pose_frames += 1

        # -------- MOTION DETECTION --------
        if prev_landmarks:
            movement = calculate_movement(prev_landmarks, lm, motion_indices)
            threshold = MOTION_THRESHOLDS.get(exercise_name, 0.01)
            if movement > threshold:
                motion_frames += 1

        prev_landmarks = lm

        # -------- EXERCISE VALIDATION (Problem 2) --------
        if exercise_name == "Squats":
            angle = calculate_angle(
                [lm[23].x, lm[23].y],
                [lm[25].x, lm[25].y],
                [lm[27].x, lm[27].y]
            )
            if angle < 120:
                exercise_match_frames += 1

        elif exercise_name == "Lunges":
            angle = calculate_angle(
                [lm[23].x, lm[23].y],
                [lm[25].x, lm[25].y],
                [lm[27].x, lm[27].y]
            )
            if 70 < angle < 150:
                exercise_match_frames += 1

        elif exercise_name == "Pushups":
            angle = calculate_angle(
                [lm[11].x, lm[11].y],
                [lm[13].x, lm[13].y],
                [lm[15].x, lm[15].y]
            )
            if angle < 110:
                exercise_match_frames += 1

        elif exercise_name == "Bridges":
            angle = calculate_angle(
                [lm[11].x, lm[11].y],
                [lm[23].x, lm[23].y],
                [lm[25].x, lm[25].y]
            )
            if angle > 150:
                exercise_match_frames += 1

        elif exercise_name == "Leg Raises":
            angle = calculate_angle(
                [lm[23].x, lm[23].y],
                [lm[25].x, lm[25].y],
                [lm[27].x, lm[27].y]
            )
            if angle > 160:
                exercise_match_frames += 1

        elif exercise_name == "Mountain Climbers":
            angle = calculate_angle(
                [lm[11].x, lm[11].y],
                [lm[23].x, lm[23].y],
                [lm[27].x, lm[27].y]
            )
            if 150 < angle < 185:
                exercise_match_frames += 1

        # -------- POSTURE ANALYSIS --------
        result = evaluate_posture(exercise_name, lm)
        if result["risk"] > 40:
            improper_frames += 1
            fault_counter[result["fault"]] = fault_counter.get(result["fault"], 0) + 1

    cap.release()
    pose.close()

    if os.path.exists(video_path):
        os.remove(video_path)

    # -------- NO PERSON --------
    if valid_pose_frames == 0:
        return {
            "exercise": exercise_name,
            "status": "no_pose",
            "message": "No person detected in the video",
            "risk_percent": 0,
            "confidence": 0
        }

    # -------- PROBLEM 1 FIX: NO EXERCISE --------
    if motion_frames < total_frames * MIN_MOTION_RATIO:
        return {
            "exercise": exercise_name,
            "status": "exercise_not_detected",
            "message": "No exercise movement detected",
            "risk_percent": 0,
            "confidence": 0
        }

    # -------- PROBLEM 2 FIX: INVALID EXERCISE --------
    if exercise_match_frames < valid_pose_frames * INVALID_EX_THRESHOLD:
        return {
            "exercise": exercise_name,
            "status": "invalid_exercise",
            "message": "Uploaded video does not match the selected exercise",
            "risk_percent": 0,
            "confidence": 0
        }

    # -------- FINAL ANALYSIS --------
    risk_percent = int((improper_frames / total_frames) * 100)
    final_fault = max(fault_counter, key=fault_counter.get) if fault_counter else "Good posture"

    confidence = max(0, 100 - risk_percent)

    return {
        "exercise": exercise_name,
        "status": "analysis_complete",
        "risk_percent": risk_percent,
        "fault": final_fault,
        "suggestions": get_suggestions(final_fault),
        "confidence": confidence
    }