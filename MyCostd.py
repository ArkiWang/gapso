
def MyCostd(sol1,model):
    # 计算航迹代价
    sol=ParseSolutiond(sol1,model)   # 函数计算具体代价
     #航迹代价参数
    Pl=model.Pl   #长度
    Pt=model.Pt   #静态威胁代价
    Pdt=model.Pdt   #移动威胁预测代价
    Pv=model.Pv   #航迹性能约束
    beta=1000 
     # 计算航迹代价
    z=sol.L*Pl+Pt*(beta*sol.Violation+sol.v)+Pv*500*sol.vs+500*sol.vdt*Pdt
    return z, sol

