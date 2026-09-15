from core.coordinate import Coordinate

class Clipper:
    def clipping(self, coords):
        match len(coords):
            case(1):
                return coords
            case(2):
                return self.cohen_sutherland(coords)
            case _:
                return coords

    def cohen_sutherland(self, coords):
        p1, p2 = coords

        rc1 = self.__calculate_rc(p1)
        rc2 = self.__calculate_rc(p2)

        while True:
            if (rc1 | rc2) == 0b0000:
                return [p1, p2]

            if (rc1 & rc2) != 0b0000:
                return [Coordinate(0, 0), Coordinate(0, 0)]

            if rc1 != 0b0000:
                rc = rc1
                p = p1
            else:
                rc = rc2
                p = p2

            if rc & 0b0001:
                y = (p2.y - p1.y) * (-1 - p.x) / (p2.x - p1.x) + p.y
                x = -1

            elif rc & 0b0010:
                y = (p2.y - p1.y) * (1 - p.x) / (p2.x - p1.x) + p.y
                x = 1

            elif rc & 0b1000:
                x = p.x + (p2.x - p1.x) * (1 - p.y) / (p2.y - p1.y)
                y = 1

            elif rc & 0b0100:
                x = p.x + (p2.x - p1.x) * (-1 - p.y) / (p2.y - p1.y)
                y = -1

            intersection = Coordinate(x, y)

            if rc == rc1:
                p1 = intersection
                rc1 = self.__calculate_rc(p1)
            else:
                p2 = intersection
                rc2 = self.__calculate_rc(p2)

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

    def __calculate_ac(self, line_coords):
        ac = (line_coords[1].y - line_coords[0].y) / (line_coords[1].x - line_coords[0].x)

        if ac == 0:
            raise ValueError("AC is zero!")

        return ac