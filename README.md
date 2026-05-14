# AI-Powered Rotoscoping Tool

## Problem
Manual rotoscoping in VFX production takes hours per shot.
This tool automates background removal using AI in seconds.

## What it does
- Takes any image or photo as input
- Automatically removes background using AI
- Outputs clean PNG with transparent background
- Ready for compositing in Nuke, After Effects, or DaVinci Resolve

## Tech Stack
- Python
- rembg (AI background removal)
- OpenCV
- PIL / Pillow

## How to Run
pip install rembg pillow
python main.py

## Results
Input images go in /input folder
Output PNGs (with transparency) appear in /output folder

## About
Built by a VFX compositor with 10 years experience,
exploring AI-powered pipeline automation for VFX workflows.