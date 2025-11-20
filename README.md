# Meme Generator API

## 1) Executive Summary
**Problem:** The problem my project is solving is not having access to a website that generates and creates quick simple memes for you out of any pictures and text you want.  
**Solution:** A Flask API that I have created lets users upload whatever picture they want as well as add any text that they want to the picture. Then when you upload the meme, my meme generator will output the very simple and quick meme for you to use. My project can be run through Apptainer with exactly what you need to run it properly given below in the README. You can copy and run that text in a terminal for the link to be given to you, when you click on the link an open it in a browser, at the end of the URL you will need to add the word 'upload' and then when you click enter the meme generator will be there for you to use.

## 2) System Overview
**Course Concept:** Azure Blob Storage + Flask API.  
**Architecture Diagram:** See `/assets/architecture.png`.
I also have screenshots to show that my project works in assets!

**Data / Services:**
- Images: PNG/JPG files uploaded by users.
- Text overlays: Added via PIL.
- Storage: Azure Blob `images-demo` container (public-read).

## 3) How to Run (Local)
**Apptainer:**

```bash
Apptainer


module load apptainer/1.3.4
apptainer run --bind /home/$USER:/home/$USER /home/grh2uv/meme-generator/meme-generator.sif


##Then when you run all of that after you open the link in a browser, make sure to add the word 'upload' to the end of the link so you can see the correct form to the meme generator.
