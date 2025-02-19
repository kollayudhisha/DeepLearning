import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image
import tempfile
import os

#use the pre trained model yolo 
model=YOLO("yolov8n.pt")
st.title("Real Time Object Detection")
st.markdown("Upload an Image or Video or Live Webcam")
option=st.sidebar.radio("Upload Image/Video/Live Webcam",["Image","Video","LiveWebcam"])


def processImage(image):
    results = model(image)
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box
            class_id = int(box.cls[0])  # Class ID
            confidence = float(box.conf[0])  # Confidence score

            # Draw bounding box and label
            label = f"{model.names[class_id]}: {confidence:.2f}"
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image

if option=="Image":
    upload_image=st.file_uploader("Upload an Image",type=["jpeg","jpg","png"])
    if upload_image:
        image=Image.open(upload_image) #converts BytesIO to image
        Fimage=np.array(image) #converts Image to Numpy array as Numpy cant interpret raw bytes directly.
        #As YOLO,CNN acccept only arrays for processing we need to convert to array.
        result_image=processImage(Fimage)
        st.image(result_image,caption="Detected Objects",use_column_width=True)
        output_file="detected_image.jpg"
        cv2.imwrite(output_file,cv2.cvtColor(result_image,cv2.COLOR_RGB2BGR))
        with open(output_file,"rb") as file:
            st.download_button(label="Download processed image", data=file,file_name="detected_image.jpg",mime="image/jpeg")
        
elif option=="Video":
    upload_video=st.file_uploader("upload video:",type=["mp4","avi","mov"])
    #st.file_uploader() stores uploaded file as a file like object in memory(BytesIO) and it contains raw binary data.
    #cv2 only accepts a actual file path and it cant read BytesIO, so we use tempfile creates a temporary file on disk and system automatically assign a unique file path.
    if upload_video:
        temp_video=tempfile.NamedTemporaryFile(delete=False,suffix=".mp4")
        temp_video.write(upload_video.read())
        #process the video frame-by-frame
        cap=cv2.VideoCapture(temp_video.name) #opens uploaded video, cap contains all frames of the video
        output_video="detected_video.mp4"
        videocompress=cv2.VideoWriter_fourcc(*"mp4v")#compresses frames
        out=cv2.VideoWriter(output_video,videocompress,20,(int(cap.get(3)),int(cap.get(4)))) #20-frames per second, width, height. stores compressed frames after processed by YOLO.
        while cap.isOpened():
            ret,frame=cap.read() #ret tells whether the frame was read successfully, boolean.
            if not ret:
                break
            result_frame=processImage(frame)
            out.write(result_frame)
        cap.release()
        out.release()
        st.video(output_video)#show processed video
        with open(output_video,"rb") as file:
            st.download_button(label="Download processed image", data=file,file_name="detected_video.mp4",mime="video/mp4")

elif option=="LiveWebcam":
    if st.button("Start Webcam"):
        cap=cv2.VideoCapture(0) #open webcam
        stframe=st.empty()
        while cap.isOpened():
            ret,frame=cap.read()
            if not ret:
                break
            result_frame=processImage(frame)
            stframe.image(result_frame,channels="BGR",use_column_width=True)
        cap.release()


        







        



