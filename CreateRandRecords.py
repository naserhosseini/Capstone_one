import csv
from os.path import exists
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

#Open the cofiguration file
with open('init.cong','r') as cnfg:
    s=cnfg.readline()
    s=s.split('|')
    s[1]=s[1].strip()
    StartDate=datetime.strptime(s[1], '%Y/%m/%d %H:%M:%S')


RT=pd.read_csv('RT.csv')
RT=RT.replace(np.nan,'')
Start=datetime.now()
Product=['Cake','Cookies','CupCake']
Cake=['8X6','10X8','6X4','6','8','10']
Cookies=['Small','Large']
Flavour=['chocolate','vanilla','strawberry','coconut','lemon','carrot','red velvet','pineapple','rainbow']
inc=2
while StartDate < datetime.now():
    i=0
    year=StartDate.year
    month='{:02d}'.format(StartDate.month)
    name='_'+year.__str__()+'_'+month
    ConsumeCSV='../Consume{}.csv'.format(name)
    Consume_Flag=exists(ConsumeCSV)
    SellsCSV = '../Sells{}.csv'.format(name)
    SellsFlag=exists(SellsCSV)
    PurchaseCSV = '../Purchase{}.csv'.format(name)
    PurchasFlag=exists(PurchaseCSV)
    with open(PurchaseCSV, 'a', newline='') as Purchase:
        purchase = csv.writer(Purchase)
        if not PurchasFlag:
            purchase.writerow(['Date', 'MIX', 'Milk', 'Egg', 'Oil', 'Fondant', 'Sugar', 'Butter', 'Flavour', 'Flour'])
        with open(ConsumeCSV, 'a', newline='') as Consume:
            consume = csv.writer(Consume)
            if not Consume_Flag:
                consume.writerow(['Date','MIX','Milk','Egg','Oil','Fondant','Sugar','Butter','Flavour','Flour'])
            with open(SellsCSV, 'a', newline='') as Sells:
                sells = csv.writer(Sells)
                if not SellsFlag:
                    sells.writerow(['Date','Product','Type','Quantities','Customer_FK'])
                while month=='{:02d}'.format(StartDate.month) and StartDate < datetime.now():
                    Purchasedate=StartDate-timedelta(weeks=1)
                    product = random.randint(0, 2)
                    cake = random.randint(0, 5)
                    flavour = random.randint(0, 8)
                    cupcake = random.randint(0, 8)
                    cookies = random.randint(0, 1)
                    customer = random.randint(1, 142)
                    count=random.randint(1, 4)
                    if product==0:
                        strSell=[StartDate.date(), 'Cake',Flavour[flavour]+' '+Cake[cake],1,customer]
                        strConsume=(RT[RT['Size']==Cake[cake]]).values.tolist()[0][1:]
                        strConsume[-2]=Flavour[flavour]
                    else:
                        if product==1:
                            strSell=[StartDate.date(),'Cookies',Cookies[cookies],count,customer]
                            strConsume = (RT[RT['Size'] == Cookies[cookies]] * count).values.tolist()[0][1:]
                        else:
                            strSell=[StartDate.date(),'Cupcakes',Flavour[cupcake], count,customer]
                            strConsume = (RT[RT['Size'] == 'Cupcakes']*count).values.tolist()[0][1:]
                            strConsume[-2] = Flavour[flavour]
                    strConsume.insert(0,StartDate.date())
                    strPurchase=strConsume
                    sells.writerow(strSell)
                    consume.writerow(strConsume)
                    strPurchase[0]=Purchasedate.date()
                    i+=1
                    purchase.writerow(strPurchase)
                    print('Item number {} is at {}!'.format(i,StartDate))
                    StartDate += timedelta(seconds=inc)
                Sells.close()
            Consume.close()
with open('init.cong','w',newline='') as cnfg:
    cnfg.writelines('start| {}'.format(StartDate.strftime('%Y/%m/%d %H:%M:%S')))
print('Total run time is {}'.format(datetime.now()-Start))

