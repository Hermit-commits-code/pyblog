---
tags:
  - Python
  - Mathematics
  - Cybersecurity
---
# Project: Log-Sieve (Part 3) - The Impossible Verdict

In the final phase of this project, I integrated the **Haversine Formula** to bridge the gap between simple data extraction and actionable security intelligence.

## The Math of a Sphere

Standard flat geometry doesn't work for global tracking. By implementing the Haversine formula, the script calculates the "Great Circle" distance between two sets of coordinates.

## Live Test Results

Analyzing my mock authentication logs produced a staggering result:

* **Login 1**: Pensacola, FL
* **Login 2**: Hong Kong (10 minutes later)
* **Calculated Distance**: 13,711.42 km

## Conclusion: Security Through Geometry

By tracking the `last_location` state and comparing it to current hits, the **Log-Sieve** mathematically proves when an account has been compromised. Even if a hacker has your password, they cannot break the laws of physics.
