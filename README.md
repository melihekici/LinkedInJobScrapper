# LinkedInJobScrapper
Script to scrap linkedin jobs

<h2>Job Scrapper for LinkedIn</h2>
<p>
  I have created an interface that is used to scrap linkedin jobs.
  The interface will give you a word cloud that shows which skills are required the most for searched job.
</p>
<p>
  The target jobs are development jobs in general.
  The skills that are going to be search through the job posts are given in a hard-coded dictionary.
</p>
<p>
  Inside the source code, we are accesing the job information at some point and i am extracting the required skills information from the job posts.
  If you need to extract some other information from the job description, you can edit the code and achieve want you want.
</p>

<p>
  You need to have Chrome and Chrome web driver to be able to use this tool.
  The setup.py file will automatically install required libraries.
  Setup.py will also attemp to find your Chrome version and download the compatible chrome driver for you.
  Note: If setup.py fails to locate and get your chrome version information, then you will have to download it manually. In this scenario, you need to put your chromedriver.exe inside the same folder where setup.py and JobScrapper.py is.
</p>

<p>
  You can reach out to me for feedbacks and suggestions from melih.ekici4@gmail.com
</p>
