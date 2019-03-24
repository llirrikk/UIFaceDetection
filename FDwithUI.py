from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import cv2
from os import chdir, mkdir, path, listdir
from PIL import Image, ImageTk

root = Tk()
root.title("Обнаружение лиц на изображении")

cascPath = "haarcascade.xml"
faceCascade = cv2.CascadeClassifier(cascPath)


def check(pathtoimg, faces):
    image = cv2.imread(pathtoimg)  # убрать квадраты
    filename = path.splitext(pathtoimg)[0]
    mkdir(filename + "_output")
    i = 0
    for (x, y, w, h) in faces:
        sub_img = image[y: y + h, x: x + w]
        i = i + 1
        chdir(filename + "_output")
        cv2.imwrite(str(i) + ".jpg", sub_img)
        chdir("../")
        int(i)
    print("Saved!")


def end(root2):
    root2.flag = False
    root2.destroy()


def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None  # initialize the dimensions of the image to be resized and grab the image size
    (h, w) = image.shape[:2]

    if width is None and height is None:  # if both the width and height are None, then return the original image
        return image
    if width is None:  # check to see if the width is None
        r = height / float(h)  # calculate the ratio of the height and construct the dimensions
        dim = (int(w*r), height)
    else:  # otherwise, the height is None
        r = width / float(w)  # calculate the ratio of the width and construct the dimensions
        dim = (width, int(h*r))

    resized = cv2.resize(image, dim, interpolation=inter)  # resize the image
    return resized  # return the resized image


def button_fullpath():
    global replace
    fullpathtoimg = fd.askopenfilenames()

    count = 0
    for i in str(fullpathtoimg):
        if i == "'":
            count += 1
    count = int(count / 2)
    print(fullpathtoimg)
    print("images uploaded: ", count)

    if count > 1:
        replace = str(fullpathtoimg)\
            .replace("('", "")\
            .replace("', '", "@")\
            .replace("')", "")

    elif count == 1:
        replace = str(fullpathtoimg)\
            .replace("('", "")\
            .replace("',)", "")

    split = str(replace).split("@")  # splitpath
    i = 0
    for current in split:
        i += 1
        print(i, "/", count, " image: ", current)
        pathtoimg = current

        extension = pathtoimg[-4:].lower()

        if extension != ".jpg" and extension != ".png" and extension != "jpeg":
            mb.showerror("Ошибка", "Должно быть выбрано изображение")
        else:
            image = cv2.imread(pathtoimg)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            root2 = Toplevel(root)

            image = image_resize(image, height=700, width=1000)

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)

            Label(root2, image=image, height=700, width=1000).pack(side=TOP)
            Button(root2, text="Сохранить лица", width=50, height=100, font=("Times", "15"), command=lambda: check(pathtoimg, faces)).pack(side=BOTTOM)

            root2.protocol('WM_DELETE_WINDOW', lambda: end(root2))

            root2.flag = True
            while root2.flag:
                root2.update()


def exit():
    raise SystemExit()


btnselect = Label(text="Выбрать изображение", width=30, height=2, font=("Times", 16))
btnye = Label(text="Хаар каскад обнаружен!", height=1, fg="#228B22")
btnno = Label(text="Хаар каскад НЕ обнаружен!", height=2, width=45, fg="#8B0000")
btndetect = Button(text="Обнаружить", width=30, command=button_fullpath, font="Times")
btnexit = Button(text="Закрыть", width=10, command=exit, font="Times")

filelist = listdir()
if any(str(cascPath) in i for i in filelist):
    btnye.grid(columnspan=2)
    btnselect.grid(columnspan=2)
    btndetect.grid(column=1, row=3)
    btnexit.grid(column=0, row=3)
else:
    btnno.grid(columnspan=3)

root.resizable(False, False)
root.mainloop()
