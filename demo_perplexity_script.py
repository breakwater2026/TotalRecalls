"""ShareX / scripted demo — Perplexity only (LS onboarding).
Flow: Page1 dropdown→Perplexity → login/download → Page2 download → complete → Open folder → Explorer → Word.
Adjust (x,y) to your screen. Add 1.5s pauses between actions for ShareX capture."""
import pyautogui, time
pyautogui.PAUSE = 1.5
# Page 1
pyautogui.click(120, 420)  # provider dropdown
pyautogui.click(120, 520)  # Perplexity
pyautogui.click(200, 680)  # Log in / Download button (updates to Perplexity)
# Page 2 (after nav)
pyautogui.click(180, 850)  # Download my conversations
# After complete
pyautogui.click(250, 980)  # Open folder (Explorer opens)
# Word opens via Explorer click (manually click file, or add click here)
