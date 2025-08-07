#!/bin/bash

tmux new-session -d -s esp32

tmux split-window -v -t esp32

tmux select-pane -t esp32:0.0

tmux split-window -h

tmux send-keys -t esp32:0.0 'screen /dev/ttyUSB0 115200' C-m

tmux send-keys -t esp32:0.1 'screen /dev/ttyUSB1 115200' C-m

tmux select-pane -t esp32:0.2

tmux set -g mouse on

tmux attach -t esp32
