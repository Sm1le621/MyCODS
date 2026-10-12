def findSmallest(arr):
  smallest = arr[0]
  small_index = 0
  for i in range(1, len(arr)):
    if arr[i] < smallest:
      smallest = arr[i]
      small_index = i
  return small_index

def SelectionSort(arr):
  newArr = []
  for i in range(len(arr)):
    smallest = findSmallest(arr)
    newArr.append(arr.pop(smallest))
  return newArr

print(SelectionSort([90, 15, 1, 5, 20, 10]))