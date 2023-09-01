# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 18:20:59 2023

@author: TheKekening
"""

import PIL
from PIL import Image


def pixelise(ImgPath: str) -> dict:
    """
    Convert the image to dictionary of pixel.

    Parameters
    ----------
    ImgPath : str
        Input Image Path.
    Returns
    -------
    PixelDict : Dict
        Returns Dictionary where each Line represents a row of pixels,
        the colour codes of these pixels are recorded in the dict.
    """
    PixelDict = {}
    with Image.open(ImgPath) as im:
        px = im.load()
        ImgSize = im.size
        for LineNum in range(ImgSize[1]):
            LineList = [0] * ImgSize[0]
            for ColNum in range(ImgSize[0]):
                NewPixel = px[ColNum, LineNum]
                LineList[ColNum] = NewPixel
            PixelDict[f"{LineNum}"] = LineList
    return PixelDict


def DictContract(PixelDict):  # noqa: D103
    NewList = []
    for i in PixelDict:
        NewList = NewList + i
    return NewList


def AlphaImg(ImgPath: str, OutPath: str):
    """Convert normal RGB image to RGBA so it contain alpha channel for modifying purpose."""
    with Image.open(ImgPath) as im:
        NewImg = PIL.Image.new("RGBA", im.size, None)
        OldImg = im.crop((0, 0) + (im.size))
        NewImg.paste(OldImg, (0, 0))
    NewImg.save(OutPath)
    return


def StrToList(SecretMsg: str):
    """Converting string of secret message to binary format."""
    OutList = ["0"] * len(SecretMsg)
    for i, a in enumerate(SecretMsg):
        mid = str(bin(ord(a)))
        final = mid.replace("0b", "")
        if len(final) != 8:
            final = "0" * (8 - len(final)) + final
        OutList[i] = final
    return OutList


def HideMsg(ImgPath: str, SecretMsg: str, OutPath: str):
    """
    Hide secret message to an image which can be decode with HideMsg

    Parameters
    ----------
    ImgPath : str
        Input Image Path.
    SecretMsg: str
        The secret message.
    OutPath: str
        Output Inamge Path.
    """
    BinMsg = StrToList(SecretMsg)
    PixHorNum = 0
    PixVerNum = 0
    AlphaImg(ImgPath, OutPath)
    PixelNum = 0
    with Image.open(OutPath) as im:
        px = im.load()
        ImgSize = (im.size[0] * im.size[1])
        IterationNumber = ImgSize // 8
        if IterationNumber < len(BinMsg):
            return "Image too small to encode message"
        for i in range(len(BinMsg)):
            for j in range(len(BinMsg[i])):
                # print(f"{PixHorNum =}")
                # print(f"{PixVerNum =}")
                # print(f"{PixelNum =}")
                if PixHorNum > im.size[0] - 1:
                    PixHorNum = 0
                    PixVerNum = PixVerNum + 1
                SelPixel = px[PixHorNum, PixVerNum]
                # print(f"{i =}")
                # print(f"{j =}")
                if int(BinMsg[i][j]) == 1:
                    RValue = SelPixel[0]
                    GValue = SelPixel[1]
                    BValue = SelPixel[2]
                    px[PixHorNum, PixVerNum] = (RValue, GValue, BValue, 254)
                # print(px[PixHorNum,PixVerNum])
                PixHorNum = PixHorNum + 1
                PixelNum = PixelNum + 1

        im.save(OutPath)
    return "done"


def DecryptImg(ImgPath: str) -> str:
    """
    Retrieve the Secret Message from the encoded image

    Parameters
    ----------
    ImgPath : str
        Input Image Path.
    Returns
    -------
    SecretMsg : str
        Return string hidden in the image from HideMsg
    """
    PixelDict = pixelise(ImgPath)
    DecodedBin = []
    for i in range(len(PixelDict)):
        for j in PixelDict[str(i)]:
            if j[3] == 254:
                DecodedBin.append(1)
            elif j[3] == 255:
                DecodedBin.append(0)
    j = 0
    # print(DecodedBin)
    Bytelist = []
    while "".join(map(str, DecodedBin[j:j + 8])) != "00000000" and "".join(map(str, DecodedBin[j:j + 8])) != "":
        Bytelist.append(DecodedBin[j:j + 8])
        j = j + 8
        # print("".join(map(str,DecodedBin[j:j+8])))
    NewStrList = ['0'] * len(Bytelist)
    for i in range(len(Bytelist)):
        SelectedByte = "".join(map(str, Bytelist[i]))
        NewStrList[i] = chr(int(SelectedByte, 2))

    return "".join(NewStrList)
