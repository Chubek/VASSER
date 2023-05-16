#ifndef __INC_GLOBVARS_INC
#define __INC_GLOBVARS_INC
#include "globvars.inc"
#endif
#ifndef __INC_ERRORS_INC
#define __INC_ERRORS_INC
#include "errors.inc"
#endif
#ifndef __INC_PROTOS_INC
#define __INC_PROTOS_INC
#include "protos.inc"
#endif
#ifndef __INC_REGISTERS_INC
#define __INC_REGISTERS_INC
#include "registers.inc"
#endif
#ifndef __INC_SYSCALL_INC
#define __INC_SYSCALL_INC
#include "syscall.inc"
#endif
#ifndef __INC_SYSCNR_INC
#define __INC_SYSCNR_INC
#include "syscnr.inc"
#endif


.data
#include "globals.inc"


.text
#include "addrutils.S"
#include "intutils.S"
#include "memutils.S"
#include "intutils.S"
#include "dnsrezulf.S"
