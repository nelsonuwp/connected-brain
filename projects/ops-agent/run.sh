#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

ssh -N -L 5433:localhost:5432 anelson@toolsdbtor01.corp.peer1.net &
TUNNEL_PID=$!
trap "kill $TUNNEL_PID 2>/dev/null" EXIT

sleep 1  # give tunnel a moment to establish

python3 -m ops_agent.main
