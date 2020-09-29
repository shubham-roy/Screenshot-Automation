# os module is used to create and delete empty folders and change directory
# shutil module is used to delete files of a folder and the folder
# glob module is used to generate paths
# cv2 module is used to handle images
import os, shutil, glob, cv2


#********************************************************************************************************
# This is a custom sort function that takes in an array containg complete address of the images and sorts it based on image-name. Employs selection sort since list size is very small i.e. around 1000
def customSort(namesList):

    n = len(namesList)
    for i in range(n):

        for j in range(i+1,n):

            i1_name = (namesList[i].split("\\")[7]).split('.')[0] # Getting name+extension from full address
            i2_name = (namesList[j].split("\\")[7]).split('.')[0] # Discarding extension
            
            if (int(i2_name) < int(i1_name)):
                namesList[i],namesList[j] = namesList[j],namesList[i]

    return namesList
#********************************************************************************************************


#********************************************************************************************************
# This function returns hamming distance of two integers
def hammingDist(num1,num2):

    dist = 0
    for i in range (63,-1,-1):

        bit1 = num1 & 1
        bit2 = num2 & 1

        if (bit1 != bit2):
            dist = dist + 1
        
        num1 = num1 >> 1
        num2 = num2 >> 1

    return dist
#********************************************************************************************************


#********************************************************************************************************
# This function gets the images from the folder to a list in sorted fashion
# Sorting is done based on name of image
# At last folder is deleted
def getImages():

    print('\n**************************************************************************************\n')
    directory = input("Enter the directory of images (Full Address): ") # address of folder where images are present
    print('\n**************************************************************************************\n')

    path = directory # stores address of folder
    directory = directory + '/*.png' # to consider all files ending with .png

    imagesPathName = [path for path in glob.glob(directory)] # get all image addresses
    imagesPathName = customSort(imagesPathName) # sorting of addresses
    
    images = [] # list

    # Populating the list
    for p in imagesPathName:
        image = cv2.imread(p)
        images.append(image)

    shutil.rmtree(path, ignore_errors=True) # deletes images in folder i.e empties the folder
    #os.rmdir(path) # deletes folder 

    return images
#********************************************************************************************************


#********************************************************************************************************
# This function converts original imageList to a newList that contains gray-scale 9X8 images
# Returns convertedList and originalList of images 
def convertedImages():

    imageList = getImages() # Get image-list
    newImageList = [] # new-list for converted images

    for image in imageList:

        newImage = cv2.resize(image,(9,8)) # change dimension to 9X8------->size has special significance
        newImage = cv2.cvtColor(newImage,cv2.COLOR_BGR2GRAY) # converting to gray-scale
        newImageList.append(newImage)

    return newImageList,imageList
#********************************************************************************************************


#********************************************************************************************************
# This function produces a list that contains dhashes of the images
# Returns hashList and originalList of images
def generateDHash():

    imageArray,originalList = convertedImages() # Get the modified images' list
    dHash = []

    # implementing dHash logic for each image
    for item in imageArray:
        
        # compute the (relative) horizontal gradient between adjacent column pixels
        diff = item[:, 1:] > item[:, :-1]
        # convert the difference image to a hash
        hashVal = sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])
        dHash.append(hashVal)

    return dHash,originalList # dHash contains integers between 0 and 2^64 - 1
#********************************************************************************************************


#********************************************************************************************************
# This funcions returns a list of duplicate images and originalList of images
def getDuplicateList():

    hashList,originalList = generateDHash()
    n = len(hashList)

    duplicates = []
    for i in range(n-1,-1,-1): # reverse iterating to keep the most recent image

        if i in duplicates:
            continue
        
        for j in range(i-1,-1,-1):

            if (i - j > 12): # compare images within 2 minutes duration
                break
        
            if j in duplicates:
                continue
        
            dist = hammingDist(hashList[j],hashList[i])
            if (dist <= 1 and j not in duplicates): # if hamming distance is less than 2 images are considered to be highly similar
                duplicates.append(j)

    return duplicates,originalList
#********************************************************************************************************


#********************************************************************************************************
# saves final images in a folder
def saveImages(finalImages):

    print('\n**************************************************************************************\n')
    folderName = input('Name (Only Name) Of The Folder To Be Created (To Save Final Images): ') # take user-input for name of the folder to be created
    print('\n**************************************************************************************\n')

    location = r"C:\Users\srwor\OneDrive\Pictures\Screenshots" # location where the folder is to be created......this can also be a user-input (here, not needed)
    path = os.path.join(location,folderName) # creation of the path

    try:  
    
        os.mkdir(path) # creation of folder
        
        os.chdir(path) # going inside the folder
        n = len(finalImages)
        
        for i in range(n):
            
            cv2.imwrite(str(i)+".png", finalImages[i]) # save images in the folder
    
    except OSError as error:  
    
        print('Folder Already Exists in the Directory')
        print(error)
#********************************************************************************************************


#********************************************************************************************************
# main function
def main():

    deleteList,originalList = getDuplicateList() # list of images to be deleted

    n = len(originalList)
    finalList = []

    # populating finalList
    for i in range(n):

        if i not in deleteList:
            finalList.append(originalList[i])
    
    saveImages(finalList) # saves the final images in a folder
#********************************************************************************************************


# calling main function        
if __name__ == "__main__":
    main()