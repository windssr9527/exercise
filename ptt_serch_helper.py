import wx
import time
import requests
from bs4 import BeautifulSoup
import re
import threading
import matplotlib.pyplot as plt
from matplotlib import font_manager

class WXFrame(wx.Frame):

    def __init__(self, parent, title):
        super(WXFrame, self).__init__(parent, title=title,
            size=(700, 850))
        
        print("正在載入程序...")
        self.InitUI()
        self.Centre()
        self.Show()
        print("載入完成")

    def InitUI(self):
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
        ptt_main_url="https://www.ptt.cc/bbs/index.html"
        main_re=requests.get(ptt_main_url,cookies={"over18":"1"},headers=self.headers)
        self.kanban_dict={}
        kanban_href=[]
        kanban_name=[]
        self.datedict={}
        main_soup = BeautifulSoup(main_re.text,'lxml')
        
        for i in main_soup.find_all("a",class_="board"):
            kanban_href.append(i["href"])
        
        for i in main_soup.find_all("div",class_="board-name"):
            kanban_name.append(i.text)
        
        for i in range(len(kanban_name)):
           self.kanban_dict[kanban_name[i]]=kanban_href[i]
           
        
        
        '''設定介面'''
        panel = wx.Panel(self)

        hbox = wx.BoxSizer(wx.VERTICAL)

        #设置为2行4列
        fgs = wx.FlexGridSizer(1, 8, 1, 10)

        Text1 = wx.StaticText(panel, label="看板分類:", style= wx.ALIGN_RIGHT)
        Text2 = wx.StaticText(panel, label="搜尋數量:", style= wx.ALIGN_RIGHT)
        Text3 = wx.StaticText(panel, label="人氣:", style= wx.ALIGN_RIGHT)
        Textspace1 = wx.StaticText(panel, label="      ")
        Textspace2 = wx.StaticText(panel, label="      ")
        Text4 = wx.StaticText(panel, label="關鍵字:", style= wx.ALIGN_RIGHT)
        self.kanban_textctrl = wx.ComboBox(panel,choices=kanban_name,size=(100,25))
        self.num_textctrl = wx.TextCtrl(panel,size=(100,25))
        self.num_textctrl.AppendText("10")
        self.hot_textctrl = wx.TextCtrl(panel,size=(100,25))
        self.hot_textctrl.AppendText("0")
        self.key_textctrl = wx.TextCtrl(panel,size=(300,25))
        self.result_textctrl = wx.TextCtrl(panel,style=wx.TE_MULTILINE | wx.TE_READONLY,size=(600,525))

        fgs.AddMany(
                    [(Text1, 0, wx.ALIGN_RIGHT), (self.kanban_textctrl, 0, wx.SHAPED),(Textspace1, 0, wx.SHAPED), (Text2, 0, wx.ALIGN_RIGHT), (self.num_textctrl, 0, wx.SHAPED),(Textspace2, 0, wx.SHAPED),
                     (Text3, 0, wx.ALIGN_RIGHT), (self.hot_textctrl, 0, wx.SHAPED)])
        
        
        fgs2 = wx.FlexGridSizer(1, 2, 1, 10)
        
        fgs2.AddMany([(Text4, 0, wx.ALIGN_RIGHT),(self.key_textctrl, 0, wx.SHAPED)])


        self.btn_start=wx.Button(panel, label="開始搜尋")
        self.btn_image= wx.Button(panel, label="日期圖表")
        self.btn_cancel=wx.Button(panel, label="停止搜尋")
        self.btn_start.SetMinSize((200,80))
        self.btn_image.SetMinSize((200,80))
        self.btn_cancel.SetMinSize((200,80))
        
        fgs3 = wx.FlexGridSizer(1, 3, 9, 25)
        fgs3.AddMany([(self.btn_start, 0, wx.SHAPED),(self.btn_image, 0, wx.SHAPED),(self.btn_cancel, 0, wx.SHAPED)])
        
        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        hbox.Add(fgs2, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        hbox.Add(self.result_textctrl,proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        hbox.Add(fgs3, proportion=1, flag=wx.ALL|wx.CENTER, border=15)

        panel.SetSizer(hbox)
        self.Bind(wx.EVT_BUTTON, self.on_start, self.btn_start)
        self.Bind(wx.EVT_BUTTON, self.on_image, self.btn_image)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.btn_cancel)
        
        '''設定菜單'''
        menubar = wx.MenuBar()
        help_menu = wx.Menu()
        about_menu = wx.Menu()
        
        help_item = help_menu.Append(wx.ID_HELP, '帮助', '帮助信息')
        about_item = about_menu.Append(wx.ID_ABOUT, '关于', '关于信息')
        
        menubar.Append(help_menu, '帮助')
        menubar.Append(about_menu, '关于')
        
        self.SetMenuBar(menubar)
        
        self.Bind(wx.EVT_MENU, self.on_help, help_item)
        self.Bind(wx.EVT_MENU, self.on_about, about_item)
        
        
    def on_start(self, event):
        kanban_value = self.kanban_textctrl.GetValue()
        num_value=self.num_textctrl.GetValue()
        hot_value=self.hot_textctrl.GetValue()
        key_value=self.key_textctrl.GetValue()
        if '|' in kanban_value and '&' in kanban_value:
            wx.MessageBox('請勿將&和|一起使用', '信息', wx.OK | wx.ICON_INFORMATION)
            return
        if  kanban_value==None or kanban_value not in self.kanban_dict:
            wx.MessageBox('選擇看板錯誤 請使用選項選擇看板', '信息', wx.OK | wx.ICON_INFORMATION)
            return
        if  num_value==None or not num_value.isdigit() or int(num_value)<1 :
            wx.MessageBox('搜尋筆數輸入錯誤 請輸入正整數', '信息', wx.OK | wx.ICON_INFORMATION)
            return
        if  hot_value==None or not hot_value.isdigit() or int(hot_value)<0 or int(hot_value)>100 :
            wx.MessageBox('最低人氣輸入錯誤 應為0~100的整數', '信息', wx.OK | wx.ICON_INFORMATION)
            return
        if '|' in key_value or key_value=='':
            threading.Thread(target=self.on_run_or).start()
        else:
            threading.Thread(target=self.on_run).start() 


    def on_run(self):
        kanban_value = self.kanban_textctrl.GetValue()
        num_value=self.num_textctrl.GetValue()
        hot_value=self.hot_textctrl.GetValue()
        key_value=self.key_textctrl.GetValue()
        key_list=key_value.split("&")
        try:
            print("正在準備")
            self.btn_start.Disable()
            self.btn_image.Disable()
            self.result_textctrl.Clear();
            self.cancel=False
            url_start="https://www.ptt.cc"
            url_end=self.kanban_dict[kanban_value]
            sub_re=requests.get(url_start+url_end, cookies={"over18":"1"},headers=self.headers)
            sub_soup=BeautifulSoup(sub_re.text,'lxml')
            
            page=1

            self.datedict={}
            count=0
            url_min_num=2147483647
            url_min_index=0
            if len(key_list)>1:
                for i in range(len(key_list)):
                    url_test=url_start+'/'.join(url_end.split("/")[:-1])+"/search?page={}&q={}".format(page,key_list[i])
                    r=requests.get(url_test,cookies={"over18":"1"},headers=self.headers)
                    souptest=BeautifulSoup(r.text,'lxml')
                    souptest1=souptest.find("div",class_="btn-group btn-group-paging")
                    comparekey=re.search("page=\d+", souptest1.find("a")["href"]).group().split("=")[-1]
                    if int(comparekey)<url_min_num:
                        url_min_num=int(comparekey)
                        url_min_index=i
                key_temp=key_list[0]
                key_list[0]=key_list[url_min_index]
                key_list[url_min_index]=key_temp
                
            print("開始搜尋")
            while(True):
                print("page="+str(page))
                url2=url_start+'/'.join(url_end.split("/")[:-1])+"/search?page={}&q={}".format(page,key_list[0])
                print(url2)
                r=requests.get(url2,cookies={"over18":"1"},headers=self.headers)
                if r.status_code==requests.codes.ok:
                    r.encoding="utf8"
                    soup=BeautifulSoup(r.text,"lxml")
                    tag_divs=soup.find_all("div",class_="r-ent")
                    for tag in tag_divs:
                        tag_a=tag.find("a")
                        if tag_a == None:
                            continue
                        if not all(sub in tag_a.text for sub in key_list[1:]):
                            continue
                        if int(hot_value)!=0:
                            if tag.find("span")==None:
                                continue
                            if tag.find("span").text!="爆" and (not tag.find("span").text.isdigit() or int(hot_value)>int(tag.find("span").text)):
                                continue
                        date_tag=tag.find("div",class_="date").text
                        if date_tag in self.datedict and next(reversed(self.datedict))!=date_tag:
                            date_tag='-f'+date_tag
                        if date_tag in self.datedict:
                            self.datedict[date_tag]+=1
                        else:
                            self.datedict[date_tag]=1
                        self.result_textctrl.WriteText("網址: "+url_start+tag_a["href"]+"\n")
                        self.result_textctrl.WriteText("標題: "+tag_a.text+"\n")
                        count+=1
                        self.result_textctrl.WriteText("========="+str(count)+"========="+"\n")
                        if count>=int(num_value):
                            break
                    if count>=(int(num_value)):
                        break
                    time.sleep(1)
                else:
                    self.result_textctrl.WriteText("Http:錯誤 可能已經搜尋完所有資料\n")
                    break
                page+=1
                if self.cancel:
                        break
            
            self.finish()
        except Exception as e:
            print(e)
            self.finish()
            wx.MessageBox('出現不明錯誤 可能為網路問題 請稍後在試', '信息', wx.OK | wx.ICON_INFORMATION)
    
    def on_run_or(self):
        kanban_value = self.kanban_textctrl.GetValue()
        num_value=self.num_textctrl.GetValue()
        hot_value=self.hot_textctrl.GetValue()
        key_value=self.key_textctrl.GetValue()
        key_list=key_value.split("|")
        try:
            print("開始搜尋")
            self.btn_start.Disable()
            self.btn_image.Disable()
            self.result_textctrl.Clear();
            self.cancel=False
            url_start="https://www.ptt.cc"
            url_end=self.kanban_dict[kanban_value]
            sub_re=requests.get(url_start+url_end, cookies={"over18":"1"},headers=self.headers)
            sub_soup=BeautifulSoup(sub_re.text,'lxml')
            
            soup_checkpage=sub_soup.find("div",class_="btn-group btn-group-paging")
            soup_checkpage=soup_checkpage.find_all("a")
    
            page=0
            for i in soup_checkpage:  
                if i.text=="‹ 上頁":
                    page = int(re.search(r'\d+', i["href"].split("/")[-1]).group())+1
            
            self.datedict={}
            count=0
            if page!=0:
                while(True):
                    print("page="+str(page))
                    url2=url_start+url_end.split(".")[0]+str(page)+".html"
                    r=requests.get(url2,cookies={"over18":"1"},headers=self.headers)
                    if r.status_code==requests.codes.ok:
                        r.encoding="utf8"
                        soup=BeautifulSoup(r.text,"lxml")
                        tag_divs=soup.find_all("div",class_="r-ent")
                        for tag in tag_divs:
                            tag_a=tag.find("a");
                            if tag_a == None:
                                continue
                            if not any(sub in tag_a.text for sub in key_value.split("|")):
                                continue
                            if int(hot_value)!=0:
                                if tag.find("span")==None:
                                    continue
                                if tag.find("span").text!="爆" and (not tag.find("span").text.isdigit() or int(hot_value)>int(tag.find("span").text)):
                                    continue
                            date_tag=tag.find("div",class_="date").text
                            if date_tag in self.datedict:
                                self.datedict[date_tag]+=1
                            else:
                                self.datedict[date_tag]=1
                            self.result_textctrl.WriteText("網址: "+url_start+tag_a["href"]+"\n")
                            self.result_textctrl.WriteText("標題: "+tag_a.text+"\n")
                            count+=1
                            self.result_textctrl.WriteText("========="+str(count)+"========="+"\n")
                            if count>=int(num_value):
                                break
                        if count>=(int(num_value)):
                            break
                        time.sleep(1)
                    else:
                        time.sleep(0.5)
                        self.result_textctrl.WriteText("Http:錯誤 可能已經搜尋完所有資料")
                        self.finish()
                        break
                    page-=1
                    if self.cancel:
                            break
            else:
                self.result_textctrl.WriteText("獲取最新頁碼失敗")
                self.finish()
            
            self.finish()
        except Exception as e:
            print(e)
            wx.MessageBox('出現不明錯誤 可能為網路問題 請稍後在試', '信息', wx.OK | wx.ICON_INFORMATION)
    
    
    def finish(self):
        self.btn_start.Enable()
        self.btn_image.Enable()
        self.result_textctrl.WriteText("搜尋結束")
        
        if not self.datedict:
            return
        else:
            print(self.datedict)
        
        self.datedict=dict(reversed(list(self.datedict.items())))
        
        
        fig_width=7
        if(len(self.datedict))>10:
            fig_width+=((len(self.datedict)/10)-1)*0.13*fig_width
            print(fig_width)
            plt.figure(figsize=(fig_width,5))

        plt.bar(self.datedict.keys(), self.datedict.values())
        
        #尋找字體名稱
        for font in  font_manager.fontManager.ttflist:
            if font.fname.split('\\')[-1]=='msyh.ttc':
                fname=font.name
          
                    
        #設定字體
        plt.rcParams['font.sans-serif'] = [fname]
        # 設置標題和標籤
        plt.title('推文的日期與數量')
        
        #設定y軸間隔
        ax=plt.gca()
        if max(self.datedict.values())>20:
            ax.yaxis.set_major_locator(plt.MultipleLocator(max(self.datedict.values())//10)) 
        else:
            ax.yaxis.set_major_locator(plt.MultipleLocator(1))
            
        if(len(self.datedict))>10:
            plt.xticks(rotation=90)
        plt.xlabel('日期')
        plt.ylabel('數量')
        plt.tight_layout()
        plt.savefig("ptt_search_image.jpg",dpi=80,bbox_inches = 'tight')
        plt.close()


    def on_image(self, event):
        if not self.datedict:
            wx.MessageBox('請先搜尋貼文', '信息', wx.OK | wx.ICON_INFORMATION)
            return
        
        
        image_path = "ptt_search_image.jpg"  # 圖片路徑
        new_frame = ImageFrame(None, title="顯示圖片", image_path=image_path,dictlen=len(self.datedict))
        new_frame.Show(True)

    def on_cancel(self, event):
        self.cancel=True
    def on_help(self, event):
        wx.MessageBox('\n看板分類:建議使用下拉選項選擇\n\n搜尋數量:請輸入正整數\n\n 人氣:文章的最小人氣值，範圍為0~100，如為100，只會搜尋人氣為"爆"的文章\n\n關鍵字:文章標題內含的文字，可使用&或|分隔，例:a&b將搜尋包含a和b的文章，a|b將搜尋內含a或內含b的文章\n\n注:1.&和|不可一起使用 2.|效率低下不建議使用 3.日期不分年份 4.日期前面有-f表示該日期之前已經出現過但非同一年份', '帮助', wx.OK | wx.ICON_INFORMATION)

    def on_about(self, event):
        wx.MessageBox('作者:詹心維\n版本:1.0。', '关于', wx.OK | wx.ICON_INFORMATION)
        
class ImageFrame(wx.Frame):
    def __init__(self, parent, title, image_path,dictlen):
        size_width=650
        if dictlen>10:
            size_width+=((dictlen/10)-1)*0.13*size_width
            
        print(size_width)
        super(ImageFrame, self).__init__(parent, title=title, size=(int(size_width),700))
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        image = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
        image_bitmap = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(image))

        sizer.Add(image_bitmap, 1, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(sizer)


if __name__ == '__main__':

    app = wx.App()
    WXFrame(None, title='ptt搜尋助手v1')
    app.MainLoop()