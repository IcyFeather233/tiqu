import json

filename = '去重借月抒怀的诗句，借月抒情的诗句..csv'

f = open('./transfer/geyan.json', 'r', encoding='utf-8')
load_dict = json.load(f)
filename = filename[2:-5] + '.txt'
filename = load_dict[filename] + '.csv'

print(filename)