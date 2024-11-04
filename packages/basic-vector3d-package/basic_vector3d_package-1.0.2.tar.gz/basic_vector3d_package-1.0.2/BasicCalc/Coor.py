class Coordinate:
    def __init__(self, x=0.0, y=0.0, z=0.0):
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
        return Coordinate(-self._x, -self._y, -self._z)

    def is_zero(self):
        return abs(self.x - 0.0) < 1e-3 and abs(self.y - 0.0) < 1e-3 and abs(self.z - 0.0) < 1e-3

    def __repr__(self):
        return f"Coord - ({self._x}, {self._y}, {self._z})"

    def __add__(self, other):
        if not isinstance(Coordinate, other):
            raise TypeError("other is not Coordinate object")
        return Coordinate(self._x + other.x, self._y + other.y, self._z + other.z)

    def __sub__(self, other):
        if not isinstance(Coordinate, other):
            raise TypeError("other is not Coordinate object")
        return Coordinate(self._x - other.x, self._y - other.y, self._z - other.z)

    def __eq__(self, other):
        if not isinstance(Coordinate, other):
            raise TypeError("other is not Coordinate object")
        return self._x == other.x and self._y == other.y and self._z == other.z




