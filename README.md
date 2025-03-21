🎲 Dice Roll Game (beta0.2)
A fullscreen idle dice game made with Pygame, where you roll dice, earn points, and purchase upgrades to increase your power!

🚀 Features:
Roll dice to gain score based on dice values, multipliers, and exponent upgrades.
Upgrade max dice value, minimum dice value, multiplier, and exponent power.
Score scales with extremely large numbers, displayed in shortened format (K, M, B... all the way up to crazy suffixes!).
Automated rolling (auto-click) unlockable after resetting.
Reset mechanic that triggers on overflow errors, allowing you to spend resets on faster animations or unlocking automation.
Save and load system using pickle so you don’t lose progress.
🎮 How to Play
Launch the game — it will run in fullscreen mode.
Click the Roll button or wait for auto-roll (if unlocked).
Accumulate score by rolling dice. Your score = (final roll * multiplier) ^ exponent.
Upgrade:
Max dice value: Increases the maximum rollable number.
Min dice value: Increases the minimum rollable number.
Multiplier: Increases the roll multiplier.
Exponent: Increases the exponent for final score calculation.
When overflow happens (game resets), you can spend resets to:
Speed up the dice animation.
Unlock automation (auto-roll).
⚙️ Requirements
Python 3.x
Pygame (pip install pygame)
💾 Saving & Loading
The game automatically saves your progress in savefile.pkl.
The code supports loading from previous versions and converting old save formats.
🛠 Current Version
beta0.2
