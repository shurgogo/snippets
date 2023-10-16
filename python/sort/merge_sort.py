def merge_sort(a, start=0, end=None):
    if not end:
        end = len(a)
    mid = (start + end + 1) // 2
    if end - start > 1:
        merge_sort(a, start, mid)
        merge_sort(a, mid, end)
        i, j, left, right = 0, 0, a[start:mid], a[mid:end]
        while start < end:
            if (j >= len(right)) or (i < len(left) and left[i] < right[j]):
                a[start] = left[i]
                i += 1
            else:
                a[start] = right[j]
                j += 1
            start += 1


if __name__ == '__main__':
    l = [34, 57, 70, 19, 48, 2, 94, 7, 63, 75]
    merge_sort(l)
    print(l)
