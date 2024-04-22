import cv2
import cvzone
import pygame
from cvzone.HandTrackingModule import HandDetector
import time
import random

# Initialize Pygame mixer
pygame.mixer.init()

# Load sound effects
sound_win = pygame.mixer.Sound("sounds/win_sound.wav")
sound_lose = pygame.mixer.Sound("sounds/lose_sound.wav")

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Initialize the hand detector
detector = HandDetector(maxHands=1)

# Initialize game variables
timer = 0
stateResults = False
startGame = False
scores = [0,0] # [COMPUTER, PLAYER]
comp_win_count = 0
player_win_count = 0
resetGame = True 

while True:
    imgBG = cv2.imread("Resources/BG.png")
    success, img = cap.read()

    # Resize the input frame
    imgScaled = cv2.resize(img, (0,0), None, 0.875, 0.875)
    imgScaled = imgScaled[:,80:480]

    # Find hands
    hands, img, = detector.findHands(imgScaled)

    if startGame:
        
        if stateResults is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255,0,255), 4)

            if timer > 3:
                stateResults = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0,0,0,0,0]: # Rock
                        playerMove = 1         
                    if fingers == [1,1,1,1,1]: # Paper
                        playerMove = 2
                    if fingers == [0,1,1,0,0]: # Scissors
                        playerMove = 3

                    randomNumber = random.randint(1,3) # Random choose 1-3 for computer move
                    imgAI = cv2.imread(f"Resources/{randomNumber}.png", cv2.IMREAD_UNCHANGED) # unchange is IMPORTANT for overlay
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    # Update scores based on the game outcome
                    if (playerMove == 1 and randomNumber == 3) or \
                        (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1 # Player wins
                        sound_win.play()  # Play winning sound
                    elif (playerMove == 3 and randomNumber == 1) or \
                          (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1 # Computer wins
                        sound_lose.play()  # Play losing sound

    imgBG[234:654,795:1195] = imgScaled

    # Counting the win for comp and player respectively
    if scores[0] >= 10:
        comp_win_count += 1
        scores = [0, 0] # reset scores
        resetGame = True # allow game to be reset

    if scores[1] >= 10:
        player_win_count += 1
        scores = [0, 0] # reset scores
        resetGame = True # allow game to be reset

    if stateResults:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    # Display scores
    cv2.putText(imgBG, str(int(scores[0])), (414, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 6)
    cv2.putText(imgBG, str(int(scores[1])), (1119, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 6)

    # Display win message for either computer or player
    if comp_win_count > 0:
        win_message = f"Computer has won {comp_win_count} times! Press 'r' to reset the game."
        cv2.putText(imgBG, win_message, (300, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    if player_win_count > 0:
        win_message = f"Player has won {player_win_count} times! Press 'r' to reset the game."
        cv2.putText(imgBG, win_message, (300, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    
    # Display the game interface
    cv2.imshow("Rock-Paper-Scissors Game", imgBG)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResults = False
        resetGame = False
    if key == ord('r'):
        comp_win_count = 0
        player_win_count = 0
        scores = [0, 0]
        resetGame = True

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()