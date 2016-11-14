import pandas as pd
import json

class RedditParser:
	# Function for writing output
	def write_file(df, fileout):
		gilded = df[df['gilded'] > 0]
		print 'Writing', gilded.shape[0], 'entries to', fileout
		if os.path.isfile(fileout):
			gilded.to_csv(fileout, mode='a', header=False, encoding='utf-8', index=False)
		else:
			gilded.to_csv(fileout, encoding='utf-8', index=False)

	# Function for reading file with given parameters
	def parse_file(filein, amount, fileout):
		print 'Opening', filein
		with open(filein, 'r') as f:
			itt = 1 # Line counter
			lines = []
			for line in f:
				lines.append(json.loads(line[:-1]))
				itt+=1
				if itt > amount: # If chunk_size is reached, write to csv and clear memory
					if lines:
						write_file(pd.DataFrame(lines), fileout)
					lines = [] # Clear list (free memory)
					itt = 1 # Reset line counter
			if lines: # Write final lines of file (if any)
				write_file(pd.DataFrame(lines), fileout)
				lines = []
		print 'Complete! All gilded records from', filein, 'written to', fileout