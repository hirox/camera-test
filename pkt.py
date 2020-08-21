desc = "Parse pcap"

import dpkt

parser = argparse.ArgumentParser(description=desc)
parser.add_argument('-i', '--input', help='input .pcap', default='in.pcap')
parser.add_argument('-o', '--output', help='output binary', default='out.bin')
parser.add_argument('-t', '--targetpts', help='target PTS', type=int, default=607240964)
parser.add_argument('-p', '--platform', help='win or linux', default='linux')
args = parser.parse_args()

header = 64 # Linux
if args.platform == 'win':
	header = 27 # Windows

pcr = dpkt.pcap.Reader(open(args.input,'rb'))
packet_count = 0

o = open(args.output, 'wb')

remains = bytes()
maxcount = 0
maxpts = 0
count = 0
lastpts = 0

for ts,buf in pcr:
	packet_count += 1
	if len(buf) > 10000:
		x = buf[header:]
		if x[0] == 0x0C:
			pts = int.from_bytes(x[2:6], 'little')
			if (lastpts == pts):
				count = count + 1
				if maxcount < count:
					maxcount = count
					maxpts = pts
			else:
				lastpts = pts
				count = 0

			x = x[0x0C:]

		print(packet_count, '. time: ', ts, 'Length:', len(buf) , ' ', lastpts, ' ', count)

		x = remains + x
		#o.write(x)
		#print(int(len(x)/3))
		if lastpts == args.targetpts:
			for num in range(int(len(x)/3/8)):
				o.write(bytes([x[num*3*8]]))
				o.write(bytes([x[num*3*8+1]]))
				o.write(bytes([x[num*3*8+2]]))

		remains = x[int(len(x)/3/8)*8*3:]

print(maxcount, " ", maxpts)

o.close()