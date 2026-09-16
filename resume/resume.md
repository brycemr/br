---
name: Bryce Richard
tagline: Machine Learning Engineer — Computer Vision, 3D Geometry, Perception Systems
location: Denver, CO
email: brycerichard26@gmail.com
phone: (385) 233-7360
portfolio: brycemr.github.io/br
github: github.com/brycemr
---

## Summary

Computer vision engineer building perception systems that run outdoors, on real hardware,
at production scale — multi-view geometry, calibration, tracking and re-identification,
and the services behind them. Mechanical engineering background, so the optics and the
geometry come before the model.

## Experience

### Blissway — Machine Learning Engineer
Denver, CO · June 2025 – Present

Founding member of the ML team at a Y Combinator-backed company replacing roadside
tolling and safety hardware with vision. Own perception end to end: data collection
and labeling strategy, model training, evaluation infrastructure, and the production
services. Models run in the cloud and on NPUs mounted to poles on live interstates.

- Built the **vision-based vehicle triggering system** that replaces in-road induction
  loops: detection on a Hailo NPU feeding a multi-frame tracker that maintains vehicle
  identity across frames and decides when a vehicle has been fully captured. **0.10%
  unrecoverable miss rate at 4.9% false-positive inflation**.
- Built **projective-geometry lane registration** that keeps each camera's stored lane
  model aligned as poles shake and cameras drift — vanishing-point and anchor
  optimization against segmented lane markings. Recovered lane coverage from **0% to
  76%** on a drifted corridor; tracked camera motion to **1–3 px through 3° of
  rotation at ~15 ms/frame on CPU**, validated on real roadside footage.
- Built **axle counting as a multi-view fusion problem**: per-frame wheel detections
  from several cameras projected into a single virtual chassis per vehicle trip, with
  RANSAC outlier rejection and density clustering over the fused representation.
  **100% precision / 99.4% recall** on the billing-critical 3+ axle call, with ~1% of
  trips routed to human review.
- Wrote an **analytic camera-placement simulator** — pinhole projection plus multi-stage
  Nelder-Mead over aim, zoom and illumination — that answers roadside siting questions
  without a field trip, with its detection model calibrated against recorded field data to
  **reproduce measured recall within 5 pp** on replayed clips.
- Fine-tuned a **DINOv3 vehicle re-identification backbone** for cross-camera matching
  and vehicle fingerprinting, raising ReID mAP from **0.69 to 0.92** in a multi-task
  co-train while cutting backbone FLOPs **3.3×**.
- Trained a custom **multi-head license plate reader** (segmentation → rectification →
  OCR, state and design heads) that beats the commercial ALPR incumbent by **7.7 pp on
  plate text** (93.8% vs 86.1%) and **8.4 pp on state** (97.5% vs 89.1%).
- Re-architected the inference pipeline into **per-service microservices** with metered cost
  attribution, and swapped the segmentation tier to RF-DETR for **2.4× cheaper serving at
  equal accuracy** across ~3M events (~7M images) per day.

### Carnegie Mellon University, Biorobotics Lab — Graduate Research Assistant
Pittsburgh, PA · August 2023 – May 2025

- Designed and implemented a **real-time sortation system for a robotic disassembly
  cell** in collaboration with a major OEM, training and fine-tuning YOLOv8, U-Net and
  Mask R-CNN for semantic and instance segmentation of components on a moving line.
- Integrated a **SCARA arm with vision-in-the-loop decision-making over ROS**, closing the
  loop from detection to pick on live hardware, and built a **Segment Anything–based
  annotation tool** that cut labeling time **50%**.
- Prototyped a tool to infer **forces and internal stresses in a smart device from
  high-speed X-ray video**, connecting image-space measurement to physical models.

### Brigham Young University, FLOW Lab — Research Assistant
Provo, UT · August 2022 – May 2023

- Developed layout optimization tools integrating bathymetry data for offshore wind
  farms, **reducing projected LCOE by 10%**.

## Education

### Carnegie Mellon University — M.S. Mechanical Engineering (Research)
Pittsburgh, PA · May 2025 · QPA 3.9 / 4.0

Advanced Computer Vision · Intermediate Deep Learning · Trustworthy AI · Systems &
Toolchains for AI Engineers

### Brigham Young University — B.S. Mechanical Engineering, Minor in Computer Science
Provo, UT · April 2023 · GPA 3.9 / 4.0

## Skills

**Languages** — Python (advanced), C++

**Perception & 3D** — projective geometry, camera calibration and registration,
multi-view and temporal fusion, tracking, re-identification and metric learning,
semantic and instance segmentation, OCR; PyTorch, OpenCV, ROS, DINOv3 / ViT, YOLO,
RF-DETR, SegFormer, SAM

**Systems & Deployment** — edge inference on Hailo NPUs, ONNX, Docker, FastAPI, Modal,
AWS, MongoDB, PostgreSQL, CI/CD, evaluation and monitoring infrastructure, SolidWorks
