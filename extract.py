#!/bin/bash

# ==========================================
# CONFIGURATION: Insert your coordinates here
# ==========================================

# 1st Action: Initial Tap
TAP1_X="938"
TAP1_Y="1172"

# 2nd Action: Tap during the recording
TAP2_X="498"
TAP2_Y="2021"

# 3rd Action: Swipe after saving the recording
SWIPE_X1="531"
SWIPE_Y1="1489"
SWIPE_X2="595"
SWIPE_Y2="954"
SWIPE_DURATION="800" # Duration in milliseconds

# ==========================================

# Prompt the user for the number of iterations
loop_count=2

current_date=$(date +%Y-%m-%d)
echo "Starting automation for $loop_count iterations..."

# Main automation loop
for (( i=0; i<loop_count; i++ )); do
    echo "----------------------------------------"
    echo "Starting Iteration $i"

    # 1. First Tap
    echo "Action 1: Tapping at ($TAP1_X, $TAP1_Y)"
    adb shell input tap $TAP1_X $TAP1_Y
    
    # Optional: Short delay if your app takes a moment to load after the first tap
    sleep 1 

    # 2. Start scrcpy recording
    filename="recording_${current_date}_${i}.mp4"
    echo "Starting background recording: $filename"
    scrcpy --record "$filename" --no-display > /dev/null 2>&1 &
    scrcpy_pid=$!

    # Minimum 1 second delay to let scrcpy initialize (using 1.5 to be safe)
    sleep 1.5

    # 3. Second Tap
    echo "Action 2: Tapping at ($TAP2_X, $TAP2_Y)"
    adb shell input tap $TAP2_X $TAP2_Y
    
    # Wait briefly so the visual result of the tap is captured in the video before it stops
    sleep 210

    # 4. Stop recording and save
    echo "Stopping recording..."
    kill -INT $scrcpy_pid
    wait $scrcpy_pid 2>/dev/null
    echo "Saved: $filename"

    # 5. Swipe gesture
    echo "Action 3: Swiping from ($SWIPE_X1, $SWIPE_Y1) to ($SWIPE_X2, $SWIPE_Y2)"
    adb shell input swipe $SWIPE_X1 $SWIPE_Y1 $SWIPE_X2 $SWIPE_Y2 $SWIPE_DURATION
    
    # Short buffer before the loop restarts from Step 1
    sleep 1

done

echo "----------------------------------------"
echo "Automation process complete! $loop_count files have been saved."
