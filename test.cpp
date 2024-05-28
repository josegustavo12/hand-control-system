#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>

using namespace cv;
using namespace std;

int countFingers(const vector<Point>& contour, const vector<Point>& hull) {
    int count = 0;
    for (int i = 0; i < contour.size(); i++) {
        Point point = contour[i];
        if (point.y < 500) continue; // Ajuste conforme necessário para a altura da mão

        bool isFinger = true;
        for (int j = 0; j < hull.size(); j++) {
            if (point == hull[j]) continue;
            double distance = norm(point - hull[j]);
            if (distance < 25) {
                isFinger = false;
                break;
            }
        }
        if (isFinger) count++;
    }
    return count;
}

int main() {
    VideoCapture cap(0);
    if (!cap.isOpened()) {
        cout << "Erro ao abrir a câmera!" << endl;
        return -1;
    }

    Mat frame, frameGray, frameBlur, frameThreshold;
    while (true) {
        cap >> frame;
        if (frame.empty()) break;

        cvtColor(frame, frameGray, COLOR_BGR2GRAY);
        GaussianBlur(frameGray, frameBlur, Size(5, 5), 0);
        threshold(frameBlur, frameThreshold, 0, 255, THRESH_BINARY | THRESH_OTSU);

        vector<vector<Point>> contours;
        findContours(frameThreshold, contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);
        
        if (contours.size() > 0) {
            vector<Point> largestContour = contours[0];
            double largestArea = contourArea(largestContour);
            for (const auto& contour : contours) {
                double area = contourArea(contour);
                if (area > largestArea) {
                    largestArea = area;
                    largestContour = contour;
                }
            }

            vector<Point> hull;
            convexHull(largestContour, hull);
            drawContours(frame, { largestContour }, -1, Scalar(0, 255, 0), 2);
            drawContours(frame, { hull }, -1, Scalar(255, 0, 0), 2);

            int fingers = countFingers(largestContour, hull);
            putText(frame, to_string(fingers), Point(50, 50), FONT_HERSHEY_SIMPLEX, 1, Scalar(0, 0, 255), 2);
        }

        imshow("Contador de Dedos", frame);
        if (waitKey(1) == 27) break; // Pressione ESC para sair
    }

    cap.release();
    destroyAllWindows();
    return 0;
}
