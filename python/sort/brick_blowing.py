# mit 6.006 ps02-4


def get_damages(H):
    """
    Input:  H | list of bricks per house from west to east
    Output: D | list of damage per house from west to east
    """
    D = [1 for _ in H]
    X = [(H[i], i) for i in range(0, len(H))]

    def merge_sort(a, start=0, end=None):
        if not end:
            end = len(a)
        mid = (start + end + 1) // 2
        if end - start > 1:
            merge_sort(a, start, mid)
            merge_sort(a, mid, end)
            i, j, left, right = 0, 0, a[start:mid], a[mid:end]
            while start < end:
                if (j >= len(right)) or (i < len(left) and left[i][0] < right[j][0]):
                    D[left[i][1]] += j
                    a[start] = left[i]
                    i += 1
                else:
                    a[start] = right[j]
                    j += 1
                start += 1
    merge_sort(X)
    return D


if __name__ == '__main__':
    height = [34, 57, 70, 19, 48, 2, 94, 7, 63, 75]
    damage = get_damages(height)
    print(damage) # [4, 5, 6, 3, 3, 1, 4, 1, 1, 1]
