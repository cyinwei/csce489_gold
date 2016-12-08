import os
import pandas as pd
import json

class RedditParser:

    # Function for writing output
    @staticmethod
    def write_gilded_file(df, fileout):
        gilded = df[df['gilded'] > 0]
        print 'Writing', gilded.shape[0], 'entries to', fileout
        if os.path.isfile(fileout):
            gilded.to_csv(fileout, mode='a', header=False, encoding='utf-8', index=False, quoting=3)
        else:
            gilded.to_csv(fileout, encoding='utf-8', index=False, quoting=3)

    # Function for reading file with given parameters
    @staticmethod
    def parse_file_for_gilded(filein, amount, fileout):
        print 'Opening', filein
        with open(filein, 'r') as f:
            itt = 1 # Line counter
            lines = []
            for line in f:
                lines.append(json.loads(line[:-1]))
                itt+=1
                if itt > amount: # If chunk_size is reached, write to csv and clear memory
                    if lines:
                        RedditParser.write_gilded_file(pd.DataFrame(lines), fileout)
                    lines = [] # Clear list (free memory)
                    itt = 1 # Reset line counter
            if lines: # Write final lines of file (if any)
                RedditParser.write_gilded_file(pd.DataFrame(lines), fileout)
                lines = []
        print 'Complete! All gilded records from', filein, 'written to', fileout


    # Function for writing output
    @staticmethod
    def write_top10_file(df, fileout):
        top10 = ['AskReddit', 'pics', 'funny', 'videos', 'todayilearned', 'AdviceAnimals', 'news', 'WTF', 'worldnews', 'nfl']
        t = df[(df['subreddit'].isin(top10)) & (df['parent_id'].str.startswith('t3_', na=False))]
        print 'Writing', t.shape[0], 'entries.'
        for subreddit in top10:
            if os.path.isfile(fileout + '_' + subreddit + '.csv'):
                t[t['subreddit'] == subreddit].to_csv(fileout + '_' + subreddit + '.csv', mode='a', header=False, encoding='utf-8', index=False, quoting=3)
            else:
                t[t['subreddit'] == subreddit].to_csv(fileout + '_' + subreddit + '.csv', encoding='utf-8', index=False, quoting=3)

    # Function for reading file with given parameters
    @staticmethod
    def parse_file_for_top10(filein, amount, fileout):
        print 'Opening', filein
        with open(filein, 'r') as f:
            itt = 1 # Line counter
            lines = []
            for line in f:
                lines.append(json.loads(line[:-1]))
                itt+=1
                if itt > amount: # If chunk_size is reached, write to csv and clear memory
                    if lines:
                        RedditParser.write_top10_file(pd.DataFrame(lines), fileout)
                    lines = [] # Clear list (free memory)
                    itt = 1 # Reset line counter
            if lines: # Write final lines of file (if any)
                RedditParser.write_top10_file(pd.DataFrame(lines), fileout)
            lines = []
        print 'Complete! All top10 subreddit records from', filein, 'written to', fileout
