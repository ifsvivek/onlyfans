#!/bin/bash

exec gnome-terminal -- bash -c "
  cd ~/Documents/omen && \
  sudo bash -c 'python3 omen-fan.py e start'
"
