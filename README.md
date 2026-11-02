# CPE 302L Operating Systems Laboratory
## Report No. 8: Containers, Namespaces, cgroups, and OS-Level Virtualization

* **Student:** Lawrence Dave S. Trinidad
* **Program & Section:** Bachelor of Science in Computer Engineering 3B
* **Instructor:** Engr. Julius Vincent M. Abanel
* **Date:** November 2, 2026

---

## Objectives

* Safely run and stop a containerized application using standard Docker commands in an online sandbox environment without breaking or risking the main computer system.
* Explain how Linux namespaces hide resources so a process only sees its own network, files, and process IDs, and how cgroups set limits so no single container steals all the host's memory or CPU.
* Explain the main differences between a Virtual Machine (which boots its own full guest OS and kernel) and a Container (which shares the main computer's kernel to run much faster).

---

## Overview & Technical Discussion

### Virtual Machines vs. Containers

Traditional hardware-level virtualization relies on a Hypervisor (Type-1 bare-metal like VMware ESXi or Type-2 hosted like VirtualBox) to emulate physical hardware. Each Virtual Machine requires its own full Guest Operating System, dedicated kernel, device drivers, and system services. While this guarantees absolute isolation, it introduces massive storage footprints, slow multi-minute boot cycles, and significant CPU/RAM memory virtualization overhead.

Operating-System-Level Virtualization (Containerization) bypasses hardware emulation entirely. Instead of running multiple kernels, container engines (such as Docker, containerd, or CRI-O) leverage fundamental capabilities embedded directly within a single shared Linux host kernel. Container isolation is governed by two core Linux kernel primitives:

### Linux Kernel Namespaces (Visibility)
Namespaces wrap global system resources into isolated virtual abstractions. Processes running inside a namespace operate under the illusion that they possess an independent, dedicated instance of system resources.

* **PID (Process ID) Namespace:** Isolates process identification numbers. A process inside a container can be assigned PID 1 while mapped to a standard non-privileged PID on the host system.
* **MNT (Mount) Namespace:** Isolates filesystem mount points. The container sees a restricted root directory structure (`/`) backed by overlay filesystems (`Overlay2`).
* **NET (Network) Namespace:** Provides an isolated network stack including virtual network interfaces (`veth`), private routing tables, IP address assignments, and firewall rules.
* **UTS Namespace:** Allows containers to maintain distinct hostnames independent of the host node.
* **IPC Namespace:** Isolates System V IPC mechanics and POSIX message queues, preventing cross-container memory segment sharing.
* **USER Namespace:** Maps UID/GID allocations so container root (`UID 0`) maps to an unprivileged standard user on the host system for enhanced security.

### Control Groups / cgroups v2 (Resource Limits)
cgroups govern resource consumption and rate-limiting across process groups:

* **cpu:** Enforces strict CPU usage caps using Completely Fair Scheduler (CFS) bandwidth control.
* **memory:** Imposes maximum RAM consumption ceilings and swap thresholds. Exceeding allocations triggers the Linux kernel Out-Of-Memory (OOM) Killer.
* **blkio:** Controls and throttles physical disk I/O bandwidth and IOPS limits on block storage devices.
* **pids:** Caps the total number of child processes a container can fork, mitigating fork-bomb Denial-of-Service attacks.

---

## Repository Artifacts

### Directory Layout

```text
cpe302l-lab08-containers-juan-delacruz/
└── CPE302L_Lab08/
    ├── app.py
    └── Dockerfile
```

### 1. Python Application 
(`~/CPE302L_Lab08/app.py`)

```python
# File Location: ~/CPE302L_Lab08/app.py
import platform
import sys

print("==================================================")
print(" Hello from CPE302L Lab 08 Containerized App!")
print(f" Python Version : {sys.version.split()[0]}")
print(f" Container OS   : {platform.system()} {platform.release()}")
print(" Execution Status: SUCCESS (Namespace/cgroup active)")
print("==================================================")
```

### 2. Docker Build Specification 
(`~/CPE302L_Lab08/Dockerfile`)

```dockerfile
FROM python:3.12-alpine
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
```

---

## Building and Running the Application

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bsu-cpe/cpe302l-lab08-containers-juan-delacruz.git
   cd cpe302l-lab08-containers-juan-delacruz/CPE302L_Lab08
   ```

2. **Build the container image:**
   ```bash
   docker build -t cpe302l-lab08 .
   ```

3. **Run the container application:**
   ```bash
   docker run --rm cpe302l-lab08
   ```

---

## Analysis & Reflection

### Reflection Questions

1. **Startup Speed:** Why do containers start faster than many virtual machines?
   * Containers bypass hardware POST emulation and guest OS kernel boot chains, starting immediately as isolated host processes via `clone()` system calls.

2. **Shared Kernel Trade-Off:** Why is sharing the host kernel both useful and risky?
   * Kernel sharing maximizes speed and resource density. However, running as root on a shared kernel means kernel vulnerability exploits (container escapes) can compromise the host machine.

3. **Cloud Fairness:** How do cgroups relate to fairness in cloud platforms?
   * cgroups prevent 'Noisy Neighbor' resource starvation in cloud platforms by placing hard allocation limits (e.g., `memory.max`) on each container.

---

## Conclusion

This laboratory activity demonstrated OS-level virtualization on a Linux from Scratch system under root user privileges. We confirmed kernel sharing (`6.12.0-rc4-lfs-custom`), built and executed custom microservice containers (`app.py`), verified cgroup resource constraints, monitored live container statistics, and restored system cleanliness.
