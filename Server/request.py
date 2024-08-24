import requests

set=set()
for i in range(100):
    request=requests.get('http://127.0.0.1:8000/random')
    print(request.json()['random'], end=' ')
    set.add(request.json()['random'])
    if (i+1)%20==0:
        print()
print('len->',len(set))
    