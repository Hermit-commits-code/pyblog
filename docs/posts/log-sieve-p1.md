---
tags:
  - Python
  - Cybersecurity
  - Threat-Hunting
---
# Project: Log-Sieve (Part 1) - Detecting Impossible Travel

What is "Impossible Travel"? It's the digital equivalent of seeing someone walk through a front door in New York and out a back door in London five seconds later.

## The Security Gap

Standard authentication logs tell you *who* logged in, but they don't tell you if it's *physically possible* for that person to be there.

## The Logic

The **Log-Sieve** is a Python-based forensic tool I’m building to:

1. Parse system logs for successful logins.
2. Geocode the IP addresses to find Latitude/Longitude.
3. Compare the time-delta between consecutive logins.
4. Calculate if the speed required to travel between those two points exceeds the speed of a commercial jet.

If the speed is 5,000 mph, we don't just have a login; we have a compromised credential.
