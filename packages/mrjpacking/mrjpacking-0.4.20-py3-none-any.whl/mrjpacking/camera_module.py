import cv2
from pygrabber.dshow_graph import FilterGraph

def get_camera_names():
    # Sử dụng pygrabber để lấy danh sách các tên camera
    graph = FilterGraph()
    camera_names = graph.get_input_devices()
    return camera_names

def list_available_cameras():
    index = 0
    available_cameras = []
    camera_names = get_camera_names()

    while True:
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            break
        # Kiểm tra xem index có nằm trong phạm vi camera_names không
        cam_name = camera_names[index] if index < len(camera_names) else f"Unknown Camera {index}"
        available_cameras.append((index, cam_name))
        cap.release()
        index += 1

    if len(available_cameras) == 1:
        return available_cameras[0][0], available_cameras[0][1]
    elif len(available_cameras) > 1:
        print(f"\nĐã tìm thấy {len(available_cameras)} camera:")
        for i, (cam_index, cam_name) in enumerate(available_cameras):
            print(f"{i + 1}. {cam_name}")
        choice = int(input("Chọn camera (nhập số): ")) - 1
        return available_cameras[choice][0], available_cameras[choice][1]
    else:
        print("\nKhông tìm thấy camera nào khả dụng.")
        return None, None

def init_camera():
    selected_camera_index, selected_camera_name = list_available_cameras()
    if selected_camera_index is None:
        return None
    
    try:
        cap = cv2.VideoCapture(selected_camera_index, cv2.CAP_DSHOW)
        if not cap.isOpened():
            raise Exception("\nKhông thể mở camera, kiểm tra lại kết nối hoặc thiết bị.")
        
        print(f"Camera đã được chọn: {selected_camera_name}")
        return cap
    except Exception as e:
        print(f"\nLỗi: {e}")
        return None

def release_camera(cap):
    if cap:
        cap.release()

def read_frame(cap):
    ret, frame = cap.read()
    return ret, frame
