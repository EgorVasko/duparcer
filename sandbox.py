import sys

print("type quit to exit")
command = input()
while command not in ['quit', 'exit', 'konec']:
   command = input()
sys.exit()
