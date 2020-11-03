from server.AppConfig import app, db
from flask import request, jsonify
from server.model.Camera import Camera, CameraSchema
from server.model.FaceModel import FaceModel
from server.model.SenderManager import SenderManager
from server.threads.RstpThread import RstpThread
from server.threads.RstpThreadRunner import RstpThreadRunner
from server.udp.UdpSender import UdpSender

camera_schema = CameraSchema()
cameras_schema = CameraSchema(many=True)
udp_sender = None

@app.route('/camera', methods=['POST'])
def add_camera():
    ip = request.json['ip']
    port = request.json['port']
    user = request.json['user']
    password = request.json['password']
    rtsp_path = request.json['rtsp_path']

    new_camera = Camera(ip, port, user, password, rtsp_path)
    db.session.add(new_camera)
    db.session.commit()

    return camera_schema.jsonify(new_camera)


@app.route('/camera', methods=['GET'])
def get_all_camera():
    all_camera = Camera.query.all()
    result = cameras_schema.dump(all_camera)
    return jsonify(result)


@app.route('/camera/<id>', methods=['GET'])
def get_camera_by_id(id):
    camera = Camera.query.get(id)
    return camera_schema.jsonify(camera)


@app.route('/camera/<id>', methods=['DELETE'])
def delete_camera_by_id(id):
    camera = Camera.query.get(id)
    db.session.delete(camera)
    db.session.commit()
    return camera_schema.jsonify(camera)


@app.route('/camera/<id>', methods=['PUT'])
def update_camera(id):
    camera = Camera.query.get(id)
    ip = request.json['ip']
    port = request.json['port']
    user = request.json['user']
    password = request.json['password']
    rtsp_path = request.json['rtsp_path']

    camera.ip = ip
    camera.port = port
    camera.user = user
    camera.password = password
    camera.rtsp_path = rtsp_path

    db.session.commit()

    return camera_schema.jsonify(camera)


sender_manager = SenderManager()
thread_runner = RstpThreadRunner()


@app.route('/streaming/<camera_id>', methods=['GET'])
def start_udp_streaming(camera_id):
    print('start start_udp_streaming from ' + str(camera_id))
    camera = Camera.query.get(camera_id)
    thread_name = str(camera.get_connect_url())
    thread_runner.set_upd_stream(thread_name)
    return jsonify(str('OK'))






@app.route('/rtsp/start/<camera_id>', methods=['GET'])
def start_rtsp_streaming(camera_id):
    global udp_sender
    print('start_rtsp_streaming with camera_id ' + camera_id)
    camera = Camera.query.get(camera_id)
    model = FaceModel()
    if udp_sender is None:
        udp_sender = UdpSender('localhost', 8089)
    thread = RstpThread(camera, model, sender_manager, udp_sender)
    thread_runner.run_rstp_thread(thread, camera.get_connect_url())
    return jsonify(str(thread.getName()))


if __name__ == '__main__':
    app.run(debug=True)
