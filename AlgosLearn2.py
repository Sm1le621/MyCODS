class File:
  def __init__(self, name, size):
    self.name = name
    self.size = size

class Folder:
  def __init__(self, name):
    self.name = name
    self.files = []
    self.subfolders = []

  def add_file(self, file):
    return self.files.append(file)

  def add_folder(self, folder):
    return self.subfolders.append(folder)

  def get_total_size(self):
    count = 0
    for i in self.files:
      count += i.size
      
    for j in self.subfolders:
      count += j.get_total_size()
      
    return count
    
if __name__ == "__main__":
  photo = File("photo.png", 50)
  txt = File("MyNode.txt", 25)
  images = Folder("Images")
  root = Folder("Root")

  images.add_file(photo)
  root.add_file(txt)
  root.add_folder(images)

  print(root.get_total_size())