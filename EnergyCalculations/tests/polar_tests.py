from math import sqrt, atan, pi

def polar(x, y):
    dist = sqrt(pow(x, 2) + pow(y, 2))
    angle = atan(abs(x)/(abs(y)+0.0000001)) * 180 / pi
    if x > 0 and y > 0:
        angle = 180 + -angle
    if x > 0 and y < 0:
        angle = angle
    if x < 0 and y > 0:
        angle = -180 + angle
    if x < 0 and y < 0:
        angle = -angle

    return (dist, angle)


def assert_angle(x, y, angle):
    dist, ang = polar(x,y)
    try:
        assert(abs(angle - ang) < 0.1)
    except AssertionError:
        print("Expected <" + str(angle) + "> got <" + str(ang) + "> ")


if __name__=="__main__":
    assert_angle(-2, -2, -45)
    assert_angle(2, -2, 45)
    assert_angle(-2, 2, -135)
    assert_angle(2, 2, 135)

    assert_angle(2, -2 * sqrt(3), 30)
    assert_angle(2 * sqrt(3), -2, 60)

    assert_angle(2, 2 * sqrt(3), 120)
    assert_angle(2 * sqrt(3), 2, 150)

    assert_angle(-2, -2 * sqrt(3), -30)
    assert_angle(-2 * sqrt(3), -2, -60)

    assert_angle(-2, 2 * sqrt(3), -120)
    assert_angle(-2 * sqrt(3), 2, -150)