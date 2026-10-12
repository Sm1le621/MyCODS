def binary_search(list, item):
  low = 0
  high = len(list) - 1

  while low <= high:
    mid = (low + high)//2
    guess = list[mid]
    if guess == item:
      return mid
    if guess > item:
      high = mid - 1
    else:
      low = mid + 1
  return None

my_list = [1, 3, 6, 9, 18, 32, 64, 128, 254]

print(f"Index: {binary_search(my_list, 128)}")