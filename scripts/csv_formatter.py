import os


# OLD CODE USED TO ADD YEAR COLUMN TO ALL FILES:
# script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
# for i in range(1958,2016):
# 	with open(os.path.join(script_dir, '100_top_songs/'+str(i)+'.csv'),'r') as readfile:
# 		with open(os.path.join(script_dir, '100_top_songs2/'+str(i)+'.csv'),'w') as writefile:
# 			writefile.write('Year,'+readfile.readline())
# 			for j in range(0,100):
# 				writefile.write(str(i)+','+readfile.readline())


# OLD CODE USED TO MERGE ALL FILES INTO TOP_SONGS.CSV
# script_dir = os.path.dirname(__file__)
# writefile = open('top_songs.csv','w')
# writefile.write('Year,Position,Artist,Song Title\n')
# for i in range(1958,2016):
# 	with open(os.path.join(script_dir, '100_top_songs/'+str(i)+'.csv'),'r') as rfile:
# 		rfile.readline()
# 		for j in range(0,100):
# 			writefile.write(rfile.readline())
# writefile.close()