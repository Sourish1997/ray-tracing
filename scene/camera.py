class Camera:
    def __init__(self, cam_from, cam_to, u, v, fov, width, height):
        self.cam_from = cam_from
        self.cam_to = cam_to
        self.u = u
        self.v = v
        self.width = width
        self.height = height
        self.fov = fov
