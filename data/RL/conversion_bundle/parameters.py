
import numpy as np
"""
Configuration parameters for the FMU-based reinforcement learning environment.

This module defines the parameters required for running simulations with a Functional Mock-up Unit (FMU)
for building energy management, specifically for controlling shading devices in a residential flat.

Attributes:
    parameter (dict): Dictionary containing all configuration parameters.
        seed (int): Random seed for reproducibility.
        store_data (bool): Flag to enable/disable data storage.
        fmu_step_size (float): Simulation step size in seconds (600 seconds = 10 minutes).
        fmu_path (str): Path to the FMU file for the building model.
        fmu_start_time (float): Simulation start time in seconds (0 days).
        fmu_warmup_time (float): Warmup period in seconds (3 days) before active learning.
        fmu_final_time (float): Total simulation duration in seconds (365 days).
        action_names (list): Names of controllable shading actuators across different zones and windows.
        action_min (np.ndarray): Minimum values for each shading action (0 = fully open).
        action_max (np.ndarray): Maximum values for each shading action (7 = fully closed).
        observation_names (list): Names of observable state variables including indoor temperatures,
            outdoor temperature, and direct normal irradiance.
        reward_names (list): Names of reward components related to energy consumption
            (electricity, district heating, and district cooling).
    
    dtype (type): NumPy data type for numerical calculations (float64).
"""

parameter = {}
parameter['seed']       = 1
parameter['store_data'] = True

dtype = np.float64
parameter['fmu_step_size']   = 3600 / 6
parameter['fmu_path']        = 'shading_edited_Res_Flat2_IDF_optimized_final.fmu'
parameter['fmu_start_time']  = 0 * 60 * 60 * 24
parameter['fmu_warmup_time'] = 3 * 60 * 60 * 24
parameter['fmu_final_time']  = 365 * 60 * 60 * 24

parameter['action_names']      = ['A_Shade_Stair_Z1_W2', 'A_Shade_Stair_Z1_W3', 'A_Shade_Stair_Z1_W4', 'A_Shade_Flat2_Z1_W2', 'A_Shade_Flat2_Z1_W8', 'A_Shade_Flat2_Z1_W9', 'A_Shade_Flat2_Z2_W2', 'A_Shade_Flat2_Z2_W3', 'A_Shade_Flat2_Z4_W2']
parameter['action_min']        = np.array(['0', '0', '0', '0', '0', '0', '0', '0', '0'], dtype=np.float64)
parameter['action_max']        = np.array(['7', '7', '7', '7', '7', '7', '7', '7', '7'], dtype=np.float64)
parameter['observation_names'] = ['Tin_Flat2_Zona1', 'Tout', 'DNI', 'Tin_Flat2_Zona2', 'Tin_Flat2_Zona3', 'Tin_Flat2_Zona4']
parameter['reward_names']      = ['Electricity', 'DistrictHeating', 'DistrictCooling']

