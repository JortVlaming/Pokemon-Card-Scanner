import cv2
import numpy as np
import cardData
import utils


def readCard():
    cam = cv2.VideoCapture(0)   # Use Video source 1 = phone; 0 = computer webcam

    # Scaled to the IRL height and width of a Pokemon card (6.6 cm x 8.8 cm)
    widthCard = utils.getWidthCard()
    heightCard = utils.getHeightCard()

    while True:
        # Create a blank image
        blackImg = np.zeros((heightCard, widthCard, 3), np.uint8)

        # Check if using phone camera or saved picture
        check, frame = cam.read()

        # Make image gray scale
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Blur the image to reduce noise
        blurredFrame = cv2.GaussianBlur(grayFrame, (3, 3), 0)

        # Use Canny edge detection to get edges
        edgedFrame = cv2.Canny(image=blurredFrame, threshold1=100, threshold2=200)

        # Clean up edges
        kernel = np.ones((5,5))
        frameDial = cv2.dilate(edgedFrame, kernel, iterations=2)
        frameThreshold = cv2.erode(frameDial, kernel, iterations=1)

        # Get image contours
        contourFrame = frame.copy()
        bigContour = frame.copy()
        contours, hierarchy = cv2.findContours(frameThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(contourFrame, contours, -1, (0, 255, 0), 10)

        imgWarpColored = blackImg  # Set imgWarpColored
        # Get biggest contour
        corners, maxArea = utils.biggestContour(contours)
        if len(corners) == 4:
            corners = [corners[0][0], corners[1][0], corners[2][0], corners[3][0]]
            corners = utils.reorderCorners(corners)  # Reorders corners to [topLeft, topRight, bottomLeft, bottomRight]
            #cv2.drawContours(bigContour, corners, -1, (0, 255, 0), 10)
            bigContour = utils.drawRectangle(bigContour, corners)
            pts1 = np.float32(corners)
            pts2 = np.float32([[0, 0], [widthCard, 0], [0, heightCard], [widthCard, heightCard]])
            # Makes a matrix that transforms the detected card to a vertical rectangle
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            # Transforms card to a rectangle widthCard x heightCard
            imgWarpColored = cv2.warpPerspective(frame, matrix, (widthCard, heightCard))

        # Resize all of the images to the same dimensions
        # Note: imgWarpColored is already resized and matchingCard gets resized in utils.getMatchingCard()
        frame = cv2.resize(frame, (widthCard, heightCard))
        grayFrame = cv2.resize(grayFrame, (widthCard, heightCard))
        blurredFrame = cv2.resize(blurredFrame, (widthCard, heightCard))
        edgedFrame = cv2.resize(edgedFrame, (widthCard, heightCard))
        contourFrame = cv2.resize(contourFrame, (widthCard, heightCard))
        bigContour = cv2.resize(bigContour, (widthCard, heightCard))

        # Check if a matching card has been found, and if so, display it
        found, matchingCard = utils.findCard(imgWarpColored.copy())  # Check to see if a matching card was found

        # An array of all 8 images
        imageArr = ([frame, grayFrame, blurredFrame, edgedFrame],
                    [contourFrame, bigContour, imgWarpColored, matchingCard])

        # Labels for each image
        labels = [["Original", "Gray", "Blurred", "Threshold"],
                  ["Contours", "Biggest Contour", "Warped Perspective", "Matching Card"]]

        # Stack all 8 images into one and add text labels
        stackedImage = utils.makeDisplayImage(imageArr, labels)

        # Display the image
        cv2.imshow("Card Finder", stackedImage)

        # Check for key press
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):  # Quit if 'q' is pressed
            break
        elif found and key != 255:  # If card found and any other key pressed, acknowledge and continue
            print('Card detected! Press any key to continue scanning, or Q to quit.')

    # Stops cameras and closes display window
    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # Automatically check if database needs regeneration
    if cardData.needsDatabaseRegeneration():
        print("Database needs regeneration (missing files or new cards detected)")
        cardData.createDatabase()
        print()
    
    readCard()  # Finds and reads from a saved image or live feed
