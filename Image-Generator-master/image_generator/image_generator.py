import customtkinter as ctk
import tkinter as tk
import os 
import openai
from PIL import Image,ImageTk
import requests,io
def generate_image():

    openai.api_key=os.getenv('OPENAI_API_KEY')
    user_prompt=prompt_entry.get("0.0",tk.END)
    user_prompt+="in style: "+style_dropdown.get()
    response=openai.Image.create(
    prompt=user_prompt,
    n=int(number_range.get()),
    size="512x512"
)
    image_url=[]
    for i in range(len(response['data'])):
        image_url.append(response['data'][i]['url'])
    print(image_url)

    images=[]
    for url in image_url:
        response=requests.get(url)
        image=Image.open(io.BytesIO(response.content))
        photo_image=ImageTk.PhotoImage(image)
        images.append(photo_image)

    def update_photo_image(index=0):
        canvas.image=images[index]
        canvas.create_image(0,0,anchor="nw",image=images[index])
        index=(index+1) % len(images)
        canvas.after(3000,update_photo_image,index)
    update_photo_image()        
root=ctk.CTk()
# * window
root.title("Image Generator Project")
ctk.set_appearance_mode("dark")
# * The box that holds the values
input_frame=ctk.CTkFrame(root)
input_frame.pack(side="left",expand=True,padx=20,pady=20)
#*promt value and its text box
prompt_label=ctk.CTkLabel(input_frame,text="Prompt")
prompt_label.grid(row=0,column=0,padx=10,pady=10)
prompt_entry=ctk.CTkTextbox(input_frame,height=10)
prompt_entry.grid(row=0,column=1,padx=10,pady=10)
#*style label and its dropdown
style_label=ctk.CTkLabel(input_frame,text="Style")
style_label.grid(row=1,column=0,padx=10,pady=10)
style_dropdown=ctk.CTkComboBox(input_frame,values=["Realistic","Cartoon","3D","Flat Art"])
style_dropdown.grid(row=1,column=1,padx=10,pady=10)
#*number of images and its range
number_label=ctk.CTkLabel(input_frame,text="Img no.")
number_label.grid(row=2,column=0,padx=10,pady=10)
number_range=ctk.CTkSlider(input_frame,from_=1,to=10,number_of_steps=9)
number_range.grid(row=2,column=1)
#*generate button
button_generate=ctk.CTkButton(input_frame,text="Generate",command=generate_image)
button_generate.grid(row=3,column=0,columnspan=2,sticky="news",padx=10,pady=10)
#* canvas
canvas=tk.Canvas(root,width=512,height=512)
canvas.pack(side="left")
root.mainloop()
