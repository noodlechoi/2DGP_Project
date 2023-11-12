objects = [[] for _ in range(4)]
collision_pairs = {}

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


# fill here


def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in objects:
        layer.clear()



# fill here
def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        print(f'Added new group {group}')
        collision_pairs[group] = [ [], [] ]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)




def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)

# list 받아서 사각형과 점의 충돌을 체크하는 함수
def isConflict(rec_location, size_list, point):
    min = [rec_location[0] - size_list[0] // 2, rec_location[1] - size_list[1] // 2]
    max = [rec_location[0] + size_list[0] // 2, rec_location[1] + size_list[1] // 2]

    if (point[0] > min[0]) and (point[0] < max[0]) and (point[1] > min[1]) and (point[1] < max[1]):
        return True

    return False
    pass

# 두 점 사이에 따라 음수나 양수 반환 함수 : 움직여야하는 좌표 p1 (기준)
def directtion(p1, p2):
    if (p1[0] - p2[0]) == 0:
        if (p1[1] - p2[1]) == 0:
            return [0, 0]
        else:
            return [0, (p1[1] - p2[1]) // abs(p1[1] - p2[1])]
    elif (p1[1] - p2[1]) == 0:
        if  (p1[0] - p2[0]) == 0:
            return [0, 0]
        else:
            return [(p1[0] - p2[0]) // abs(p1[0] - p2[0]), 0]


    return [(p1[0] - p2[0]) // abs(p1[0] - p2[0]), (p1[1] - p2[1]) // abs(p1[1] - p2[1])]