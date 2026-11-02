# File Location: ~/CPE302L_Lab08/app.py
import platform
import sys

print("==================================================")
print(" Hello from CPE302L Lab 08 Containerized App!")
print(f" Python Version : {sys.version.split()[0]}")
print(f" Container OS   : {platform.system()} {platform.release()}")
print(" Execution Status: SUCCESS (Namespace/cgroup active)")
print("==================================================")
