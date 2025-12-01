# roblox_username_checker
Fast | Multi-Threaded | Roblox Username Rules Enforced | Saves Available Names

This tool checks Roblox username availability while respecting Roblox account naming rules.
It generates valid usernames, checks availability, and safely paces requests to avoid rate-limit errors.
All available usernames are automatically saved for later use.

🔥 Features
Feature	Status
Generates usernames that follow Roblox rules	✔️
Multi-threaded for speed	✔️
Writes available usernames to a file	✔️
Random delays to reduce rate-limits	✔️
Configurable threads	✔️
Lowercase generation for consistency	✔️
📌 Roblox Username Rules Applied

Roblox username constraints (general rules):

3–20 characters

Only letters + numbers

No spaces

No special characters (_, ., -, *, etc. not allowed in new usernames)

Must be unique

Not case-sensitive (we convert to lowercase automatically)

🛠 Requirements
Python 3.8+
pip install requests

🚀 Usage

Run directly:

python roblox_checker.py


Choose thread count:

python roblox_checker.py --threads 10


All available usernames will be saved to:

available_roblox.txt

⚠ Notes

Roblox rate-limits quickly → threads too high may cause blocks

Increase delay if checking large name lengths

Shorter usernames = fewer combinations but harder to find
