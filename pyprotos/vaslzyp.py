from os import open, close, read, write, lseek, SEEK_SET, O_CREAT, O_WRONLY, O_RDONLY
from stat import S_IRUSR, S_IWUSR
from operator import rshift, lshift, add, and_, ge, le, sub


MAX_BLOCK_SIZE = 65536

MAX_HUFFM_SIZE = 16777216

AND_OPRDS_CNTZ = (
	0x00ffffffffffffff,
	0x0000ffffffffffff,
	0x000000ffffffffff,
	0x00000000ffffffff,
	0x0000000000ffffff,
	0x000000000000ffff,
	0x00000000000000ff,
	0x000000000000000f,
	0x0000000000000003,
	0x0000000000000001,
)

AND_OPRDS_CNLZ = (
	0xffffffffffffff00,
	0xffffffffffff0000,
	0xffffffffff000000,
	0xffffffff00000000,
	0xffffff0000000000,
	0xffff000000000000,
	0xff00000000000000,
	0xf000000000000000,
	0xc000000000000000,
	0x8000000000000000,
)

CNT_FIRSTSET_ADDS_SHIFTS = (56, 48, 40, 32, 24, 16, 8, 4, 2, 1)

MAX_U2PN = [
	0x0000000000000000, 0x0000000000000001, 0x0000000000000003, 0x0000000000000007, 
	0x000000000000000f, 0x000000000000001f, 0x000000000000003f, 0x000000000000007f, 
	0x00000000000000ff, 0x00000000000001ff, 0x00000000000003ff, 0x00000000000007ff, 
	0x0000000000000fff, 0x0000000000001fff, 0x0000000000003fff, 0x0000000000007fff, 
	0x000000000000ffff, 0x000000000001ffff, 0x000000000003ffff, 0x000000000007ffff, 
	0x00000000000fffff, 0x00000000001fffff, 0x00000000003fffff, 0x00000000007fffff, 
	0x0000000000ffffff, 0x0000000001ffffff, 0x0000000003ffffff, 0x0000000007ffffff, 
	0x000000000fffffff, 0x000000001fffffff, 0x000000003fffffff, 0x000000007fffffff, 
	0x00000000ffffffff, 0x00000001ffffffff, 0x00000003ffffffff, 0x00000007ffffffff, 
	0x0000000fffffffff, 0x0000001fffffffff, 0x0000003fffffffff, 0x0000007fffffffff, 
	0x000000ffffffffff, 0x000001ffffffffff, 0x000003ffffffffff, 0x000007ffffffffff, 
	0x00000fffffffffff, 0x00001fffffffffff, 0x00003fffffffffff, 0x00007fffffffffff, 
	0x0000ffffffffffff, 0x0001ffffffffffff, 0x0003ffffffffffff, 0x0007ffffffffffff, 
	0x000fffffffffffff, 0x001fffffffffffff, 0x003fffffffffffff, 0x007fffffffffffff, 
	0x00ffffffffffffff, 0x01ffffffffffffff, 0x03ffffffffffffff, 0x07ffffffffffffff, 
	0x0fffffffffffffff, 0x1fffffffffffffff, 0x3fffffffffffffff, 0x7fffffffffffffff,
]

AND_CNTS = [
	0x01, 0x01, 0x03, 0x03, 0x07, 0x07, 0x07, 0x07,
	0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f,
	0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f,
	0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f,
	0x3f, 0x3f, 0x3f, 0x3f, 0x3f, 0x3f, 0x3f, 0x3f,
	0x3f, 0x3f, 0x3f, 0x3f, 0x3f, 0x3f, 0x3f, 0x3f,
	0x3f, 0x3f, 0x3f, 0x3f, 0x3f, 0x3f, 0x3f, 0x3f,
	0x3f, 0x3f, 0x3f, 0x3f, 0x3f, 0x3f, 0x3f, 0x3f,
]

LEN_CNTS = [
	1, 1, 2, 2, 3, 3, 3, 3,
	4, 4, 4, 4, 4, 4, 4, 4,
	5, 5, 5, 5, 5, 5, 5, 5,
	5, 5, 5, 5, 5, 5, 5, 5,
	6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6,
]



def dataclass(cls: type) -> type:
	args = {k: v for k, v in cls.__dict__.items() if not k.startswith("__")}
	def init(self, **args):
		for k, v in args.items():
			exec(f"self.{k} = {v}")
	def str(self):
		string = ""
		for k in self.__class__.__dict__:
			if not k.startswith("__"):
				val = eval(f'self.{k}')
				string +=  f"{k} -> {val}\n"
		return string
	cls.__init__ = init
	cls.__str__ = str
	return cls



def postop(self, other=1, operator=add):
	n = self.__num__
	self.__num__ = operator(self.__num__, other.__num__ if "__num__" in vars(other.__class__) else other)
	return n



def preop(self, other=1, operator=add):
	self.__num__ = operator(self.__num__, other.__num__ if "__num__" in vars(other.__class__) else other)	
	return self.__num__



def passthru(self, other=1, operator=add):
	return operator(self.__num__, other.__num__ if "__num__" in vars(other.__class__) else other)



def bitsetcnt(self, shiftop, ands, shadds=CNT_FIRSTSET_ADDS_SHIFTS):
	if self.__num__ == 0: return 64
	n = 0
	for andoprd_, shiftoprd, addoprd in zip(ands, shadds, shadds):
		if not passthru(self, andoprd_, and_):
			n +=  addoprd
			preop(self, shiftoprd, shiftop)
	return n


def djb2short(s: bytes):
	hash = 0
	for c in s:
		hash = (((hash << 5) + hash) + c) % MAX_BLOCK_SIZE
	return hash


@dataclass
class AdaptiveHuffmanCoder:
	codes = list(range(MAX_HUFFM_SIZE))
	counts = [0] * MAX_HUFFM_SIZE
	max_so_far = 0


	def update_table(self, symbol: int):
		self.counts[symbol] += 1
		if self.counts[symbol] > self.max_so_far:
			tmp = self.codes[symbol]
			self.codes[symbol] = self.codes[self.max_so_far]
			self.codes[self.max_so_far] = tmp


	def write_encoded_count(self, fd):
		oprpack = {
			"__ge__": lambda self, other: passthru(self, other, ge), 
			"__le__": lambda self, other: passthru(self, other, le), 
			"__sub__": lambda self, other: passthru(self, other, sub),
			"__rshift__": lambda self, other: passthru(self, other, rshift),
			"__rrshift__": lambda self, other: passthru(self, other, rshift),
			"__lshift__": lambda self, other: passthru(self, other, lshift),
			"__str__": lambda self: str(self.__num__)
		}
		args_clz = (lshift, AND_OPRDS_CNLZ)
		args_ctz = (rshift, AND_OPRDS_CNTZ)
		for i in range(0, MAX_HUFFM_SIZE, 4):
			c1, c2, c3, c4 = self.counts[i:i + 4]
			cnt = int.from_bytes(bytearray([c1, c2, c3, c4]), byteorder='little', signed=False)
			ctz = type("Ctz", (), {"__num__": cnt, "__invert__": lambda self: bitsetcnt(self, *args_ctz), **oprpack})()
			clz = type("Clz", (), {"__num__": cnt, "__invert__": lambda self: bitsetcnt(self, *args_clz), **oprpack})()
			ctz = ~ctz
			clz = ~clz
			lenset = ctz - clz if ctz >= clz else clz - ctz
			cnt = cnt >> ctz
			cnt &= MAX_U2PN[dif]
			ctz &= AND_CNTS[ctz]
			clz &= AND_CNTS[clz]
			code = ctz | (cnt << ctz) | (clz << (dif))
			print(code)
			print(ctz, clz, cnt, code.to_bytes(3, byteorder='little', signed=False))
			#write(fd, int.to_bytes(code, byteorder='little', signed=False))
			exit()

@dataclass
class PanLzypTrie:
	data = list(range(256))
	datalen = 0
	pointers = [{'parent': 0, 'symbol': 0, 'terminal': 0}] * MAX_BLOCK_SIZE

	def add_item(self, item: bytes):
		idx = 0
		for i in range(1, MAX_CONCAT_LEN):
			hash = djb2short(item[i - 1] + item[i])
			if self.pointers[hash]['parent'] == 0:
				idx = hash		
			else:
				idx = hash + 1
			self.pointers[idx]['parent'] = item[i - 1]
			self.pointers[idx]['symbol'] = item[i]
		self.pointers[idx]['terminal'] = 1

	def seach_for_item(self, idx: int):
		item = bytearray()
		terminal = 0
		while not terminal:
			idx = self.pointers[idx]['parent']
			item += self.pointers[idx]['symbol']
			terminal = self.pointers[idx]['terminal']
		return item





def lzy_compress(inpf: str, outf: str):
	inpfd = open(inpf, O_RDONLY, S_IRUSR)
	outfd = open(outf, O_WRONLY | O_CREAT, S_IWUSR | S_IRUSR)
	
	s = list(range(256, 512))
	t = []
	m = bytearray()
	o = bytearray()
	i = type("PostIncr", (), {"__num__": 256, "__pos__": postincr})
	while True:
		c = read(inpfd, 1)
		if not c: break
		if o + c in s:
			o += c
		else:
			write(outfd, s[int.from_bytes(o, byteorder='little', signed=False)])
			o = c
			s += t
			t = bytearray()
		while any([m + c not in d for d in [s, t]]):
			t.append(m + c)
			m = m[1:]
		m = m + c
	write(outfd, s[int.from_bytes(o, byteorder='little', signed=False)])
	lseek(outfd, 0, SEEK_SET)
	write(outfd, len(s).to_bytes(8, byteorder='little', signed=False))
	write(outfd, s)
	close(inpfd)
	close(outfd)


def lzy_compress(inpf: str, outf: str):
	inpfd = open(inpf, O_RDONLY, S_IRUSR)
	outfd = open(outf, O_WRONLY | O_CREAT, S_IWUSR | S_IRUSR)
	dlen = read(inpfd, 8)
	dlen = int.from_bytes(dlen, byteorder='little', signed=False)
	s = read(inpfd, dlen)


	close(inpfd)
	close(outfd)


c = AdaptiveHuffmanCoder()
c.counts = [12, 33, 1, 9 ,1]
c.write_encoded_count(0)