import requests
import sys
import multiprocessing

#function to check for one url
def check_one_url():
    url_input = input("Enter url you want to check: ")
    print(url_input)
    r = requests.get('https://web.archive.org/cdx/search/xd?url='+url_input)
    if (r.status_code != 200):
        return 
    arr=[]
    print("Result")
    for line in r.text.splitlines():
        arr.append(line)
    if (arr ==[]):
        return 
    link_arr=[]
    status_arr=[]
    for i in arr:
        link_arr.append(i.split()[1])
        status_arr.append(i.split()[4])

    num=0
    ok_arr=[]
    while num < len(status_arr):
       if status_arr[num] != '403' and status_arr[num]!= '500' and status_arr[num] != '404' and status_arr[num] != '401' and status_arr[num] != '301':
            ok_arr.append(num)
       num=num+1

    list_of_link=[]
    if (ok_arr == []):
        print ("nothing here")
        return
    else:
        print("there is "+str(len(ok_arr))+" file in waybackmachine that has content for " + url_input+"\n")
        print("Time range from : " + link_arr[0] + " to " +link_arr[len(ok_arr)-1])
        print("\nHere all the link from waybackmachine\n")
        for i in ok_arr:
            list_of_link.append('https://web.archive.org/web/'+link_arr[i]+'/'+url_input)
    
        for i in list_of_link:
            print(i)

#fucntion to check file as input
def process_link(url):
    r = requests.get('https://web.archive.org/cdx/search/xd?url='+url)
    if (r.status_code != 200):
        return 
    new_arr=[]
    for line in r.text.splitlines():
        new_arr.append(line)
    if (new_arr == []):
        return 
    link_arr=[]
    status_arr=[]
    for i in new_arr:
        link_arr.append(i.split()[1])
        status_arr.append(i.split()[4])
    num=0
    ok_arr=[]
    while num < len(status_arr):
       if status_arr[num] != '403' and status_arr[num]!= '500' and status_arr[num] != '404' and status_arr[num] != '401' and status_arr[num] != '301':
            ok_arr.append(num)
       num=num+1
    list_of_link=[]
    if (ok_arr == []):
        return
    else:
        for i in ok_arr:
            list_of_link.append('https://web.archive.org/web/'+link_arr[i]+'/'+url)
        output = open("way_back_output.txt","a+")
        output_link =[]
        n=0
        for i in list_of_link:
            output.write(i)
            output.write("\n")
        output.close()
           
#Code for cmd input       
if __name__ == "__main__":
    if sys.argv[1] == "-h":
        print("help menu\n")
        print("use -u for one url\n")
        print("use -f for a file input")
    if sys.argv[1] == "-u":    
        check_one_url()
    if sys.argv[1] == "-f":
        #process file input first
        file_lines=[]
        path = sys.argv[2]
        print("input from "+path)
        with open(path,'r') as f:
            file_lines = f.readlines()
        processes = []
        for i in file_lines:
            p = multiprocessing.Process(target=process_link, args=(i,))
            processes.append(p)
            p.start()

        for process in processes:
            process.join()

            
