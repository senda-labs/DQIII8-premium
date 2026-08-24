#!/usr/bin/env bash
# install_ollama_tunnel.sh — one-shot installer for the Hostinger -> Netcup
# Ollama SSH tunnel (2026-08-24 migration). Run as root on Hostinger.
# Exists so the operator only has to paste one short command instead of
# several long ones that some terminals mangle on paste (line-wrap becomes
# real newlines, splitting a long `cp`/`systemctl` line mid-word).
set -euo pipefail

SRC="/root/dqiii8/infrastructure/systemd/dqiii8-ollama-tunnel.service"
DST="/etc/systemd/system/dqiii8-ollama-tunnel.service"

echo "[1/5] copying unit file..."
cp "$SRC" "$DST"

echo "[2/5] stopping + disabling local ollama.service..."
systemctl disable --now ollama

echo "[3/5] daemon-reload..."
systemctl daemon-reload

echo "[4/5] enabling + starting dqiii8-ollama-tunnel..."
systemctl enable --now dqiii8-ollama-tunnel

echo "[5/5] status:"
sleep 2
systemctl is-active dqiii8-ollama-tunnel
echo "--- ollama list via tunnel ---"
ollama list
