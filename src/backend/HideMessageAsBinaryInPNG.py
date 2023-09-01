# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 18:20:59 2023

@author: TheKekening
"""

import PIL
from PIL import Image


def pixelise(ImgPath: str):
    PixelDict = {}
    with Image.open(ImgPath) as im:
        px=im.load()
        ImgSize = im.size
        for LineNum in range(ImgSize[1]):
            LineList = []
            for ColNum in range(ImgSize[0]):
                NewPixel = px[ColNum,LineNum]
                LineList.append(NewPixel)
            PixelDict[f"{LineNum}"] = LineList
    return PixelDict

def DictContract(PixelDict):
    NewList = []
    for i in PixelDict:
        NewList = NewList + i
    return NewList

def AlphaImg(ImgPath: str, OutPath: str):
    with Image.open(ImgPath) as im:
        NewImg = PIL.Image.new("RGBA", im.size, None)
        OldImg = im.crop((0,0)+(im.size))
        NewImg.paste(OldImg, (0,0))
    NewImg.save(OutPath)
    return 
    
def StrToList(SecretMsg:str):
    OutList = []
    for i in SecretMsg:
        mid = str(bin(ord(i)))
        final = mid.replace("0b","")
        while len(final) != 8:
            final = "0"+final
        OutList.append(final)
    return OutList

def HideMsg(ImgPath:str, SecretMsg:str, OutPath:str):
    BinMsg = StrToList(SecretMsg)
    PixHorNum = 0
    PixVerNum = 0  
    AlphaImg(ImgPath, OutPath)
    PixelNum = 0
    with Image.open(OutPath) as im:
        px = im.load()
        ImgSize = (im.size[0]*im.size[1])
        IterationNumber = ImgSize // 8
        if IterationNumber < len(BinMsg):
            return "Image too small to encode message"
        for i in range(len(BinMsg)):
            for j in range(len(BinMsg[i])):
                print(f"{PixHorNum =}")
                print(f"{PixVerNum =}")
                print(f"{PixelNum =}")
                if PixHorNum > im.size[0]-1:
                    PixHorNum = 0
                    PixVerNum = PixVerNum + 1
                SelPixel = px[PixHorNum,PixVerNum]
                print(f"{i =}")
                print(f"{j =}")
                if int(BinMsg[i][j]) == 1:
                    RValue = SelPixel[0]
                    GValue = SelPixel[1]
                    BValue = SelPixel[2]
                    px[PixHorNum,PixVerNum] = (RValue,GValue,BValue,254)
                print(px[PixHorNum,PixVerNum])
                PixHorNum = PixHorNum + 1
                PixelNum = PixelNum + 1
                
        im.save(OutPath)
    return "done"

def DecryptImg(ImgPath:str):
    PixelDict = pixelise(ImgPath)
    DecodedBin = []
    for i in range(len(PixelDict)):
        for j in PixelDict[str(i)]:
            if j[3] == 254:
                DecodedBin.append(1)
            elif j[3] == 255:
                DecodedBin.append(0)
    j = 0
    print(DecodedBin)
    Bytelist=[]
    while "".join(map(str,DecodedBin[j:j+8])) != "00000000" and "".join(map(str,DecodedBin[j:j+8])) !="":
        Bytelist.append(DecodedBin[j:j+8])
        j=j+8
        print("".join(map(str,DecodedBin[j:j+8])))
    NewStrList=[]
    for i in range(len(Bytelist)):
        SelectedByte = "".join(map(str,Bytelist[i]))
        NewStrList.append(chr(int(SelectedByte,2)))

    return "".join(NewStrList)