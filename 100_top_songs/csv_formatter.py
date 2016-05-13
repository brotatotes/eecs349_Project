import os

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in



for i in range(1958,2016):
	with open(os.path.join(script_dir, '100_top_songs/'+str(i)+'.csv'),'r') as readfile:
		with open(os.path.join(script_dir, '100_top_songs2/'+str(i)+'.csv'),'w') as writefile:
			writefile.write('Year,'+readfile.readline())
			for j in range(0,100):
				writefile.write(str(i)+','+readfile.readline())
