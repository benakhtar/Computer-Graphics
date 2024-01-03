from transform import Transform


class PointLight:

    def __init__(self, intensity, rgb):
        self.transform = Transform()
        self.intensity = intensity
        self.rgb       = rgb
