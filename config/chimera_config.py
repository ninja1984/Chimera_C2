#!/usr/bin/env python3
import os

def get_c2_host():
    return os.getenv("C2_HOST", "127.0.0.1")

def get_c2_port():
    return int(os.getenv("C2_PORT", "9999"))

def get_callback_host():
    return os.getenv("CALLBACK_HOST", "146.115.17.147")

def get_callback_port():
    return int(os.getenv("CALLBACK_PORT", "4444"))

def get_gpu_ip():
    return os.getenv("GPU_IP", "146.115.17.147")

def get_lab_password():
    """Returns the lab/test password from environment variables"""
    return os.getenv("LAB_PASSWORD", "change_me_in_.env")
