import math


class Vector3d:
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value

    def reverse(self):
        return Vector3d(-self._x, -self._y, -self._z)

    def length(self):
        return math.sqrt(math.pow(self._x, 2) + math.pow(self._y, 2) + math.pow(self._z, 2))

    def normalization(self):
        return Vector3d(self._x / self.length(), self._y / self.length(), self._z / self.length())

    def shift(self, direction, offset):
        if not isinstance(direction, Vector3d):
            raise TypeError("direction is not Vector3d object")
        if not isinstance(offset, float):
            raise TypeError("offset is not float object")
        norm = direction.normalization()
        return Vector3d(self._x + offset * norm.x, self._y + offset * norm.y, self._z + offset * norm.z)

    def is_zero(self):
        return abs(self.x - 0.0) < 1e-3 and abs(self.y - 0.0) < 1e-3 and abs(self.z - 0.0) < 1e-3

    def is_vertical(self, other):
        if not isinstance(other, Vector3d):
            raise TypeError("other is not Vector3d object")
        cos_value = self.cos_value(other)
        if self.is_zero() or other.is_zero():
            return False
        return abs(cos_value - 1.0) < 1e-3

    def is_relative_parallel(self, other):
        if not isinstance(other, Vector3d):
            raise TypeError("other is not Vector3d object")
        if self.is_zero() or other.is_zero():
            return True
        cos_value = self.cos_value(other)
        return abs(cos_value + 1.0) < 1e-3 or abs(cos_value - 1.0) < 1e-3

    def is_abs_parallel(self, other):
        if not isinstance(other, Vector3d):
            raise TypeError("other is not Vector3d object")
        if self.is_zero() or other.is_zero():
            return True
        cos_value = self.cos_value(other)
        return abs(cos_value - 1.0) < 1e-3

    def cos_value(self, other):
        if not isinstance(other, Vector3d):
            raise TypeError("other is not Vector3d object")
        if self.is_zero() or other.is_zero():
            return 1.0
        return self.__mul__(other) / (self.length() * other.length())

    def radians_degree(self, other):
        if not isinstance(other, Vector3d):
            raise TypeError("other is not Vector3d object")
        if self.is_zero() or other.is_zero():
            return 0.0
        return math.acos(self.cos_value(other))

    def degree(self, other):
        if not isinstance(other, Vector3d):
            raise TypeError("other is not Vector3d object")
        if self.is_zero() or other.is_zero():
            return 0.0
        return self.radians_degree(other) * (180 / math.pi)

    def __repr__(self):
        return f"Vector3d - ({self._x}, {self._y}, {self._z})"

    def __add__(self, other):
        if not isinstance(other, Vector3d):
            raise TypeError("other is not Vector3d object")
        return Vector3d(self._x + other.x, self._y + other.y, self._z + other.z)

    def __sub__(self, other):
        if not isinstance(other, Vector3d):
            raise TypeError("other is not Vector3d object")
        return Vector3d(self._x - other.x, self._y - other.y, self._z - other.z)

    def __eq__(self, other):
        if not isinstance(other, Vector3d):
            raise TypeError("other is not Vector3d object")
        return self._x == other.x and self._y == other.y and self._z == other.z

    def __mul__(self, other):
        if not isinstance(other, Vector3d):
            raise TypeError("other is not Vector3d object")
        return self._x * other.x + self._y * other.y + self._z * other.z




