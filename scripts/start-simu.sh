#!/bin/bash

# Démarre la simulation complète dans tmux

SESSION=simu

cd ..

# Crée une nouvelle session détachée
tmux new-session -d -s $SESSION

# Panneau 0 : ports série virtuels
 tmux send-keys -t $SESSION:0.0 './simulation_pc/creer_ports_serie.sh' C-m

# Split vertical pour panneau 1 (émetteur)
tmux split-window -v -t $SESSION
 tmux send-keys -t $SESSION:0.1 'SIMULATION=True python3 source/programme_antenne_emission.py' C-m

# Split horizontal pour panneau 2 (récepteur)
tmux split-window -h
 tmux send-keys -t $SESSION:0.2 'SIMULATION=True python3 source/programme_antenne_reception.py' C-m

# Active la souris
tmux set -g mouse on

# Attache la session
tmux attach -t $SESSION
