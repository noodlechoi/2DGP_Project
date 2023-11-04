objects = [[] for _ in range(4)]

WIDTH = 900
HEIGHT = 800

def add_object(o, depth = 0):
    objects[depth].append(o)

def add_objects(ol, depth = 0):
    objects[depth] += ol


def update():
    for layer in objects:
        for o in layer:
            o.update()


def render():
    for layer in objects:
        for o in layer:
            o.draw()


def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in objects:
        layer.clear()
    pass

# list 받아서 사각형과 점의 충돌을 체크하는 함수
def isConflict(rec_location, size_list, point):
    min = [rec_location[0] - size_list[0] // 2, rec_location[1] - size_list[1] // 2]
    max = [rec_location[0] + size_list[0] // 2, rec_location[1] + size_list[1] // 2]

    if (point[0] > min[0]) and (point[0] < max[0]) and (point[1] > min[1]) and (point[1] < max[1]):
        return True

    return False
    pass