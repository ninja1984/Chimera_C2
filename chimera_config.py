#!/usr/bin/env python3
import os

def get_c2_host():
    return os.getenv("C2_HOST", "127.0.0.1")

def get_c2_port():
    return int(os.getenv("C2_PORT", "9999"))

def get_callback_host():
    return os.getenv("CALLBACK_HOST", "10.0.2.15")

def get_callback_port():
    return int(os.getenv("CALLBACK_PORT", "4444"))

def get_gpu_ip():
    return os.getenv("GPU_IP", "127.0.0.1")
