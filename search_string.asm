section .data
	str1 db "my string is 2016 pucsd",10,0
    subs db "2016",10,0
    n dd 4
section .bss
	str2 resb 10

section .text
	global main
	extern printf

main:
	xor eax,eax
	xor ebx,ebx
	xor ecx,ecx
	xor edx,edx
    mov eax,dword[n]
	mov ebx,str1
	mov edx,10
	mov ecx,subs
	

pqr:    
	cmp ebx,2
	jz abc
	jnz return

abc:
	mov al,'a'
	mov edx,al
	inc ebx
	inc ecx
	inc edx
	jmp pqr
	
return:
	push edx
	add esp,8
	ret

	
