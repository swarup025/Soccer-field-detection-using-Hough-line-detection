import cv2
import numpy as np
import math

def find_intersection(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denominator != 0:
        intersection_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
        intersection_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator
        return int(intersection_x), int(intersection_y)

    return None

def calculate_angle(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2

    angle = math.atan2(y2 - y1, x2 - x1)
    angle = math.degrees(angle)
    if angle < 0:
        angle += 360

    return angle

def main():
    # Step 1: Load the image
    image_path = "houghlines4.jpg"
    image = cv2.imread(image_path)
    image1 = cv2.imread("1st.png")
    image1 = cv2.resize(image1, (640,480))

    # Step 2: Apply Canny edge detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    # Step 3: Apply HoughLinesP to detect lines
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

    # Step 4: Find intersection points for lines with angle between 45 and 90 degrees
    intersections = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            line1 = lines[i][0]
            line2 = lines[j][0]

            intersection = find_intersection(line1, line2)
            if intersection is not None:
                x, y = intersection
                if 0 <= x < 640 and 0 <= y < 480:
                    intersections.append(intersection)

    # Step 5: Sort the intersection points in ascending order
    intersections.sort()

    # Step 6: Filter the intersection points based on the gap of 30 or more in both x and y coordinates
    filtered_intersections = []
    for i in range(len(intersections) - 1):
        x1, y1 = intersections[i]
        x2, y2 = intersections[i + 1]
        if abs(x2 - x1) >= 30 and abs(y2 - y1) >= 30:
            filtered_intersections.append(intersections[i])
    filtered_intersections.append(intersections[-1])

    # Step 7: Print the list of intersection points
    print("Intersection points:")
    for intersection in filtered_intersections:
        print(intersection)

    # Step 8: Draw the points on the image
    for intersection in filtered_intersections:
        cv2.circle(image, intersection, 3, (0, 255, 0), -1)

    # Step 9: Sort the coordinates in intersection clockwise
    center_x = sum(point[0] for point in filtered_intersections) / len(filtered_intersections)
    center_y = sum(point[1] for point in filtered_intersections) / len(filtered_intersections)
    filtered_intersections.sort(key=lambda point: np.arctan2(point[1] - center_y, point[0] - center_x))

    # Step 10: Take each element of intersection as an (x, y) coordinate and write it in the image
    for i, point in enumerate(filtered_intersections):
        cv2.putText(image, f"({point[0]}, {point[1]})", (point[0] + 5, point[1] + 5), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 255), 2)

    # Step 11: Draw lines between the selected intersection points
    for i in range(len(filtered_intersections)):
        cv2.line(image, filtered_intersections[i], filtered_intersections[(i + 1) % len(filtered_intersections)],
                 (255, 0, 0), 2)
    # Step 12: Distinguish between coordinates of both lines
    cv2.line(image, (0, 480), (640, 0), (255, 199, 211), 2)
    interchanged_list = [filtered_intersections[0], filtered_intersections[2], filtered_intersections[3], filtered_intersections[1]]
    side1 = []
    side2 = []
    new_points = []
    
    for point in interchanged_list:
        x, y = point
        # Check if the point is above the line
        if y < (480 - (x * 480 / 640)):
            side1.append(point)
            if x < 100:
                ynew = y + 200
                new_points.append((13, ynew))
            elif 100 <= x < 200:
                ynew = y + 100
                new_points.append((13, ynew))
            elif 200 <= x < 300:
                ynew = y + 110
                new_points.append((13, ynew))
            elif 300 <= x < 400:
                ynew = y + 60
                new_points.append((13, ynew))
            elif 400 <= x <= 500:
                ynew = y + 70
                new_points.append((13, ynew))
            elif x >= 500:
                ynew = y + 10
                new_points.append((13, ynew))
            
        else:
            side2.append(point)
            if x < 100:
                ynew = y + 200
                new_points.append((126, ynew))
            elif 100 <= x < 200:
                ynew = y + 100
                new_points.append((126, ynew))
            elif 200 <= x < 300:
                ynew = y + 110
                new_points.append((126, ynew))
            elif 300 <= x < 400:
                ynew = y + 60
                new_points.append((126, ynew))
            elif 400 <= x < 500:
                ynew = y + 70
                new_points.append((126, ynew))
            elif x >= 500:
                ynew = y + 10
                new_points.append((126, ynew))
                
    print("Side 1:")
    for point in side1:
        print(point)

    print("Side 2:")
    for point in side2:
        print(point)
    
    print("New coordinates:")
    for point in new_points:
        print(point)
    
    #Homography
    result_list1 = [list(t) for t in interchanged_list]
    result_list2 = [list(t) for t in new_points]
    destination = cv2.imread("FieldDiagram.png")
    pts_src = np.array(result_list1)
    pts_dst = np.array(result_list2)
    h,status = cv2.findHomography(pts_src, pts_dst)
    im_out = cv2.warpPerspective(image1, h, (destination.shape[1],destination.shape[0]))
    cv2.imshow("Warped Source Image", im_out)
    
    # Display the image with points and lines
    cv2.imshow("Intersections", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()



























