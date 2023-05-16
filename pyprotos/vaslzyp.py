from os import open, close, read, write, lseek, SEEK_SET, O_CREAT, O_WRONLY, O_RDONLY
from stat import S_IRUSR, S_IWUSR


MAX_BLOCK_SIZE = 65536
MAX_HUFFM_SIZE = 65536
MAX_HCODE_SIZE = 65535
MAX_CONACT_LEN = 8

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


def postincr(self):
	n = self.__num__
	self.__num__ += 1
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
c.update_table(2)
c.update_table(2)
c.update_table(3)
c.update_table(5)
c.update_table(5)
c.update_table(5)
print(c.codes[:10])
print(c.counts[:10])