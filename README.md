# Small Soccer Robot

This repository contains the programming division code for the Small Soccer Robot project (Dagozilla ITB). It uses ROS 2 Jazzy Jalisco and Python (rclpy) to control a small wheeled soccer robot (20x20x20 cm) that can chase and kick a ball automatically.

## ROS 2 Workspace Structure

- `ros2_ws/` - Main ROS 2 workspace
    - `src/small_robot_control/` - Robot movement control (Python, rclpy)
    - `src/small_robot_vision/` - Ball detection using OpenCV
    - `src/small_robot_comm/` - Serial communication with ESP32
    - `src/small_robot_launch/` - Launch files for all nodes
- `docs/` - Documentation (architecture, flowchart)
- `.github/workflows/` - CI/CD with GitHub Actions

## Setup

1. Install ROS 2 Jazzy Jalisco (see [ROS 2 Docs](https://docs.ros.org/en/rolling/Installation.html))
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Build workspace:
   ```bash
   colcon build --symlink-install
   ```

## Testing

Run tests using pytest:
```bash
pytest
```

## License

MIT
