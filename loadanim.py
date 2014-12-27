lines = 3
speed = 0.08
width = 41
def genAnim():
    moves=[
"""
   
|"|
""",
"""
   
/"|
""",
"""
_  
 "|
""",
"""
\  
 "|
""",
"""
 | 
 ? 
""",
"""
  /
|" 
""",
"""
  _
|" 
""",
"""
   
|"\\
"""
]
    m=0
    result=[]
    steps=0
    for i in range(0,8*20+1):
        spaceFirst= ""
        spaceLast= ""
        if m==4:
            steps=steps+2
        for j in range(0, steps):
            spaceFirst+= " "
        for j in range(0, 41-steps):
            spaceLast+=  " "
        result += [moves[m]]
        result[i]=result[i].replace("\n","\n"+spaceFirst)
        result[i]=result[i].replace("\n",spaceLast+"\n")
        m=m+1
        if m>7:
            m=0
    return result+result[::-1]