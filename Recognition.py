import cv2
from pyzbar.pyzbar import decode

class Recognition:
    data = []
    def __init__(self) -> None:
        pass

    def run(self):
        self.cam = self.cam_ON()
        while True:
            self.frame = self.reading()
            self.recognized = self.recognition()
            for object in self.recognized:
                self.object = object
                self.highlight()
                self.print_out()
            self.cam_out()
            if self.quit_program():
                break
        self.cam_OFF()

    def cam_ON(self):
        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        return cam

    def reading(self):
        ret, frame = self.cam.read()
        return frame

    def recognition(self):
        recognized = decode(self.frame)
        return recognized

    def highlight(self):
        bbox = self.object.rect
        cv2.rectangle(self.frame, (bbox.left, bbox.top), (bbox.left + bbox.width, bbox.top + bbox.height), (0, 255, 0), 2)

    def print_out(self):
        output = self.object.data.decode("utf-8")
        print("QR Code Data:",'\033[33m', output,'\033[0m')
        if output not in Recognition.data:
            Recognition.data.append(output)

    def cam_out(self):    
        cv2.imshow("QR Code Reader", self.frame)

    def quit_program(self):
        return cv2.waitKey(1) & 0xFF == ord('q')

    def cam_OFF(self):
        self.cam.release()
        cv2.destroyAllWindows()
        print("", '\033[32m')
        print("="*50)
        print("Data:", Recognition.data)
        print("Len =", len(Recognition.data))
        print("="*50, '\033[0m')

Recognition().run()