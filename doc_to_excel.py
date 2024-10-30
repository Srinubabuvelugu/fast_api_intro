import pandas as pd
lines = []
with open('file.txt','r') as f:
    lines = f.readlines()
# print(lines[:20])
questions=[]
a=[]
b=[]
c=[]
d=[]
answers =[]
for i in range(0,len(lines),6):
    try:
        questions.append(lines[i][:-1])
        a.append(lines[i+1][2:-1])
        b.append(lines[i+2][2:-1])
        c.append(lines[i+3][2:-1])
        d.append(lines[i+4][2:-1])
        answers.append(lines[i+5][8:-1])
    except Exception as e:
        print(e)
# print(questions)

data = pd.DataFrame(
    {"Qustion":questions,
    "Option1":a,
    "Option2":b,
    "Option3":c,	
    "Option4":d,
    "Answer":answers}	
)
# print(data.head(10),True)
data.to_excel("css_100_mcqs.xlsx")