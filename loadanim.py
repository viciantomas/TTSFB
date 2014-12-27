lines = 3
speed = 0.08
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
    for i in range(0,41):
        spaceFirst= ""
        spaceLast= ""
        
        for j in range(0, i):
            spaceFirst+= " "
        for j in range(0, 41-i):
            spaceLast+=  " "
        result += [moves[m]]
        result[i]=result[i].replace("\n","\n"+spaceFirst)
        result[i]=result[i].replace("\n",spaceLast+"\n")
        m=m+1
        if m>7:
            m=0
    return result+result[::-1]