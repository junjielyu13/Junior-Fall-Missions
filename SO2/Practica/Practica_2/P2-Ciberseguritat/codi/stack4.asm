
a.out:     file format elf64-x86-64


Disassembly of section .init:

0000000000001000 <_init>:
    1000:	f3 0f 1e fa          	endbr64 
    1004:	48 83 ec 08          	sub    $0x8,%rsp
    1008:	48 8b 05 d9 2f 00 00 	mov    0x2fd9(%rip),%rax        # 3fe8 <__gmon_start__@Base>
    100f:	48 85 c0             	test   %rax,%rax
    1012:	74 02                	je     1016 <_init+0x16>
    1014:	ff d0                	call   *%rax
    1016:	48 83 c4 08          	add    $0x8,%rsp
    101a:	c3                   	ret    

Disassembly of section .plt:

0000000000001020 <.plt>:
    1020:	ff 35 7a 2f 00 00    	push   0x2f7a(%rip)        # 3fa0 <_GLOBAL_OFFSET_TABLE_+0x8>
    1026:	f2 ff 25 7b 2f 00 00 	bnd jmp *0x2f7b(%rip)        # 3fa8 <_GLOBAL_OFFSET_TABLE_+0x10>
    102d:	0f 1f 00             	nopl   (%rax)
    1030:	f3 0f 1e fa          	endbr64 
    1034:	68 00 00 00 00       	push   $0x0
    1039:	f2 e9 e1 ff ff ff    	bnd jmp 1020 <_init+0x20>
    103f:	90                   	nop
    1040:	f3 0f 1e fa          	endbr64 
    1044:	68 01 00 00 00       	push   $0x1
    1049:	f2 e9 d1 ff ff ff    	bnd jmp 1020 <_init+0x20>
    104f:	90                   	nop
    1050:	f3 0f 1e fa          	endbr64 
    1054:	68 02 00 00 00       	push   $0x2
    1059:	f2 e9 c1 ff ff ff    	bnd jmp 1020 <_init+0x20>
    105f:	90                   	nop
    1060:	f3 0f 1e fa          	endbr64 
    1064:	68 03 00 00 00       	push   $0x3
    1069:	f2 e9 b1 ff ff ff    	bnd jmp 1020 <_init+0x20>
    106f:	90                   	nop
    1070:	f3 0f 1e fa          	endbr64 
    1074:	68 04 00 00 00       	push   $0x4
    1079:	f2 e9 a1 ff ff ff    	bnd jmp 1020 <_init+0x20>
    107f:	90                   	nop

Disassembly of section .plt.got:

0000000000001080 <__cxa_finalize@plt>:
    1080:	f3 0f 1e fa          	endbr64 
    1084:	f2 ff 25 6d 2f 00 00 	bnd jmp *0x2f6d(%rip)        # 3ff8 <__cxa_finalize@GLIBC_2.2.5>
    108b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

Disassembly of section .plt.sec:

0000000000001090 <puts@plt>:
    1090:	f3 0f 1e fa          	endbr64 
    1094:	f2 ff 25 15 2f 00 00 	bnd jmp *0x2f15(%rip)        # 3fb0 <puts@GLIBC_2.2.5>
    109b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

00000000000010a0 <__stack_chk_fail@plt>:
    10a0:	f3 0f 1e fa          	endbr64 
    10a4:	f2 ff 25 0d 2f 00 00 	bnd jmp *0x2f0d(%rip)        # 3fb8 <__stack_chk_fail@GLIBC_2.4>
    10ab:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

00000000000010b0 <printf@plt>:
    10b0:	f3 0f 1e fa          	endbr64 
    10b4:	f2 ff 25 05 2f 00 00 	bnd jmp *0x2f05(%rip)        # 3fc0 <printf@GLIBC_2.2.5>
    10bb:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

00000000000010c0 <gets@plt>:
    10c0:	f3 0f 1e fa          	endbr64 
    10c4:	f2 ff 25 fd 2e 00 00 	bnd jmp *0x2efd(%rip)        # 3fc8 <gets@GLIBC_2.2.5>
    10cb:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

00000000000010d0 <exit@plt>:
    10d0:	f3 0f 1e fa          	endbr64 
    10d4:	f2 ff 25 f5 2e 00 00 	bnd jmp *0x2ef5(%rip)        # 3fd0 <exit@GLIBC_2.2.5>
    10db:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

Disassembly of section .text:

00000000000010e0 <_start>:
    10e0:	f3 0f 1e fa          	endbr64 
    10e4:	31 ed                	xor    %ebp,%ebp
    10e6:	49 89 d1             	mov    %rdx,%r9
    10e9:	5e                   	pop    %rsi
    10ea:	48 89 e2             	mov    %rsp,%rdx
    10ed:	48 83 e4 f0          	and    $0xfffffffffffffff0,%rsp
    10f1:	50                   	push   %rax
    10f2:	54                   	push   %rsp
    10f3:	45 31 c0             	xor    %r8d,%r8d
    10f6:	31 c9                	xor    %ecx,%ecx
    10f8:	48 8d 3d 4c 01 00 00 	lea    0x14c(%rip),%rdi        # 124b <main>
    10ff:	ff 15 d3 2e 00 00    	call   *0x2ed3(%rip)        # 3fd8 <__libc_start_main@GLIBC_2.34>
    1105:	f4                   	hlt    
    1106:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
    110d:	00 00 00 

0000000000001110 <deregister_tm_clones>:
    1110:	48 8d 3d f9 2e 00 00 	lea    0x2ef9(%rip),%rdi        # 4010 <__TMC_END__>
    1117:	48 8d 05 f2 2e 00 00 	lea    0x2ef2(%rip),%rax        # 4010 <__TMC_END__>
    111e:	48 39 f8             	cmp    %rdi,%rax
    1121:	74 15                	je     1138 <deregister_tm_clones+0x28>
    1123:	48 8b 05 b6 2e 00 00 	mov    0x2eb6(%rip),%rax        # 3fe0 <_ITM_deregisterTMCloneTable@Base>
    112a:	48 85 c0             	test   %rax,%rax
    112d:	74 09                	je     1138 <deregister_tm_clones+0x28>
    112f:	ff e0                	jmp    *%rax
    1131:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
    1138:	c3                   	ret    
    1139:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

0000000000001140 <register_tm_clones>:
    1140:	48 8d 3d c9 2e 00 00 	lea    0x2ec9(%rip),%rdi        # 4010 <__TMC_END__>
    1147:	48 8d 35 c2 2e 00 00 	lea    0x2ec2(%rip),%rsi        # 4010 <__TMC_END__>
    114e:	48 29 fe             	sub    %rdi,%rsi
    1151:	48 89 f0             	mov    %rsi,%rax
    1154:	48 c1 ee 3f          	shr    $0x3f,%rsi
    1158:	48 c1 f8 03          	sar    $0x3,%rax
    115c:	48 01 c6             	add    %rax,%rsi
    115f:	48 d1 fe             	sar    %rsi
    1162:	74 14                	je     1178 <register_tm_clones+0x38>
    1164:	48 8b 05 85 2e 00 00 	mov    0x2e85(%rip),%rax        # 3ff0 <_ITM_registerTMCloneTable@Base>
    116b:	48 85 c0             	test   %rax,%rax
    116e:	74 08                	je     1178 <register_tm_clones+0x38>
    1170:	ff e0                	jmp    *%rax
    1172:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)
    1178:	c3                   	ret    
    1179:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

0000000000001180 <__do_global_dtors_aux>:
    1180:	f3 0f 1e fa          	endbr64 
    1184:	80 3d 85 2e 00 00 00 	cmpb   $0x0,0x2e85(%rip)        # 4010 <__TMC_END__>
    118b:	75 2b                	jne    11b8 <__do_global_dtors_aux+0x38>
    118d:	55                   	push   %rbp
    118e:	48 83 3d 62 2e 00 00 	cmpq   $0x0,0x2e62(%rip)        # 3ff8 <__cxa_finalize@GLIBC_2.2.5>
    1195:	00 
    1196:	48 89 e5             	mov    %rsp,%rbp
    1199:	74 0c                	je     11a7 <__do_global_dtors_aux+0x27>
    119b:	48 8b 3d 66 2e 00 00 	mov    0x2e66(%rip),%rdi        # 4008 <__dso_handle>
    11a2:	e8 d9 fe ff ff       	call   1080 <__cxa_finalize@plt>
    11a7:	e8 64 ff ff ff       	call   1110 <deregister_tm_clones>
    11ac:	c6 05 5d 2e 00 00 01 	movb   $0x1,0x2e5d(%rip)        # 4010 <__TMC_END__>
    11b3:	5d                   	pop    %rbp
    11b4:	c3                   	ret    
    11b5:	0f 1f 00             	nopl   (%rax)
    11b8:	c3                   	ret    
    11b9:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

00000000000011c0 <frame_dummy>:
    11c0:	f3 0f 1e fa          	endbr64 
    11c4:	e9 77 ff ff ff       	jmp    1140 <register_tm_clones>

00000000000011c9 <complete_level>:
  "Welcome to " LEVELNAME ", brought to you by https://exploit.education"

char *gets(char *);


void complete_level() {
    11c9:	f3 0f 1e fa          	endbr64 
    11cd:	55                   	push   %rbp
    11ce:	48 89 e5             	mov    %rsp,%rbp
  printf("Congratulations, you've finished " LEVELNAME " :-) Well done!\n");
    11d1:	48 8d 05 30 0e 00 00 	lea    0xe30(%rip),%rax        # 2008 <_IO_stdin_used+0x8>
    11d8:	48 89 c7             	mov    %rax,%rdi
    11db:	e8 b0 fe ff ff       	call   1090 <puts@plt>
  exit(0);
    11e0:	bf 00 00 00 00       	mov    $0x0,%edi
    11e5:	e8 e6 fe ff ff       	call   10d0 <exit@plt>

00000000000011ea <start_level>:
}

void start_level() {
    11ea:	f3 0f 1e fa          	endbr64 
    11ee:	55                   	push   %rbp
    11ef:	48 89 e5             	mov    %rsp,%rbp
    11f2:	48 83 ec 60          	sub    $0x60,%rsp
    11f6:	64 48 8b 04 25 28 00 	mov    %fs:0x28,%rax
    11fd:	00 00 
    11ff:	48 89 45 f8          	mov    %rax,-0x8(%rbp)
    1203:	31 c0                	xor    %eax,%eax
  char buffer[64];
  void *ret;

  gets(buffer);
    1205:	48 8d 45 b0          	lea    -0x50(%rbp),%rax
    1209:	48 89 c7             	mov    %rax,%rdi
    120c:	e8 af fe ff ff       	call   10c0 <gets@plt>

  ret = __builtin_return_address(0);
    1211:	48 8b 45 08          	mov    0x8(%rbp),%rax
    1215:	48 89 45 a8          	mov    %rax,-0x58(%rbp)
  printf("and will be returning to %p\n", ret);
    1219:	48 8b 45 a8          	mov    -0x58(%rbp),%rax
    121d:	48 89 c6             	mov    %rax,%rsi
    1220:	48 8d 05 24 0e 00 00 	lea    0xe24(%rip),%rax        # 204b <_IO_stdin_used+0x4b>
    1227:	48 89 c7             	mov    %rax,%rdi
    122a:	b8 00 00 00 00       	mov    $0x0,%eax
    122f:	e8 7c fe ff ff       	call   10b0 <printf@plt>
}
    1234:	90                   	nop
    1235:	48 8b 45 f8          	mov    -0x8(%rbp),%rax
    1239:	64 48 2b 04 25 28 00 	sub    %fs:0x28,%rax
    1240:	00 00 
    1242:	74 05                	je     1249 <start_level+0x5f>
    1244:	e8 57 fe ff ff       	call   10a0 <__stack_chk_fail@plt>
    1249:	c9                   	leave  
    124a:	c3                   	ret    

000000000000124b <main>:

int main(int argc, char **argv) {
    124b:	f3 0f 1e fa          	endbr64 
    124f:	55                   	push   %rbp
    1250:	48 89 e5             	mov    %rsp,%rbp
    1253:	48 83 ec 10          	sub    $0x10,%rsp
    1257:	89 7d fc             	mov    %edi,-0x4(%rbp)
    125a:	48 89 75 f0          	mov    %rsi,-0x10(%rbp)
  printf("%s\n", BANNER);
    125e:	48 8d 05 03 0e 00 00 	lea    0xe03(%rip),%rax        # 2068 <_IO_stdin_used+0x68>
    1265:	48 89 c7             	mov    %rax,%rdi
    1268:	e8 23 fe ff ff       	call   1090 <puts@plt>
  start_level(argv[1], argv[2]);
    126d:	48 8b 45 f0          	mov    -0x10(%rbp),%rax
    1271:	48 83 c0 10          	add    $0x10,%rax
    1275:	48 8b 10             	mov    (%rax),%rdx
    1278:	48 8b 45 f0          	mov    -0x10(%rbp),%rax
    127c:	48 83 c0 08          	add    $0x8,%rax
    1280:	48 8b 00             	mov    (%rax),%rax
    1283:	48 89 d6             	mov    %rdx,%rsi
    1286:	48 89 c7             	mov    %rax,%rdi
    1289:	b8 00 00 00 00       	mov    $0x0,%eax
    128e:	e8 57 ff ff ff       	call   11ea <start_level>
    1293:	b8 00 00 00 00       	mov    $0x0,%eax
} 
    1298:	c9                   	leave  
    1299:	c3                   	ret    

Disassembly of section .fini:

000000000000129c <_fini>:
    129c:	f3 0f 1e fa          	endbr64 
    12a0:	48 83 ec 08          	sub    $0x8,%rsp
    12a4:	48 83 c4 08          	add    $0x8,%rsp
    12a8:	c3                   	ret    
