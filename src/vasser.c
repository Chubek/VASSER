#ifndef __INC_TYPES_H
#define __INC_TYPES_H
#include "types.h"
#endif
#ifndef __INC_ADDRUTILS_H
#define __INC_ADDRUTILS_H
#include "addrutils.h"
#endif
#ifndef __INC_STRUTILS_H
#define __INC_STRUTILS_H
#include "strutils.h"
#endif
#ifndef __INC_INTUTILS_H
#define __INC_INTUTILS_H
#include "intutils.h"
#endif
#ifndef __INC_MEMUTILS_H
#define __INC_MEMUTILS_H
#include "memutils.h"
#endif
#ifndef __INC_DNSREZULF_H
#define __INC_DNSREZULF_H
#include "dnsrezulf.h"
#endif
#ifndef __INC_GLOBVARS_INC
#define __INC_GLOBVARS_INC
#include "globvars.inc"
#endif


#if defined (__TEST__) && defined (__TEST_FUNC__)

int main() {
	__TEST__FUNC__();
}

#elif defined (__TEST__) && ! defined (__TEST_FUNC__)
#error "You may not define __TEST__ without defining __TEST_FUNC__"
#elif defined (__TEST_FUNC__) && ! defined (__TEST__)
#error "You may not define __TEST_FUNC__ without defining __TEST__"
#endif