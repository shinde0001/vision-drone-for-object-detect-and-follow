#!/usr/bin/env bash
# ============================================================
# start_all.sh — Run both Simulation and Web Backend
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}╔══════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   🚀 Vision Drone — Full System Launcher    ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${YELLOW}[1/3] Cleaning up any existing instances...${NC}"
pkill -f "python3 web/server.py" 2>/dev/null || true
fuser -k 8080/tcp 2>/dev/null || true
fuser -k 5600/udp 2>/dev/null || true
fuser -k 14540/udp 2>/dev/null || true
pkill -x gazebo 2>/dev/null || true
pkill -x gzserver 2>/dev/null || true
pkill -x gzclient 2>/dev/null || true
pkill -x px4 2>/dev/null || true
pkill -x mavsdk_server 2>/dev/null || true
sleep 2

echo -e "${GREEN}[2/3] Starting Simulation (Gazebo + PX4)...${NC}"
bash ./launch_vision.sh &
VISION_PID=$!

# Give the simulator a head start to initialize its ports
echo -e "${YELLOW}Waiting for simulation to initialize...${NC}"
sleep 10

echo -e "${GREEN}[3/3] Starting FastAPI Web Server...${NC}"
# Source Gazebo/PX4 environments so Python's gz subprocess calls work
PX4_DIR="${HOME}/PX4-Autopilot"
BUILD_PATH="${PX4_DIR}/build/px4_sitl_default"
if [ -f "/usr/share/gazebo-11/setup.bash" ]; then
    source /usr/share/gazebo-11/setup.bash
fi
if [ -f "/opt/ros/humble/setup.bash" ]; then
    source /opt/ros/humble/setup.bash
fi
source "${PX4_DIR}/Tools/simulation/gazebo-classic/setup_gazebo.bash" "${PX4_DIR}" "${BUILD_PATH}" 2>/dev/null || true
export GAZEBO_MODEL_PATH="${SCRIPT_DIR}/gazebo/models:${GAZEBO_MODEL_PATH}"

python3 web/server.py &
SERVER_PID=$!

echo ""
echo -e "${CYAN}================================================${NC}"
echo -e "${GREEN}✅ All services started!${NC}"
echo -e "Dashboard will be available at: ${CYAN}http://localhost:8080/${NC}"
echo -e "Wait for PX4 to finish booting up before arming."
echo -e "${YELLOW}Press Ctrl+C to shut down everything.${NC}"
echo -e "${CYAN}================================================${NC}"
echo ""

cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down all processes...${NC}"
    kill $SERVER_PID 2>/dev/null || true
    kill -TERM $VISION_PID 2>/dev/null || true
    
    # Force kill just to be sure
    pkill -f "python3 web/server.py" 2>/dev/null || true
    fuser -k 8080/tcp 2>/dev/null || true
    pkill -x gazebo 2>/dev/null || true
    pkill -x gzserver 2>/dev/null || true
    pkill -x gzclient 2>/dev/null || true
    pkill -x px4 2>/dev/null || true
    pkill -x mavsdk_server 2>/dev/null || true
    
    echo -e "${GREEN}Done.${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

wait $SERVER_PID
wait $VISION_PID
