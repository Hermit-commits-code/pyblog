---
tags:
  - Python
  - Regex
  - Geolocation
---
# Project: Log-Sieve (Part 2) - From Raw Text to Coordinates

The first challenge of building a security detective is teaching it to "read." System logs are messy, but they follow a strict structure that we can exploit.

## Step 1: Regex Extraction

I used a **Regular Expression** to slice through the standard Linux `auth.log` format. By targeting the "Accepted password" string, I was able to pull the three critical pieces of evidence:

1. **The Timestamp**: When the event happened.
2. **The User**: Whose account was accessed.
3. **The IP Address**: The digital origin of the login.

## Step 2: Adding a "Sense of Place"

An IP address is just a number. To turn it into a location, I integrated the `ip-api.com` service via the Python `requests` library.

Now, instead of just seeing `1.1.1.1`, the script reports **Hong Kong**. This enrichment is the foundation for our "Impossible Travel" detection logic.

## What's Next?

Now that we have the coordinates (Latitude and Longitude), we need to calculate the physical distance between consecutive logins. If the distance is 10,000 miles and the time difference is only 10 minutes, we've found our smoking gun.
