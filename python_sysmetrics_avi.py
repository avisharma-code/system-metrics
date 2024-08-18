import os
import platform
import time

def extractipifstr(a):
   b = ''
   if isinstance(a, str) == False:
      print('Function only accepts string values')
      exit()
    
   for i in a.strip(''):
      if i in ['0','1','2','3','4','5','6','7','8','9','.'] :
         b+=i
         
   return b
 

def ipngatewaywin():
   p = os.popen('curl -s ifconfig.co -4').read().strip('\n')
   a = os.popen('netsh interface ipv4 show addresses').read()
   l=a.split('interface')
   b=[]
   for i in l:
      if "Default Gateway" in i:
         b.append(i.split('\n'))
   prip = []
   prpl = []
   dg = []
   dgl = []
   for j in range(len(b)):
      for i in b[j]:
         if 'IP Address' in i:
            prip.append(i)
         elif 'Default Gateway' in i:
            dg.append(i)
   for i in range(len(prip)):
      prpl.append(extractipifstr(prip[i]))
   for i in range(len(dg)):
      dgl.append(extractipifstr(dg[i]))
   return p, prpl, dgl


def ipngatewaylin():
   publicip = os.popen('curl -s ifconfig.co -4').read().strip('\n')
   privateip = os.popen('hostname -I').read().strip('\n')
   dgateway = os.popen("ip route | grep default | awk '{print $3}'").read().strip('\n')
   return publicip, privateip, dgateway

def distatswin():
   inf = os.popen('wmic logicaldisk get size,freespace,caption').read().strip().splitlines()
   a = []
   for i in range(1,len(inf)):
      a.append(inf[i].strip().split(' '))
   for i in a:
      for j in range(len(i)-1,-1,-1):
         if i[j] == '':
            i.pop(j)
   for i in range(len(a)-1,-1,-1):
      if len(a[i]) == 0:
         a.pop(i)
   disk_volumes = []
   freespace = []
   totalspace = []
   usedspace = []
   for i in a:
      disk_volumes.append(i[0])
      freespace.append((int(i[1])/(1024*1024)))
      totalspace.append((int(i[2])/(1024*1024)))
   for i in range(len(totalspace)):
      usedspace.append(totalspace[i]-freespace[i])
   return disk_volumes, freespace, usedspace, totalspace
   
def distatlin():
   vol = os.popen("df -h | awk '{print $1}'").read().split('\n')
   totalspace = os.popen("df -h | awk '{print $2}'").read().split('\n')
   usedspace = os.popen("df -h | awk '{print $3}'").read().split('\n')
   freespace = os.popen("df -h | awk '{print $4}'").read().split('\n')
   for i in range(len(vol)-1,-1,-1):
      if vol[i] == 'tmpfs':
         vol.pop(i)
         totalspace.pop(i)
         usedspace.pop(i)
         freespace.pop(i)
   return vol, freespace, usedspace, totalspace

def dirsize(s = R"C:\\"):
   b = 0
   c=0
   try:
      a = os.scandir(s)
      for i in a:
        if i.is_file():
           b+=i.stat().st_size
        elif i.is_dir():
         b+=dirsize(i.path)
   except Exception:
      c+=1
   if c>1:
      print(f"error accesing {c} directories")
   return b/(1024**2)


def largestndir(n = 5, s = R"D:\\"):
   l =[]
   for root, dirs, files in os.walk(s):
      for i in dirs:
         path = os.path.join(root, i)
         a = dirsize(path)
         l.append([path, a])
   ls = sorted(l, key = lambda l:l[1], reverse=True)[:n]
   return ls


def largestdirlin(n = 5, di = '/home/.'):
   l = os.popen(f'du -ah {di} 2>/dev/null | sort -rh | head -n {n}').read().split('\n')
   return l


def totalcpuwin():
   tc = os.popen('wmic cpu get loadpercentage').read().strip().split('\n')
   for i in range(len(tc)-1,-1,-1):
      if len(tc[i])==0:
         tc.pop(i)
   return tc

def processcputime():
   tpc = os.popen('wmic path win32_perfformatteddata_perfproc_process get Name, PercentProcessorTime').read().strip().split('\n')
   l=[]
   for i in tpc:
      j = i.strip().split()
      if len(j)>=2:
         usage = j[-1]
         name = ' '.join(j[:-1])
         if usage.isdigit():
            l.append([name, usage])
   l.sort(key= lambda l:int(l[1]), reverse=True)
   for i in range(len(l)):
      if int(l[i][1]) == 0:
         n = i
         break
   return l[:n]


def cpustatslin():
   ps = os.popen(r"ps -eo pid,comm,%cpu --sort=-%cpu | awk '$3 > 0.0'").read().strip().split('\n')
   l = []
   for i in ps[1:]:
      i.strip().split(' ')
      if len(i)>=3:
       cusage = i[-3:]
       cmnd = i[1:-3]
       pid = i[0]
       l.append([pid, cmnd, cusage])
   return l


def sysdeets():
    sos = os.name
    pf = platform.platform()
    return sos, pf

sos, pf = sysdeets()
if len(sos) > 0:
   print(f'Your OS is {pf} which is running a {sos} environment.')
while True: 
   if sos == 'nt':
     print('What do you want to know about your Windows system?\n')
     print('''
         1. Network Details
         2. Disk Statistics(Including largest 5 Directories)
         3. CPU Statistics
         4. All of the above''')
     a = int(input('\n Enter your choice number: '))
     if a == 1:
         pub, pri, dg = ipngatewaywin()
         print('Public IP: ', pub)
         print('Private IP: ', pri)
         print('Default Gateway: ', dg)
     elif a == 2:
         disk_volumes, freespace, usedspace, totalspace = distatswin()
         print('Data is showed in MB\n')
         print('disk', 'Total Space', 'Free Space', 'Used Space', sep='\t|\t')
         for i in range(len(disk_volumes)):
            print(disk_volumes[i], totalspace[i], freespace[i], usedspace[i], sep='\t|\t')
         d = input('Enter disk name u want to search directories in as stated above: ')
         e = d+r"\\"
         f = largestndir(5, e)
         print('Path', 'Size', sep='\t\t\t|\t\t')
         for i in f:
            print(i[0], i[1], sep='\t|\t')
         time.sleep(10)
     elif a == 3:
         g = totalcpuwin()
         for i in g:
            print(i, '%')
         print('Percent processor time might be higher than 100 for multi core CPU')
         print('\nProcess Name    |     PercentProcessorTime')
         h = processcputime()
         for i in h:
            print(i[0], i[1], sep='    |\t')
         time.sleep(10)
     elif a == 4:
         pub, pri, dg = ipngatewaywin()
         print('Public IP: ', pub)
         print('Private IP: ', pri)
         print('Default Gateway: ', dg)
         disk_volumes, freespace, usedspace, totalspace = distatswin()
         print('Data is showed in MB\n')
         print('disk', 'Total Space', 'Free Space', 'Used Space', sep='\t|\t')
         for i in range(len(disk_volumes)):
            print(disk_volumes[i], totalspace[i], freespace[i], usedspace[i], sep='\t|\t')
         d = input('Enter disk name u want to search directories in as stated above: ')
         e = d+ R"\\"
         f = largestndir(5, e)
         print('Path', 'Size', sep='\t\t\t|\t\t')
         for i in f:
            print(i[0], i[1], sep='\t|\t')
         g = totalcpuwin()
         for i in g:
            print(i, '%')
         print('Percent processor time might be higher than 100 for multi core CPU')
         print('\nProcess Name    |     PercentProcessorTime')
         h = processcputime()
         for i in h:
            print(i[0], i[1], sep='    |\t')
         time.sleep(10)
     else:
        break
   elif sos == 'posix':
      print('What do you want to know about your Unix system?\n')
      print('''
         1. Network Details
         2. Disk Statistics(Including largest 5 Directories)
         3. CPU Statistics
         4. All of the above''')
      a = int(input('\n Enter your choice number: '))
      if a == 1:
         pub, pri, dg = ipngatewaylin()
         print('Public IP: ', pub)
         print('Private IP: ', pri)
         print('Default Gateway: ', dg)
      elif a == 2:
         vol, freespace, usedspace, totalspace = distatlin()
         for i in range(len(vol)):
            print(vol[i], totalspace[i], freespace[i], usedspace[i], sep='|')
         b = largestdirlin()
         for i in b:
            print(i)
         time.sleep(10)
      elif a == 3:
         c = cpustatslin()
         print('pid', 'command', '%CPU', sep='  |  ')
         for i in c:
            print(i)
         time.sleep(10)
      elif a == 4:
         pub, pri, dg = ipngatewaylin()
         print('Public IP: ', pub)
         print('Private IP: ', pri)
         print('Default Gateway: ', dg)
         vol, freespace, usedspace, totalspace = distatlin()
         for i in range(len(vol)):
            print(vol[i], totalspace[i], freespace[i], usedspace[i], sep=' | ')
         b = largestdirlin()
         for i in b:
            print(i)
         c = cpustatslin()
         print('pid', 'command', '%CPU', sep='  |  ')
         for i in c:
            print(i)
         time.sleep(10)
      else:
         break
      
         

         



      
