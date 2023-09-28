#!/bin/bash

while true; do
  # Run the Python script in the background
  python create_data.py &

  # Get the process ID (PID) of the Python script
  python_pid=$!

  # Sleep for 2 minutes
  sleep 120

  # Terminate the Python script using its PID
  kill -9 $python_pid

  echo "Python script terminated. Waiting for the next iteration..."
  sleep 120
done
