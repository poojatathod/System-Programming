import re

dict1={}
litdict={}
datatype=[' dd ',' db ',' dw ',' dq ',' resb ',' resw ',' resd ',' resq ',':',' equ ']
jmpInst=['jz','jmp','je','jnz']
sizeofdt={'db':1,'dw':2,'dd':4,'dq':8,'resb':1,'resw':2,'resd':4,'resq':8}



registers={'eax':['Reg32_1','000'],'ebx':['Reg32_4','001'],'ecx':['Reg32_2','010'],'edx':['Reg32_3','011'],'esi':['Reg32_7','100'],'edi':['Reg32_8','101'],'esp':['Reg32_5','110'],'ebp':['Reg32_6','111'],'ax':['Reg16_1','000'],'bx':['Reg16_4','001'],'cx':['Reg16_2','010'],'dx':['Reg16_3','011'],'si':['Reg16_7','100'],'di':['Reg16_8','101'],'sp':['Reg16_5','110'],'bp':['Reg16_6','111'],'al':['Reg8_1','000'],'ah':['Reg8_5','000'],'bl':['Reg8_4','001'],'bh':['Reg8_8','001'],'cl':['Reg8_2','010'],'ch':['Reg8_6','010'],'dl':['Reg8_3','011'],'dh':['Reg8_7','011']}


opcodes={ "add":"OP1", "cld":"OP2" , "cmp":"OP3" , "dec":"OP4" , "div":"OP5","inc":"OP6","int":"OP7","jmp":"OP8","lodsb":"OP9","lodsd":"OP10","mov":"OP11","movsb":"OP12","movsd":"OP13","mul":"OP14","pop":"OP15","popa":"OP16","push":"OP17","pusha":"OP18","ret":"OP19","scasb":"op20","std":"OP21","stosb":"OP22","stosd":"OP23","sub":"OP24","xor":"OP25","jz":"OP26","je":"OP27","jg":"OP28","jl":"OP29","jnz":"OP30","call":"OP31"}

global sym_no
sym_no=1
global lit_no
lit_no=1
list2=[]
ilist2=[]


def symtbl():
    mflag=0
    line_no=0
    global sym_no
    secFlag=0
    f=open("search_string.asm","r")
    for line in f:
        line_no+=1
        if 'section .text' in line:
            secFlag=1

        if secFlag==1:
            littbl(line,line_no)

        for i in datatype+jmpInst:
	        line=line.strip()
                symid='S'+str(sym_no)
		if i in datatype and i in line:

		   if i==":":
		        x=line.split(":")
			addToSymTbl(x[0],'D','-','-',line_no,'-','-',symid)
		   elif i in [" db "," dw ",' dd ',' dq ']:
                        x=line.split(' ',2)
                        size=calcSize(x[1],x[2])
			addToSymTbl(x[0],'D',size,x[1],line_no,x[2],calAddr(),symid)
                   elif i in [' resb ',' resw ',' resd ',' resq ']:
		        x=line.split(' ')
                        size=calcSize(x[1],x[2])
			addToSymTbl(x[0],'D',calcSize(x[1],x[2]),x[1],line_no,'-',calAddr(),symid)

	        elif i in jmpInst and i in line:
		    x=line.split(' ')
		    addToSymTbl(x[1],'U','-','-',line_no,'-','-',symid)

        if 'main:' in line:
           mflag=1
        if mflag==1:
           intermediate(line)
        #intermediateafter(line)

def CheckDefOrNot(Symbol,DefOrUndef):
    if Symbol not in dict1:
        return 1
    else:
        if (dict1[Symbol][0]=='D' and DefOrUndef=='D'):
            return -1
        elif dict1[Symbol][0]=='U' and DefOrUndef=='D':
            return 1



def addToSymTbl(sym,DefUndef,SizeOfSym,DataType,LineNo,Value,addr,symid):
    global sym_no
    doru=CheckDefOrNot(sym,DefUndef)
    if doru==-1:
       print "ERROR: redefination of symbol"
    elif doru==1:
        dict1[sym]=[DefUndef,SizeOfSym,DataType,LineNo,Value,addr,symid]
        sym_no+=1

def calcSize(dt,val):
    if dt=='db':
        val=val.replace('"','')
	val=val.replace(',','')
	return len(val)

    if dt in ['dw','dd','dq']:
        val=val.split(",")
	val=len(val)
	val=val*(sizeofdt[dt])
	return val

    if dt in ['resb','resd','resw','resq']:
        val=int(val)*(sizeofdt[dt])
	return val


def calAddr():
    if len(dict1)==0:
        return 0;
    else:
        addr=0
        for sym in dict1:
             tsize=dict1[sym][1]
             if tsize=='-':
                 return '-'
             else:
                 addr+=tsize
        return addr



def littbl(line, lineno):
    global lit_no
    l="L"+str(lit_no)
    line=line.strip()
    line=re.split(' |,',line)
    len_lit=len(line)
    if len_lit==3:
        try:
            i=int(line[2])
            litdict[line[2]]=[l,lineno,hex(int(line[2]))]
            lit_no+=1

        except ValueError:
            if line[2][0]=="'" and line[2][2]=="'" and len_lit==3:
                litdict[line[2]]=[l,lineno,hex(ord(line[2][1]))]
                lit_no+=1


    elif len_lit==2:
        try:
            i=int(line[1])
            litdict[line[1]]=[l,lineno,hex(int(line[1]))]
            lit_no+=1

        except ValueError:
            if line[1][0]=="'" and line[1][2]=="'" and len(line[1])==3:
                litdict[line[1]]=[l,lineno,hex(ord(line[1][1]))]
                lit_no+=1


def intermediate(line):
    ilist1=[]
    line=line.strip()
    li=re.split(' |,',line)
    str1=''
    if li[0] in opcodes:
        str1+=opcodes[li[0]]

    if len(li)==3:
        if li[1] in registers:
            str1+='  '+registers[li[1]][0]

        elif 'dword' in li[1]:
            v=li[1]
            v=v.split('[')
            v=v[1].split(']')
            if v in dict1:
                str1+='  MEM['+dict1[v][6]+']'
            elif v in registers:
                str1+='  MEM['+registers[v][0]+']'

        if li[2] in registers:
            str1+='  '+registers[li[2]][0]

        elif 'dword' in li[2]:
            v1=li[2]
            v1=v1.split('[')
            v1=v1[1].split(']')
            if v1[0] in dict1:
                str1+='  MEM['+dict1[v1[0]][6]+']'
            elif v1 in registers:
                str1+='  MEM['+registers[li[2]][0]+']'

        elif li[2] in dict1:
            str1+='  IMD['+dict1[li[2]][6]+']'
        elif li[2] in litdict:
            str1+='  IMD['+litdict[li[2]][0]+']'

        ilist1.append(str1)
        ilist1.append(line)
        ilist2.append(ilist1)

    elif len(li)==2:
        if li[1] in registers:
            str1+='  '+registers[li[1]][0]

        elif 'dword' in li[1]:
            v1=li[1]
            v1=v1.split('[')
            v1=v1[1].split(']')
            if v1[0] in dict1:
                str1+='  MEM['+dict1[v1[0]][6]+']'
            elif v1 in registers:
                str1+='  MEM['+registers[li[1]][0]+']'

        elif li[1] in dict1:
            str1+='  IMD['+dict1[li[1]][6]+']'
        elif li[1] in litdict:
            str1+='  IMD['+litdict[li[1]][0]+']'


        ilist1.append(str1)
        ilist1.append(line)
        ilist2.append(ilist1)





'''def intermediateafter(line):

    list1=[]

    line=line.strip()
    li=re.split(' |,',line)
    if len(li)==3:
        str1=''
        str1=str(li[0])+' '+'11'+' '
        for reg in registers:
            if li[1]==reg:
                str1+=str(registers[reg][1])
            if li[2]==reg:
                str1+=str(registers[reg][1])
        for sym in dict1:
            if li[2]==sym:
                str1+="["+str(dict1[li[2]][5])+"]"
        for lit in litdict:
            if li[2]==litdict[lit][0]:
                str1+=lit

        list1.append(str1)
        list1.append(line)
        list2.append(list1)


    if len(li)==2:
        str1=''
        for reg in registers:
            if li[1]==reg:
                str1=str(li[0])+' '+'11'+' '
                str1+=str(registers[reg][1])


        list1.append(str1)
        list1.append(line)
        list2.append(list1)'''


symtbl()
print "!!!!!!!!........             SYMBOL TABLE            .........!!!!!!!! \n\n"
print "SYM_NO\tSYMBOL\tDEF_UNDEF\tSIZE_OF_SYM\tDATA_TYPE\tLINE_NO\t\tAddress\t\tVALUE\n"
for sym in dict1:
    print dict1[sym][6],"\t",sym,"\t",dict1[sym][0],"\t\t",dict1[sym][1],"\t\t",dict1[sym][2],"\t\t",dict1[sym][3],"\t\t",dict1[sym][5],"\t\t",dict1[sym][4]


print "\n\n\n!!!!!!!!!.......       LITRAL TABLE            ...........!!!!!!!!\n\n"
print "LIT_NAME\t LITRAL\t\tLINE_NO\t\tHEX_VALUE"
for litname in litdict:
    print litdict[litname][0],"\t\t",litname,"\t\t",litdict[litname][1],"\t\t",litdict[litname][2]


print "\n\n\n !!!!!!!!...............INTERMIDIATE    ...............!!!!!!!!\n\n"
for lst in ilist2:
    print lst[0],"                             ",lst[1]



print "\n\n\n!!!!!!!!!!!...........   INTERMEDIATE TABLE    ..........!!!!!!!!!\n\n"
for lst in list2:
    print lst[0],'                         ',lst[1]


