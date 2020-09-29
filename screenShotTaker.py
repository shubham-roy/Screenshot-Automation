# os module helps us in creating folders at desired locations
# time module helps us in making the machine wait for t sec before capturing the next screenshot
# pyautogui helps in taking screenshots
import  os, time, pyautogui


#********************************************************************************************************
# creates a new folder and returns its address
def createFolder():
    
    folderName = input('Name Of The Folder To Be Created: ') # take user-input for name of the folder to be created
    
    location = r"C:\Users\srwor\OneDrive\Pictures\Screenshots" # location where the folder is to be created......this can also be a user-input (here, not needed)

    path = os.path.join(location,folderName) # creation of the path

    try:  
    
        os.mkdir(path) # creation of folder
        return path # returns path of folder
    
    except OSError as error:  
    
        print('Folder Already Exists in the Directory')
        print(error)
#********************************************************************************************************   

#********************************************************************************************************
# takes screenshot and saves it in given folder
# Arguments: 1) Address of folder  2) image-index for saving purpose
def capture(path,i):

    # path-creation for saving
    name = '\\' + str(i) + '.png' # example of sample name = '\3.png'
    dest = path + name # creation of complete address
    # ..............    

    # take screenshot using pyautogui 
    image = pyautogui.screenshot()

    # saving
    image.save(dest)
#********************************************************************************************************


#********************************************************************************************************
# main function     
def main():

    image_folder = createFolder() # gets the address of the folder
    i = -1 # numbering-purpose while saving image

    while 1:
        i = i + 1
        capture(image_folder,i)
        time.sleep(10) # for wait purpose
#********************************************************************************************************


# script initializes with the main() function call
if __name__ == "__main__":
    main()    

