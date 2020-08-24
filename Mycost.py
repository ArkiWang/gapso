from CreateModel import Model
from ParseSolution import ParseSolution
def MyCost(sol1, model: Model) ->():

     # 计算航迹代价
    sol=ParseSolution(sol1,model)  #输入航迹与环境数据等数据

     #航迹代价参数
    Pl=model.Pl   #长度
    Pt=model.Pt    #静态威胁代价
    Pdt=model.Pdt   #航迹性能代价
    Pv=model.Pv    #移动威胁预测
    beta=100 
     # 计算航迹代价
    z=sol.L*Pl+Pt*(beta*sol.Violation+sol.v)+Pv*500*sol.vs+beta*sol.vdt*Pdt
    return (z, sol)