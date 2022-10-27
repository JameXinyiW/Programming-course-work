import csv
import matplotlib.pyplot as plt
import datetime
import numpy as np
from pyecharts.charts import Geo
from pyecharts import  options as opts


class Datana():
    def __init__(self,area,path_head,path_tail):
        self.path=path_head+area+path_tail
        self.station = area
        self.number = []
        self.year = []
        self.month = []
        self.day = []
        self.hour = []
        self.PM25 = []
        self.PM10 = []
        self.SO2 = []
        self.NO2 = []
        self.CO = []
        self.zero3 = []
        self.temp = []
        self.pres = []
        self.dewp = []
        self.rain = []
        self.wd = []
        self.wspm = []

    def attr_get(self):
        with open(self.path) as csvfile:
            f = csv.DictReader(csvfile)
            for dic in f:
                self.number.append(dic['No'])
                self.year.append(dic['year'])
                self.month.append(dic['month'])
                self.day.append(dic['day'])
                self.hour.append(dic['hour'])
                self.PM25.append(dic['PM2.5'])
                self.PM10.append(dic['PM10'])
                self.SO2.append(dic['SO2'])
                self.NO2.append(dic['NO2'])
                self.CO.append(dic['CO'])
                self.zero3.append(dic['O3'])
                self.temp.append(dic['TEMP'])
                self.pres.append(dic['PRES'])
                self.dewp.append(dic['DEWP'])
                self.rain.append(dic["RAIN"])
                self.wd.append(dic['wd'])
                self.wspm.append(dic['WSPM'])

    def bytime(self,attr):
        lis_t = []
        for i in range(len(self.year)):
            time_str = self.year[i]+'-'+self.month[i]+'-'+self.day[i]+'-'+self.hour[i]
            timedate = datetime.datetime.strptime(time_str, '%Y-%m-%d-%H')
            lis_t.append(timedate)
        statis = eval('self'+'.'+attr)
        #print(statis)

        for i in range(len(statis)):
            if statis[i] == 'NA':
                statis[i] = -1
                lis_t[i] = -1
            statis[i] = float(statis[i])

        statis = list(filter(lambda x : x != -1, statis))
        lis_t = list(filter(lambda x: x != -1, lis_t))

        return statis,lis_t



class Visual(Datana):
    def __init__(self,areas,location,area,path_head,path_tail):
        super().__init__(area,path_head,path_tail)
        self.stations = areas
        self.location = location
        self.attr_get()
        self.path_head = path_head
        self.path_tail = path_tail

    def visual_by_time(self,attr):
        statis,lis_t = self.bytime(attr)
        plt.plot(lis_t, statis)
        plt.ylim(0, max(statis))
        new_ticks = np.linspace(0, max(statis), 10)
        plt.yticks(new_ticks)
        plt.xlabel('Time')
        plt.ylabel(f'Statistics of {attr} at {self.station}')
        plt.savefig(f'{attr},by time.jpg')
        plt.show()

    def visual_by_station(self,time,attr):
        s = {}
        g = (Geo(
            init_opts=opts.InitOpts(width="900px", height="900px",
                                    page_title=f'北京各观测点{time[0]}年{time[1]}月{time[2]}日{time[3]}时{attr}数据.html',
                                    bg_color="#404a59")
            # 颜色是str的16进制或英文都可以
        ).add_schema(
            maptype="china",  # 地图类型
            itemstyle_opts=opts.ItemStyleOpts(
                color="white"  # 背景颜色
                , border_color="black")  # 边界线颜色
        ))
        j = 0
        for station in self.stations:
            x = Datana(station,self.path_head,self.path_tail)
            x.attr_get()
            for i in range(len(x.year)):
                if x.year[i] == time[0]:
                    if x.month[i]  == time[1]:
                        if x.day[i]  == time[2]:
                            if x.hour[i]  == time[3]:
                                k = eval('x.' + attr)
                                s[station] = k[i]

            g.add_coordinate(station, self.location[j][0], self.location[j][1])

            g.add(series_name=attr, data_pair=[(station, s[station])], symbol_size=10, color="red", is_selected=True)
            j+=1
        g.render(f'北京各观测点{time[0]}年{time[1]}月{time[2]}日{time[3]}时{attr}数据.html')
        return

class NotNumError(ValueError):
    def __init__(self, region, year, month, day, hour, pollutant):
        self.year = year
        self.region = region
        self.month = month
        self.day = day
        self.hour = hour
        self.pollutant = pollutant
        self.message = f"NotNumError happen at {self.year}-{self.month}-{self.day} {self.hour}:00,pollutant is {self.pollutant},region is {self.region}"



def main():

    path_head = "D:\\pycharm code\\week7\\PRSA_Data_20130301-20170228\\PRSA_Data_"
    path_tail = "_20130301-20170228.csv"
    area = 'Dingling'
    areas=['Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan', 'Gucheng',
           'Huairou', 'Nongzhanguan', 'Shunyi', 'Tiantan', 'Wanliu', 'Wanshouxigong']
    #https://github.com/283567072n/station/blob/main/%E5%9B%BD%E6%8E%A7%E6%95%B0%E6%8D%AE.txt

    location=[[116.407,40.0031],[116.23,40.1952],[116.17,40.2865],[116.434,39.9522],[116.361,39.9425],[116.184,39.9136],
              [116.644,40.3937],[116.473,39.7916],[116.72,40.1438],[116.434,39.8745],[116.2878,39.9611],[116.366,39.8673]]

    attr = 'NO2'
    v = Visual(areas,location,area,path_head, path_tail)
    v.attr_get()
    v.visual_by_time(attr)
    t = ['2015','3','1','10']
    #v.visual_by_station(t,'NO2')


if __name__ == '__main__':
    main()


