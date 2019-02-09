import csv
import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import ttk
from copy import deepcopy
import sys

with open('五彩石.csv', 'r') as f:
    data = csv.reader(f)
    data = list(data)[1:]

attr = []

BASEATTR = 34


def select_zy(event):
    temp = combox.get()
    if temp in ('紫霞','冰心','毒经','莫问'):
        lab[6]['text'] = '根骨:'
    elif temp in ('傲血','惊羽','丐帮','霸刀'):
        lab[6]['text'] = '力道:'
    elif temp in ('太虚','藏剑','分山','蓬莱'):
        lab[6]['text'] = '身法:'
    elif temp in ('花间','易筋','天罗','焚影'):
        lab[6]['text'] = '元气:'
    else:
        raise KeyError

def do_pct():
    if pct.get(): # 使用百分比输入法
        lab[3]['text'] = '破防率(%):'
        lab[4]['text'] = '会心率(%):'
        lab[5]['text'] = '会效率(%):'
        s_pf.set('0.0')
        s_hx1.set('0.0')
        s_hx2.set('175.0')
        l_info['text'] = '请注意:输入百分比来计算可能会造成误差'
        root.after(3000, deshow)
    else:
        lab[3]['text'] = '破防等级:'
        lab[4]['text'] = '会心等级:'
        lab[5]['text'] = '会效等级:'
        s_pf.set('0')
        s_hx1.set('0')
        s_hx2.set('0')

def dett(a, isfloat):
    try:
        if isfloat:
            a = float(a)
        else:
            a = int(a)
    except ValueError:
        return True
    return False

def detect():
    if dett(s_gjl.get(), False):
        return True
    if dett(s_pf.get(), pct.get()):
        return True
    if dett(s_hx1.get(), pct.get()):
        return True
    if dett(s_hx2.get(), pct.get()):
        return True
    if dett(s_attr.get(), False):
        return True
    return False

def deshow():
    l_info['text'] = ''

def select_attrs():
    if not is_attr.get():
        l_info['text'] = '请注意:基础属性加成五彩石价格都非常高'
        root.after(3000, deshow)

def calc():
    if detect():
        msgbox.showwarning('警告','您填写的某些数字格式不对')
        return None
    ex_att = att = float(s_gjl.get())
    ex_de_defence = de_defence = float(s_pf.get()) # 0.006512倍 -> 破防率
    ex_crit_poss = crit_poss = float(s_hx1.get()) # 0.006515倍 -> 会心率(%)
    ex_crit_power = crit_power = float(s_hx2.get()) # 0.018625倍 -> 会效(%)
    ex_weapon_att = weapon_att = 0 
    ex_shenfa = shenfa = 0 # 0.28倍 -> 会心等级
    ex_lidao = lidao = 0 # 0.15倍 -> 攻击  0.3倍 -> 破防
    ex_yuanqi = yuanqi = 0 # 0.18倍 -> 攻击 0.3倍 -> 破防
    ex_gengu = gengu = 0 # 0.64倍 -> 会心等级

    zy = combox.get()
    wg = zy in ('太虚','藏剑','傲血','惊羽','丐帮','分山','霸刀','蓬莱')

    if zy in ('紫霞','冰心','毒经','莫问'):
        ex_lidao = lidao = BASEATTR
        ex_shenfa = shenfa = BASEATTR
        ex_yuanqi = yuanqi = BASEATTR
        ex_gengu = gengu = int(s_attr.get())
    elif zy in ('傲血','惊羽','丐帮','霸刀'):
        ex_lidao = lidao = int(s_attr.get())
        ex_shenfa = shenfa = BASEATTR
        ex_yuanqi = yuanqi = BASEATTR
        ex_gengu = gengu = BASEATTR
    elif zy in ('太虚','藏剑','分山','蓬莱'):
        ex_lidao = lidao = BASEATTR
        ex_shenfa = shenfa = int(s_attr.get())
        ex_yuanqi = yuanqi = BASEATTR
        ex_gengu = gengu = BASEATTR
    elif zy in ('花间','易筋','天罗','焚影'):
        ex_lidao = lidao = BASEATTR
        ex_shenfa = shenfa = BASEATTR
        ex_yuanqi = yuanqi = int(s_attr.get())
        ex_gengu = gengu = BASEATTR

    if pct.get(): # 百分比输入法
        crit_poss = crit_poss/0.006515
        crit_power = (crit_power-175)/0.018625
        de_defence = de_defence/0.006512


    new_data = []
    for each in data:
        attr = [(each[2],each[3]),(each[4],each[5]),(each[6],each[7])]
        tetr = (each[2],each[4],each[6])
        if need_hj.get() and '化劲' not in tetr:
            continue # 无化劲
        if need_yj.get() and '御劲' not in tetr:
            continue # 无御劲
        if need_mz.get():
            flag = False
            for n in tetr:
                if '命中' in n:
                    flag = True
                    break
            if not flag: # 无命中
                continue
        if is_attr.get():
            flag = True
            for n in tetr:
                if n=='全属性' or '基础' in n:
                    flag = False
                    break
            if not flag:
                continue
        
        ex_att = att
        ex_crit_poss = crit_poss
        ex_crit_power = crit_power
        ex_de_defence = de_defence
        ex_weapon_att = weapon_att
        ex_shenfa = shenfa
        ex_lidao = lidao
        ex_yuanqi = yuanqi
        ex_gengu = gengu

        
        for a,v in attr:
            v = int(v)
            if wg:
                if a == '外功·攻击':
                    ex_att += v
                elif a == '外功·会心':
                    ex_crit_poss += v
                elif a == '外功·会效':
                    ex_crit_power += v
                elif a == '外功·破防':
                    ex_de_defence += v
                elif a == '外功·武器伤害':
                    ex_weapon_att += v
                elif a == '基础·力道':
                    #ex_lidao += v
                    ex_att += 0.15*v
                    ex_de_defence += 0.3*v
                    if zy == '霸刀':
                        ex_att += 1.55*v
                        ex_de_defence += 0.36*v
                    elif zy == '惊羽':
                        ex_att += 1.45*v
                        ex_crit_poss += 0.59*v
                    elif zy == '傲血':
                        ex_att += 1.6*v
                        ex_de_defence += 0.25*v
                    elif zy == '丐帮':
                        ex_att += 1.55*v
                        ex_de_defence += 0.36*v
                elif a == '基础·身法':
                    #ex_shenfa += v
                    ex_crit_poss += 0.28*v
                    if zy == '蓬莱':
                        ex_att += 1.55*v
                        ex_crit_poss += 0.36*v
                    elif zy == '藏剑':
                        ex_att += 1.6*v
                        ex_de_defence += 0.25*v
                    elif zy == '分山':
                        ex_att += 1.71*v
                    elif zy == '剑纯':
                        ex_att += 1.45*v
                        ex_crit_poss += 0.58*v
            else:
                if len(a)>3 and a[:2] == '内功':
                    if a[3:] == '攻击':
                        ex_att += v
                    elif a[3:] == '会心':
                        ex_crit_poss += v
                    elif a[3:] == '会效':
                        ex_crit_power += v
                    elif a[3:] == '破防':
                        ex_de_defence += v
                elif len(a)>3 and a[:2] == '毒性' and zy in ('毒经','天罗'):
                    if a[3:] == '攻击':
                        ex_att += v
                    elif a[3:] == '会心':
                        ex_crit_poss += v
                    elif a[3:] == '会效':
                        ex_crit_power += v
                    elif a[3:] == '破防':
                        ex_de_defence += v
                elif len(a)>3 and a[:2] == '混元' and zy in ('紫霞','花间'):
                    if a[3:] == '攻击':
                        ex_att += v
                    elif a[3:] == '会心':
                        ex_crit_poss += v
                    elif a[3:] == '会效':
                        ex_crit_power += v
                    elif a[3:] == '破防':
                        ex_de_defence += v
                elif len(a)>3 and a[:2] == '阴性' and zy in ('冰心','莫问'):
                    if a[3:] == '攻击':
                        ex_att += v
                    elif a[3:] == '会心':
                        ex_crit_poss += v
                    elif a[3:] == '会效':
                        ex_crit_power += v
                    elif a[3:] == '破防':
                        ex_de_defence += v
                elif len(a)>3 and a[:2] == '阳性' and zy == '易筋':
                    if a[3:] == '攻击':
                        ex_att += v
                    elif a[3:] == '会心':
                        ex_crit_poss += v
                    elif a[3:] == '会效':
                        ex_crit_power += v
                    elif a[3:] == '破防':
                        ex_de_defence += v
                elif len(a)>3 and a[:2] == '阴阳' and zy == '焚影':
                    if a[3:] == '攻击':
                        ex_att += v
                    elif a[3:] == '会心':
                        ex_crit_poss += v
                    elif a[3:] == '会效':
                        ex_crit_power += v
                    elif a[3:] == '破防':
                        ex_de_defence += v
                elif a == '基础·元气':
                    #ex_yuanqi += v
                    ex_att += 0.18*v
                    ex_de_defence += 0.3*v
                    if zy == '花间':
                        ex_att += 1.95*v
                        ex_de_defence += 0.19*v
                    elif zy == '易筋':
                        ex_att += 1.85*v
                        ex_crit_poss += 0.38*v
                    elif zy == '天罗':
                        ex_att += 1.75*v
                        ex_crit_poss += 0.57*v
                    elif zy == '焚影':
                        ex_att += 1.9*v
                        ex_crit_poss += 0.29*v
                elif a == '基础·根骨':
                    #ex_gengu += v
                    ex_crit_poss += 0.64*v
                    if zy == '紫霞':
                        ex_att += 1.75*v
                        ex_crit_poss += 0.56*v
                    elif zy == '冰心':
                        ex_att += 1.9*v
                        ex_cri_poss += 0.28*v
                    elif zy == '毒经':
                        ex_att += 1.95*v
                        ex_de_defence += 0.19*v
                    elif zy == '莫问':
                        ex_att += 1.85*v
                        ex_crit_poss += 0.38*v

        temp = {'att': ex_att,
                'crit_poss': ex_crit_poss,
                'crit_power': ex_crit_power,
                'de_defence': ex_de_defence,
                'weapon_att': ex_weapon_att,
                'shenfa': ex_shenfa,
                'lidao': ex_lidao,
                'yuanqi': ex_yuanqi,
                'gengu': ex_gengu}


        hx1 = ex_crit_poss * 0.006515 / 100
        hx2 = (175+0.018625*ex_crit_power)/100
        pf = ex_de_defence * 0.006512 / 100
        damage = ex_att * ((hx1*hx2)+1-hx1) * (1+pf)
        new_data.append((each[0],*each[2:],damage,temp,
                         {'att':ex_att,'hx1':hx1,'hx2':hx2,'pf':pf}))

    new_data.sort(key = lambda x:x[7], reverse = False)
    x = tree.get_children()
    for item in x:
        tree.delete(item)
    _index = 0
    for each in new_data[-10:]:
        _name = each[0]
        _attr1 = each[1]+' +'+each[2]
        _attr2 = each[3]+' +'+each[4]
        _attr3 = each[5]+' +'+each[6]
        _damage = '%.2f'%each[7]
        tree.insert('', _index, text='', values=(_name, _attr1, _attr2,
                                                 _attr3, _damage))
    



root = tk.Tk()
root.title('剑网三 最佳五彩石计算')
temp = ['门派心法','输入百分比','攻击力','破防等级','会心等级',
        '会效等级','根骨','五彩石限制']
lab = []
for i in range(len(temp)): # 标签
    lab.append(tk.Label(root, text=temp[i]+':'))
    lab[-1].grid(row=i, column=0)

l_info = tk.Label(root, text='', fg='red')
l_info.grid(row=10,column=3)

zhiye = tk.StringVar()
combox = ttk.Combobox(root, textvariable=zhiye, state='readonly') # 下拉菜单
combox['values'] = ('紫霞','太虚','花间','藏剑','傲血',
                    '易筋','冰心','毒经','天罗','惊羽',
                    '焚影','丐帮','分山','莫问','霸刀','蓬莱')
combox.bind('<<ComboboxSelected>>',select_zy)
combox.current(0)
combox.grid(row=0, column=1, columnspan=2) # 职业选择


pct = tk.IntVar()
pct.set(0)
check = tk.Checkbutton(root, text='输入破防率/会心率/会效率', variable=pct,
                       onvalue=1, offvalue=0, command=do_pct)
check.grid(row=1, column=1, columnspan=2)

s_gjl = tk.StringVar()
s_gjl.set('0')
t1 = tk.Entry(root, textvariable=s_gjl) # 攻击力
#t1.bind('<KeyRelease>',limit_1)
t1.grid(row=2, column=1, columnspan=2)

s_pf = tk.StringVar()
s_pf.set('0')
t2 = tk.Entry(root, textvariable=s_pf) # 破防
#t2.bind('<KeyRelease>',limit_2)
t2.grid(row=3, column=1, columnspan=2)

s_hx1 = tk.StringVar()
s_hx1.set('0')
t3 = tk.Entry(root, textvariable=s_hx1) # 会心
#t3.bind('<KeyRelease>',limit_3)
t3.grid(row=4, column=1, columnspan=2)

s_hx2 = tk.StringVar()
s_hx2.set('0')
t4 = tk.Entry(root, textvariable=s_hx2) # 会效
#t4.bind('<KeyRelease>',limit_4)
t4.grid(row=5, column=1, columnspan=2)

s_attr = tk.StringVar()
s_attr.set('0')
t5 = tk.Entry(root, textvariable=s_attr) # 属性
#t5.bind('<KeyRelease>',limit_5)
t5.grid(row=6, column=1, columnspan=2)

need_hj = tk.IntVar()
need_hj.set(0)
check2 = tk.Checkbutton(root, text='需含化劲', variable=need_hj,
                        onvalue=1, offvalue=0)
check2.grid(row=7, column=1)

need_yj = tk.IntVar()
need_yj.set(0)
check3 = tk.Checkbutton(root, text='需含御劲', variable=need_yj,
                        onvalue=1, offvalue=0)
check3.grid(row=7, column=2)

need_mz = tk.IntVar()
need_mz.set(0)
check4 = tk.Checkbutton(root, text='需含命中', variable=need_mz,
                        onvalue=1, offvalue=0)
check4.grid(row=8, column=1)

is_attr = tk.IntVar()
is_attr.set(1)
check5 = tk.Checkbutton(root, text='不选基础属性五彩石(价格贵)',
                        variable=is_attr, onvalue=1, offvalue=0,
                        command=select_attrs)
check5.grid(row=9, column=1, columnspan=2)

btn = tk.Button(root, text='计算最佳', command=calc)
btn.grid(row=10, column=0, columnspan=3)

tree = ttk.Treeview(root, show='headings')
tree['columns'] = ('name','attr1','attr2','attr3','damage')
tree.grid(row=0,column=3, rowspan=10)
tree.column('name', width=125)
tree.column('attr1', width=100)
tree.column('attr2', width=100)
tree.column('attr3', width=100)
tree.column('damage', width=60)
tree.heading('name', text='五彩石')
tree.heading('attr1', text='属性1')
tree.heading('attr2', text='属性2')
tree.heading('attr3', text='属性3')
tree.heading('damage', text='理论伤害')


root.mainloop()

sys.exit()
