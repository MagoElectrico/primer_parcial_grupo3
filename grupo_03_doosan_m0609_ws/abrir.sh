#!/usr/bin/env bash
set -eo pipefail
WS="$HOME/grupo_03_doosan_m0609_ws"
if [ ! -f "$WS/entorno.sh" ] || [ ! -f "$WS/install/setup.bash" ]; then
  echo "ERROR: el workspace no está instalado. Ejecuta primero ./instalar.sh"
  exit 1
fi
source "$WS/entorno.sh"
ros2 launch grupo03_doosan_m0609_bringup display.launch.py
