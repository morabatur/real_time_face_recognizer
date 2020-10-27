from server.model.Camera import Camera
from server.model.CameraMap import CameraMap
from server.model.FaceModel import FaceModel
from server.threads.RstpThread import RstpThread
from server.threads.RstpThreadRunner import RstpThreadRunner
from server.model.SenderManager import SenderManager


model = FaceModel()

laptop_camera = Camera('local', 0, '', '', '')

sender_manager = SenderManager()
sender_manager.set_stream_ip('local')

thread_runner = RstpThreadRunner()

camera_map = CameraMap()
camera_map.add(laptop_camera.ip, laptop_camera)

for camera in camera_map.map():
    thread = RstpThread(camera_map.get(camera), model, sender_manager)
    thread_runner.run_rstp_thread(thread, camera_map.get(camera).get_connect_url())

