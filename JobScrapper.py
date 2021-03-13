import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from Scrappers.LinkedInScrapper import LinkedInScrapper
from tkinter import *
import threading

def cloudFromDict(dictionary, outFileName="RequiredSkills"): # Creates a word cloud from a dictionary, saves it and opens it
    wc = WordCloud(background_color="white",width=2000,height=1000, max_words=10,relative_scaling=.8,normalize_plurals=False).generate_from_frequencies(dictionary)
    wc.to_file(outFileName + ".jpg")
    #ax1 = fig.axes(frameon=False)
    #ax1.axes.get_xaxis().set_visible(False)
    #ax1.axes.get_yaxis().set_visible(False)
    #plt.imshow(wc)
    #plt.savefig(outFileName + ".jpg")
    os.startfile(outFileName + ".jpg")

def filterOutNonFrequentSkills(dictionary, numJobs): # Filters out the skills. Skills that are asked by more than 10% of the job postings are shown
    filtered_skills = {} # Starting from empty dictionary for filtered skills
    values_list = [v[1] for v in dictionary.values()] # Extracting values from dictionary that is passed as parameter
    for i in range(len(dictionary.keys())): # For each key in dictionary
        if(values_list[i] / numJobs > 0.1): # If the key(skill) is mentioned more than 10% of the jobs
            filtered_skills[list(dictionary.keys())[i]] = values_list[i] # Then add this skill to the filtered_skills dictionary
    return filtered_skills 

def scrap(): # Does the scrapping
    global job_entry, location_entry, counter_label, scrap_button
    try:
        scrap_button.config(state="disabled") # Disable the scrap button while scrapping is allready in progress
        job_to_be_searched = job_entry.get() # Get the job information from interface
        job_location = location_entry.get() # Get the location information from interface
        linkedInScrapper = LinkedInScrapper(job_to_be_searched, job_location) # Initialize an instance of LinkedInScrapper class
        
        # These are the skills are we are searching for on a job post. The dictionar key here is the skill name that will be shown on word cloud
        # And the skills on the values side inside the list are the synonyms for that key, 0 at the end is the counter that will keep # of job postings
        # that mention this skill.
        skills = {'java' : [[' java '], 0], 'sql' : [[' sql ', ' nosql '], 0], 'spring':[[' spring '], 0], 'c#':[[' c# '], 0], 'unity':[[' unity ', ' unity2d ', ' unity3d '], 0], 'aws': [[' aws ', ' amazon web services '], 0], 'jupyter':[[' jupyter '], 0], 'azure':[[' azure '],0], 'docker':[[' docker '], 0], 'git':[[' git ', ' github ', ' version control systems '],0], 'kotlin':[[' kotlin '], 0], 'android studio':[[' android studio ', ' android development '], 0], 'swift':[[' swift '], 0], 'javascript':[[' javascript '], 0], 'c':[[' c ', ' c/c++ '], 0], 'c++':[['c++', ' c/c++ '], 0], 'lua':[[' lua '], 0], 'unreal engine':[[' unreal engine '], 0], 'keras':[[' keras '], 0], 'tensorflow':[[' tensorflow '], 0], 'pytorch':[[' pytorch '], 0], 'objective-c':[[' objective-c ', ' objective c '], 0], 'ruby':[[' ruby '] , 0], 'seaborn':[[' seaborn '], 0], 'html':[[' html ', ' html5 '], 0], 'css':[[' css ', ' css3 '], 0], 'php':[['php'], 0], 'python':[[' python ', ' python3 '], 0], ' spark ':[[' spark '], 0], 'powerbi':[[' powerbi ', ' power-bi '],0]}
        skills, numJobs = linkedInScrapper.scrapSkills(skills, counter_label) # Scrapping the skills and keeping total # of jobs as well to filter non-frequent skills
        cloudFromDict(filterOutNonFrequentSkills(skills, numJobs), job_to_be_searched) # Filters out rarely asked skills
        scrap_button.config(state="normal") # Make scrap button clickable again
        messagebox.showinfo(title="Tamamlandı", message=f"Scrap işlemi tamamlandı. Gerekli yetenekler {job_to_be_searched}.jpg olarak kaydedildi.")
    except Exception as e: # In case of an error occurs
        if("division by zero" in str(e)):
            messagebox.showerror(title="Hata", message="Arama için iş ilanı bulunamadı.")
        print(str(e)) # print error massage for debug purposes
        scrap_button.config(state="normal") # Unlock scrap button

def scrapPrep(): # Calls scrap() on a new thread
    t=threading.Thread(target=scrap)
    t.start()

# User Interface
root = Tk()
root.geometry("600x300")
root.title("Skills Scrapper from LinkedIn Jobs")
Label(root, text = "Job to be searched").place(x=100, y=50)
Label(root, text = "Location").place(x=400, y=50)
job_entry = Entry(root, "", width = 20)
job_entry.place(x=90, y=75)
location_entry = Entry(root, "", width= 20)
location_entry.place(x=370, y=75)
scrap_button = Button(root, text="Scrap", font="Verdana 12",width = 10, command=scrapPrep)
scrap_button.place(x=235, y=110)
counter_label = Label(root, text = "/", font = "Verdana 12")
counter_label.place(x=270, y=200)

root.mainloop()

