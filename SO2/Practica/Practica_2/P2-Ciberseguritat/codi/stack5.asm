
stack5.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <start_level>:
   0:	f3 0f 1e fa          	endbr64 
   4:	55                   	push   %rbp
   5:	48 89 e5             	mov    %rsp,%rbp
   8:	48 81 ec a0 00 00 00 	sub    $0xa0,%rsp
   f:	64 48 8b 04 25 28 00 	mov    %fs:0x28,%rax
  16:	00 00 
  18:	48 89 45 f8          	mov    %rax,-0x8(%rbp)
  1c:	31 c0                	xor    %eax,%eax
  1e:	48 8d 85 70 ff ff ff 	lea    -0x90(%rbp),%rax
  25:	48 89 c6             	mov    %rax,%rsi
  28:	48 8d 05 00 00 00 00 	lea    0x0(%rip),%rax        # 2f <start_level+0x2f>
  2f:	48 89 c7             	mov    %rax,%rdi
  32:	b8 00 00 00 00       	mov    $0x0,%eax
  37:	e8 00 00 00 00       	call   3c <start_level+0x3c>
  3c:	48 8d 85 70 ff ff ff 	lea    -0x90(%rbp),%rax
  43:	48 89 c7             	mov    %rax,%rdi
  46:	e8 00 00 00 00       	call   4b <start_level+0x4b>
  4b:	48 8b 45 08          	mov    0x8(%rbp),%rax
  4f:	48 89 85 68 ff ff ff 	mov    %rax,-0x98(%rbp)
  56:	48 8b 85 68 ff ff ff 	mov    -0x98(%rbp),%rax
  5d:	48 89 c6             	mov    %rax,%rsi
  60:	48 8d 05 00 00 00 00 	lea    0x0(%rip),%rax        # 67 <start_level+0x67>
  67:	48 89 c7             	mov    %rax,%rdi
  6a:	b8 00 00 00 00       	mov    $0x0,%eax
  6f:	e8 00 00 00 00       	call   74 <start_level+0x74>
  74:	90                   	nop
  75:	48 8b 45 f8          	mov    -0x8(%rbp),%rax
  79:	64 48 2b 04 25 28 00 	sub    %fs:0x28,%rax
  80:	00 00 
  82:	74 05                	je     89 <start_level+0x89>
  84:	e8 00 00 00 00       	call   89 <start_level+0x89>
  89:	c9                   	leave  
  8a:	c3                   	ret    

000000000000008b <main>:
  8b:	f3 0f 1e fa          	endbr64 
  8f:	55                   	push   %rbp
  90:	48 89 e5             	mov    %rsp,%rbp
  93:	48 83 ec 10          	sub    $0x10,%rsp
  97:	89 7d fc             	mov    %edi,-0x4(%rbp)
  9a:	48 89 75 f0          	mov    %rsi,-0x10(%rbp)
  9e:	48 8d 05 00 00 00 00 	lea    0x0(%rip),%rax        # a5 <main+0x1a>
  a5:	48 89 c7             	mov    %rax,%rdi
  a8:	e8 00 00 00 00       	call   ad <main+0x22>
  ad:	b8 00 00 00 00       	mov    $0x0,%eax
  b2:	e8 00 00 00 00       	call   b7 <main+0x2c>
  b7:	b8 00 00 00 00       	mov    $0x0,%eax
  bc:	c9                   	leave  
  bd:	c3                   	ret    
