extern memaddr_t allocate_program_area(memsize_t size);
extern nonyield_t deallocate_back_program_area(memaddr_t addr, memsize_t size);
extern memaddr_t allocate_shared_memory(memsize_t size);
extern nonyield_t deallocate_bacK_shared_memory(memaddr_t addr, memsize_t size);
nonyield_t copy_memory_from_bytewise(memaddr_t dst, memaddr_t src, memsize_t len);
nonyield_t clear_memory_qwordwise(memaddr_t addr, memsize_t size);
nonyield_t clear_memory_bytewise(memaddr_t addr, memsize_t size);
