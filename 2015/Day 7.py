from Functions import get_input
from collections import deque


def get_wires():
    wire_strings = get_input('line')
    deq = deque()
    for wire in wire_strings:
        deq.append(wire)
    return deq


def can_wire_run(wire, outputs):
    if 'AND' in wire:
        left, right = wire.split(' -> ')
        a, b = left.split(' AND ')
        if a.isdigit() and b.isdigit():
            outputs[right] = int(a) & int(b)
            return True
        if a.isdigit() and b in outputs:
            outputs[right] = int(a) & outputs[b]
            return True
        if b.isdigit() and a in outputs:
            outputs[right] = outputs[a] & int(b)
            return True
        if a in outputs and b in outputs:
            outputs[right] = outputs[a] & outputs[b]
            return True

    elif 'OR' in wire:
        left, right = wire.split(' -> ')
        a, b = left.split(' OR ')
        if a.isdigit() and b.isdigit():
            outputs[right] = int(a) | int(b)
            return True
        if a.isdigit() and b in outputs:
            outputs[right] = int(a) | outputs[b]
            return True
        if b.isdigit() and a in outputs:
            outputs[right] = outputs[a] | int(b)
            return True
        if a in outputs and b in outputs:
            outputs[right] = outputs[a] | outputs[b]
            return True


    elif 'LSHIFT' in wire:
        left, right = wire.split(' -> ')
        a, b = left.split(' LSHIFT ')
        if a.isdigit() and b.isdigit():
            outputs[right] = int(a) << int(b)
            return True
        if a.isdigit() and b in outputs:
            outputs[right] = int(a) << outputs[b]
            return True
        if b.isdigit() and a in outputs:
            outputs[right] = outputs[a] << int(b)
            return True
        if a in outputs and b in outputs:
            outputs[right] = outputs[a] << outputs[b]
            return True


    elif 'RSHIFT' in wire:
        left, right = wire.split(' -> ')
        a, b = left.split(' RSHIFT ')
        if a.isdigit() and b.isdigit():
            outputs[right] = int(a) >> int(b)
            return True
        if a.isdigit() and b in outputs:
            outputs[right] = a >> outputs[b]
            return True
        if b.isdigit() and a in outputs:
            outputs[right] = outputs[a] >> int(b)
            return True
        if a in outputs and b in outputs:
            outputs[right] = outputs[a] >> outputs[b]
            return True



    elif 'NOT' in wire:
        left, right = wire.split(' -> ')
        a = left[4:]
        if a.isdigit():
            outputs[right] = ~int(a)
            return True
        if a in outputs:
            outputs[right] = ~outputs[a]
            return True
        return False

    else:
        left, right = wire.split(' -> ')
        if left.isdigit():
            outputs[right] = int(left)
            return True
        if left in outputs:
            outputs[right] = outputs[left]
            return True
    return False


def main(part):
    wire_deq = get_wires()
    outputs = dict()

    # Rotate through the deque until it is empty
    while len(wire_deq) > 0:
        wire = wire_deq[0]
        if can_wire_run(wire, outputs):
            wire_deq.popleft()
        else:
            wire_deq.rotate()

    answer_p1 = outputs['a']
    print(f"Part 1 answer is {answer_p1}")


main(1)
