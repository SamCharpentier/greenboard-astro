#!/bin/bash
OUT=/home/claude/greenboard-astro/public/video/products
SRC=/home/claude/samcharpentier/greenboard
enc() { ffmpeg -y -loglevel error -i "$SRC/$1" -an -vf "scale=960:-2:flags=lanczos,format=yuv420p" -c:v libx264 -preset slow -crf 27 -movflags +faststart "$OUT/$2.mp4"; }
enc "Greenboard-ProductPage-01-PeoplePermissions_v2.mp4" platform-1
enc "Greenboard-ProductPage-02-Books-Records_FULL_v2.mp4" platform-2
enc "Greenboard-ProductPage-03-Intergrations_v2.mp4" communications-archiving-supervision-1
enc "Greenboard-ProductPage-04-Capture_v2.mp4" communications-archiving-supervision-2
enc "Greenboard-ProductPage-06-Retain-Search_v2.mp4" communications-archiving-supervision-3
enc "Greenboard-ProductPage-07-Personal-Trading_v2.mp4" employee-compliance-1
enc "Greenboard-ProductPage-08-Best-In-Class_v2.mp4" employee-compliance-2
enc "Greenboard-ProductPage-09-Attestation-Workflows_v2.mp4" employee-compliance-3
enc "Greenboard-ProductPage-10-Marketing-Compliance_v2.mp4" marketing-compliance-1
enc "Greenboard-ProductPage-05-Supervise_v2.mp4" marketing-compliance-2
enc "Greenboard-ProductPage-11-Firm-Compliance_v2.mp4" firm-compliance-1
enc "Greenboard-ProductPage-12-Third-Party-Management_v2.mp4" third-party-compliance-1
enc "GG05_Greenboard_Q2WebAnimations_Automation_v2 (online-video-cutter.com) (1).mp4" ../greenboardgo
echo done
