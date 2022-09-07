router.post("/image", status_code=status.HTTP_201_CREATED)
async def post_image(request: Request,file: UploadFile=File(...),get_current_user: int = Depends(oauth.get_current_user)):
    url = 'https://api-2445582032290.production.gw.apicast.io/v1/foodrecognition?user_key=6d44fe497a4a4733bb0b86014d64ee42'
    contents = await file.read()
    file_copy = NamedTemporaryFile('wb', delete=False)
    f,newstream,outfile,resp = None,None,None,None
    #headers={"Content-Type" :"image/jpeg"
    #            ,"Accept-Encoding": "gzip"
    #        }
    foodai=utils.FoodAI()
    foodai.connect()

    try:
        # The 'with' block ensures that the file closes and data are stored
        with file_copy as f:
            f.write(contents);

        # Here, upload the file to your S3 service
        # You can reopen the file as many times as desired.
        # old testing 1
        #img = {'media': open(file_copy.name, 'rb')}
        img=open(file_copy.name, 'rb')
        img=io.BytesIO(img.read())
        img=Image.open(img).resize((544,544))
        outfile=io.BytesIO()
        img.save(outfile,"jpeg",quality=100)
        #testing httpx resize
        #newstream=io.BytesIO(contents)
        #img=Image.open(newstream).resize((544,544))
        #outfile=io.BytesIO()
        #img.save(outfile,"jpeg",quality=100)
        #final_img=outfile.getvalue()
        #resp=foodai.recognize(outfile)
        resp=foodai.recognize(outfile.getvalue())


#        resp = requests.post(url=url, files=img,headers=headers)
        print(resp)

    finally:
        if f is not None:
            f.close() # Remember to close any file instances before removing the temp file
        if newstream is not None:
            newstream.close()
        if outfile is not None:
            outfile.close()
        os.unlink(file_copy.name)  # unlink (remove) the file from the system's Temp folder

    # Handle file contents as desired
    # print(contents)
    #print(await request.form())
    #with open(f'{file.filename}','wb') as buffer:
        #print(file.file.read())
        #contents = await file.read()
        #temp_file = BytesIO()
        #temp_file.write(contents)
        #temp_file.seek(0)
        #shutil.copyfileobj(file.file,buffer)
        #os.system(f"mpv {file.file.read()}")

#    return {"file_name": file.filename }
    return resp
