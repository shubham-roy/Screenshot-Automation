import  os, time, pyautogui

def createFolder():
    
    folderName = input('Name Of The Folder To Be Created: ') # take user-input for name of the folder to be created
    
    location = r"C:\Users\srwor\OneDrive\Pictures\Screenshots" # location where the folder is to be created......this can also be a user-input (here, not needed)

    path = os.path.join(location,folderName) # creation of the path

    try:  
    
        os.mkdir(path) # creation of folder
        return path # returns path of folder
    
    except OSError as error:  
    
        print('Folder Already Exists in the Directory')
   


def capture(path,i):

    print (path)
    # path-creation for saving
    name = r'\image' + str(i) + '.png'
    print(name)
    dest = path + name
    print(dest)
    # ..............    

    # take screenshot using pyautogui 
    image = pyautogui.screenshot()

    # saving
    image.save(dest)

     
def main():

    image_folder = createFolder()
    i = 0

    while 1:
        i = i + 1
        capture(image_folder,i)
        time.sleep(5)

if __name__ == "__main__":
    main()    

