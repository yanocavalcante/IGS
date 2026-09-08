from core.coordinate import Coordinate

class Clipper:
    def cohen_sutherland(self, coords):
        rcs = []
        print(coords)
        for coord in coords:
            rcs.append(self.__calculate_rc(coord))

        if rcs[0] != rcs[1]:
            if rcs[0] & rcs[1] == 0:
                print("Partially")
            else:
                print("Outside")
                return [Coordinate(0, 0), Coordinate(0, 0)]
        else:
            if rcs[0] & rcs[1] == 0:
                print("Inside")
            else:
                print("Outside")
                return [Coordinate(0, 0), Coordinate(0, 0)]

        return coords

    def liang_barsky(self, line):
        pass

    def nicholl_lee_nicholl(self, line):
        pass

    def weiler_atherton(self):
        pass

    def __calculate_rc(self, coord: Coordinate):
        rc = 0b0000

        if coord.x < -1:
            rc += 0b0001

        if coord.x > 1:
            rc += 0b0010

        if coord.y < -1:
            rc += 0b0100

        if coord.y > 1:
            rc += 0b1000

        return rc