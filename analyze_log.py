import pandas as pd
import numpy as np

df = pd.read_csv('logs/pid_tuning_1783931892.csv')
tracking_df = df[df['state'] == 'TRACKING'].copy()

if len(tracking_df) == 0:
    print("No TRACKING state found in the log.")
else:
    print(f"Tracking Data points: {len(tracking_df)}")
    print(f"Time tracked: {tracking_df['timestamp'].iloc[-1] - tracking_df['timestamp'].iloc[0]:.2f} s")
    
    # Error statistics
    print("\n--- X-Axis (Yaw) Error Stats ---")
    print(f"Mean Abs Error: {tracking_df['err_x'].abs().mean():.2f} px")
    print(f"Max Abs Error: {tracking_df['err_x'].abs().max():.2f} px")
    print(f"Std Dev Error: {tracking_df['err_x'].std():.2f} px")
    
    print("\n--- Altitude Error Stats ---")
    print(f"Mean Abs Error: {tracking_df['err_alt'].abs().mean():.2f} m")
    print(f"Max Abs Error: {tracking_df['err_alt'].abs().max():.2f} m")
    print(f"Std Dev Error: {tracking_df['err_alt'].std():.2f} m")

    # Command statistics
    print("\n--- Yaw Command Stats ---")
    print(f"Mean Abs Cmd: {tracking_df['cmd_yaw'].abs().mean():.2f} deg/s")
    print(f"Max Abs Cmd: {tracking_df['cmd_yaw'].abs().max():.2f} deg/s")

    print("\n--- Alt Command Stats ---")
    print(f"Mean Abs Cmd: {tracking_df['cmd_alt'].abs().mean():.2f} m/s")
    print(f"Max Abs Cmd: {tracking_df['cmd_alt'].abs().max():.2f} m/s")

