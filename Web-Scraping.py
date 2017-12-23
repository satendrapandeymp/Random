import urllib2, time, sys, urllib, cookielib
from getpass import getpass
from bs4 import BeautifulSoup as Soup

reload(sys)
sys.setdefaultencoding("utf-8")

cj = cookielib.CookieJar()

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0')]

username = raw_input("username : ")
password = getpass()

opener.open('https://www.facebook.com/login')

login_data = urllib.urlencode({'email' : username, 'pass' : password})

opener.open('https://www.facebook.com/login', login_data)

# Done Authenticating till here

check = raw_input("to post on friend wall type p, to scrap mobile number type m and to scrap comments as .csv file type c : ")

# posting on wall
if check.lower() == 'p':

    person = raw_input("username of the person on which wall you want to post : ")
    
    test = opener.open('https://m.facebook.com/' + person)
    
    Page_Html = test.read()
    
    Parsed_html = Soup(Page_Html, "html.parser")
    
    form = Parsed_html.findAll("form")[1]
    
    inputs = form.findAll("input")
    
    message = raw_input("type message you want to post on his wall : ")
    
    data = {'xc_message' : message, 'view_post':'Post', 'rst_icv':''}
    data1 = data
    
    for i in range(8):
        data[str(inputs[i]['name'])] = str(inputs[i]['value'])
    
    link = 'https://m.facebook.com' + form['action']
    
    post_data = urllib.urlencode(data)
    
    test = opener.open(link, post_data)

elif check.lower() == 'm':
    
    
    arr = []
    arr1 = []
    baseurl = raw_input("put username of the person like satendrapandeymp : ")
    baseurl = 'https://m.facebook.com/' + baseurl
    arr.append(baseurl)

    
    File_name = "Data.csv"
    File_name1 = "Data1.csv"
    f = open(File_name, "w+")
    f.write("Name, B'Day, Gender, Home Town, Curr City, Mobile no. \n")  
    f.close()
    
    def final(url, Name, f, mutual):
        
        if 'id' in url:
            url1 = url.split("&")[0] 
            url = url1 + "&v=info"
        else:
            url1 = url.split("?")[0]
            url = url1 + "/about"
            
        if url in arr1:
            return 1
        else:
            arr1.append(url)
            
        response = opener.open(url)
        Page_Html = response.read()
        Parsed_html = Soup(Page_Html, "html.parser")
        
        Mobiles = Parsed_html.findAll("div", {"title":"Mobile"})    
        Genders = Parsed_html.findAll("div", {"title":"Gender"})  
        Birthdays = Parsed_html.findAll("div", {"title":"Birthday"})  
        Curr_citys = Parsed_html.findAll("div", {"title":"Current City"})  
        Home_towns = Parsed_html.findAll("div", {"title":"Hometown"})  
        
        flag = 0
        temp = ""
        
        for Mobile in Mobiles:
            Number = Mobile.findAll("td")[1].text
            Number = Number.replace(" ", "") + ","
            temp += Number
            flag = 1
        
        try:
            Gender = Genders[0].text
            Gender = Gender.split("ender")[1]
        except:
            Gender = "NA"
            
        try:
            Birthday = Birthdays[0].text
            Birthday = Birthday.split("irthday")[1].replace(',', "-")
        except:
            Birthday = "NA"
            
        try:
            Curr_city = Curr_citys[0].text
            Curr_city = Curr_city.split("urrent City")[1].replace(',', "-")
        except:
            Curr_city = "NA"
            
        try:
            Home_town = Home_towns[0].text
            Home_town = Home_town.split("ometown")[1].replace(',', "-")
        except:
            Home_town = "NA"
    
        print Curr_city, Home_town
    
        if flag == 1:
            f.write(Name + "," + Birthday + "," + Gender + "," + Home_town + "," + Curr_city + "," + temp + "\n" )

        
        if mutual > 10:
            
            if url1 not in arr:
                arr.append(url1)
            print url1
    
        return flag     
            
    def urlMaker(url):
        
        if 'id' in url:
            url = url.split("&")[0] + "&v=friends"
        else:
            url = url.split("?")[0] + "/friends"      
            
        return url
            
    def base(seed):     
            
        flag = 0
    
        while flag == 0:
            response = opener.open(seed)
            Page_Html = response.read()
            Parsed_html = Soup(Page_Html, "html.parser")
            
            Parsed_html = Parsed_html.findAll("div", {"id":"root"})[0]
        
            Details = Parsed_html.findAll("table", {"role":"presentation"})
            for Detail in Details:
                try:
                    Friend = Detail.findAll("a")[0]
                    mutuals = Detail.findAll("div")[0].text.split(' ')
                    mutual = 0
                    if len(mutuals)>0:
                        mutual = int(mutuals[0].strip())

                    test = final("https://m.facebook.com" + Friend["href"], Friend.text , f, mutual)
                except:
                    print "This person has deactivated his account" , Detail
            
            try:
                See_more = Parsed_html.findAll("div", {"id":"m_more_friends"}) 
                See_more = See_more[0]
                Next_page = See_more.findAll("a")[0]
                seed = 'https://m.facebook.com' + Next_page["href"]
                
            except:
                flag = 1
    
    count = 0
    while(count < 300):
        f = open(File_name1, "w")      
        test = arr[count]
        test = urlMaker(test)
        base(test)
        f.close()
        f1 = open(File_name1, "r") 
        test = f1.read()
        f1.close()
        f = open(File_name, "a")
        f.write(test)
        f.close()        
        count += 1
        time.sleep(100)
            
    print arr, arr1
    print len(arr), len(arr1)

# for comments details scrapping

elif check == 'c':
    
    id = raw_input("Type the page id : ")
    story_fbid = raw_input("Type the post id : ")
    
    seed = "https://m.facebook.com/story.php?story_fbid=" + str(story_fbid) + "&id=" + str(id)  
    flag = 0
    
    File_name = "Data.csv"
    f = open(File_name, "w+")
    f.write("Name, Link, Comment, Likes \n") 
    
    while flag == 0:
        response = opener.open(seed)
        Page_Html = response.read()
        Parsed_Html = Soup(Page_Html, "html.parser")
        
        more = 'see_next_' + str(story_fbid)
        try:
            Parsed_html = Parsed_Html.findAll("div", {"id":more})[0]
            key =  Parsed_html['class'][0]
            more_comment = Parsed_html.findAll("a")[0]
            seed = 'https://m.facebook.com' + more_comment['href']
        except:
            flag = 1    
        
        if flag == 0:
            Parsed_htmls = Parsed_Html.findAll("div", {"class":key})
        else:
            Parsed_htmls = Parsed_Html.findAll("div", {"class":'do'}) + Parsed_Html.findAll("div", {"class":'dp'}) + Parsed_Html.findAll("div", {"class":'dh'})
            
        for Parsed_html in Parsed_htmls:
            try:
                Detail = Parsed_html.findAll("a")[0]
                name = Detail.text
                url = Detail['href']
                print url
                if '?id' in url:
                    url = url.split("&")[0]
                else:
                    url = url.split("?")[0]
                Comment = Parsed_html.findAll("div")[1].text.replace(',','-')
                Support = Parsed_html.findAll("div")[3]
                likes = Support.findAll("a")[0].text
                if likes == 'Like':
                    likes = str(0)
                f.write(name + ' , ' + url + ' , ' + Comment + ' , ' + likes + "\n")
            except:
                cool = 'cool'
            
    f.close()
