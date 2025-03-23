import cv2

def visualize_search_area(rect, duration: int = 2, window_name: str = "Search Area"):
    """
    Draws a red box around the specified search area and displays it.
    
    Args:
        rect (Rectangle): The Rectangle object (must have screenshot(), width, and height).
        duration (int): Duration to show the image in seconds.
        window_name (str): Title of the display window.
    """
    screenshot = rect.screenshot()
    img_with_box = screenshot.copy()

    cv2.rectangle(
        img_with_box,
        (0, 0),
        (rect.width - 1, rect.height - 1),
        (0, 0, 255),  # Red in BGR
        2
    )

    cv2.imshow(window_name, img_with_box)
    cv2.waitKey(duration * 1000)
    cv2.destroyAllWindows()
