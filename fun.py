def create_dic_mplot(plik,kontekst='cg',odczyt=1,n_pz1=100,n_pz2=100):
    '''Funkcja towrzy słownik z informacją o liczbie i prociencie metylowanych cytozyn w każdej pozycji odczytów PE 
    na podstawie pliku genorowanego przez program Bismark'''
    if odczyt==1:
        n_pz=n_pz1
    else:
        n_pz=n_pz2
    koor_dic = {}
    for k in range(1,7):
        if k<4:
            l1 = (k-1)*n_pz1+3+(k-1)*4
            l2 = l1+n_pz1
            koor_dic[k] = [l1,l2]
        else:
            l1 = (k-1)*n_pz2+3+(k-1)*4+(3*(n_pz1-n_pz2))
            l2 = l1+n_pz2
            koor_dic[k] = [l1,l2]
    if kontekst == 'cg' and odczyt == 1:
        linie = plik[koor_dic[1][0]:koor_dic[1][1]]
    elif kontekst == 'chg' and odczyt == 1:
        linie = plik[koor_dic[2][0]:koor_dic[2][1]]
    elif kontekst == 'chh' and odczyt == 1:
        linie = plik[koor_dic[3][0]:koor_dic[3][1]]
    elif kontekst == 'cg' and odczyt == 2:
        linie = plik[koor_dic[4][0]:koor_dic[4][1]]
    elif kontekst == 'chg' and odczyt == 2:
        linie = plik[koor_dic[5][0]:koor_dic[5][1]]
    elif kontekst == 'chh' and odczyt == 2:
        linie = plik[koor_dic[6][0]:koor_dic[6][1]]
    else:
        print('Błędne argument')
        return
    plot_dic = {}
    for i in range(1,n_pz+1):
        n_met = int(linie[i-1].split('\t')[1])
        n_umet = int(linie[i-1].split('\t')[2])
        pr_met = float(linie[i-1].split('\t')[3])
        n = int(linie[i-1].split('\t')[4][:-1])
        plot_dic[i] = [n_met,n_umet,pr_met,n]
        
    return plot_dic

def make_plot(plik,odczyt=1,npz1=100, npz2=100):
    '''Funkcja gneruje M-bias plot na podstawie danych genarowanych przez program Bismark'''
    p = plik
    o = odczyt
    mnpz1 = npz1
    mnpz2 = npz2
    if odczyt==1:
        npz=npz1
    else:
        npz=npz2
    
    cg = create_dic_mplot(plik=p,kontekst='cg',odczyt=o,n_pz1=mnpz1,n_pz2=mnpz2)
    chg = create_dic_mplot(plik=p,kontekst='chg',odczyt=o,n_pz1=mnpz1,n_pz2=mnpz2)
    chh = create_dic_mplot(plik=p,kontekst='chh',odczyt=o,n_pz1=mnpz1,n_pz2=mnpz2)
    
    import matplotlib.pyplot as plt
    
    fig, host = plt.subplots()
    par1 = host.twinx()
    offset = 60
    
    y1, y2, y3, y4, y5, y6 = [], [], [], [], [], []
    for j in range(1,npz+1):
        y1.append(cg[j][2])
        y2.append(cg[j][3])
        y3.append(chg[j][2])
        y4.append(chg[j][3])
        y5.append(chh[j][2])
        y6.append(chh[j][3])
    
    host.set_xlim(1, npz+1)
    host.set_ylim(0, 100)
    
    host.set_xlabel("Pozycja")
    host.set_ylabel("% metylacji")
    par1.set_ylabel("Całkowita liczba cytozyn")
    
    p1, = host.plot(list(range(1,npz+1)), y1, linewidth=4, label="CG % metylacji")
    p2, = par1.plot(list(range(1,npz+1)), y2, linewidth=1, label="CG całkowita liczba cytozyn")
    p3, = host.plot(list(range(1,npz+1)), y3, linewidth=4, label="CHG % metylacji")
    p4, = par1.plot(list(range(1,npz+1)), y4, linewidth=1, label="CHG całkowita liczba cytozyn")
    p5, = host.plot(list(range(1,npz+1)), y5, linewidth=4, label="CHH % metylacji")
    p6, = par1.plot(list(range(1,npz+1)), y6, linewidth=1, label="CHH całkowita liczba cytozyn")
    
    par1.set_ylim(0, max([max(y2),max(y4),max(y6)]))
    
    host.legend(loc='center left', bbox_to_anchor=(1.4, 0.5))
    par1.legend(loc='center left', bbox_to_anchor=(1.4, 0.8))
    
    
    par1.yaxis.set_visible(True)
    
    
    plt.show()
    plt.draw()
