#!/usr/bin/env python


import sys
import os
import zlib
import Image
import StringIO

from pdfrw import PdfReader, PdfDict, PdfArray, PdfName, PdfWriter

def process_image(image):
    #if image.get("/Mask"):
    #    del(image["/Mask"])
    #if image.get("/SMask"):
    #    del(image["/SMask"])
    #if image.get("/ImageMask"):
    #    del(image["/ImageMask"])
    #    image["/Width"] = 1
    #    image["/Height"] = 1
    #    image["/Filter"] = PdfName("FlateDecode")
    #    imgdata = Image.open("empty.jpg")
    #    image.stream = zlib.compress(imgdata.tostring())
    #print image
    if image["/Filter"] == PdfName("FlateDecode"):
        pass
    elif image["/Filter"] == PdfName("DCTDecode"):
        im = Image.open(StringIO.StringIO(image.stream))
        outf = StringIO.StringIO()
        im.save(outf, "JPEG", quality=45)
        image.stream = outf.getvalue()
        outf.close()
        #image["/Filter"] = PdfName("FlateDecode")
        #image.stream = zlib.compress(im.tostring())

def find_images(obj, visited=set()):
    if not isinstance(obj, (PdfDict, PdfArray)):
        return

    # Don't get stuck in an infinite loop
    myid = id(obj)
    if myid in visited:
        return
    visited.add(myid)

    if isinstance(obj, PdfDict):
        if obj.Type == PdfName.XObject and obj.Subtype == PdfName.Image:
            process_image(obj)
        obj = obj.itervalues()

    for item in obj:
        find_images(item, visited)

if __name__ == '__main__':
    inpfn,outfn = sys.argv[1:]
    reader = PdfReader(inpfn)
    find_images(reader)
    PdfWriter().addpages(reader.pages).write(outfn)
