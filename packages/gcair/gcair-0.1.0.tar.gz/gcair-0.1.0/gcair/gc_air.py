# gcair/gc_air.py

from .get_sim_params import get_sim_params
from .error import Error

class GCAir:
    """
    A python class for GCAir

    使用时, 先启动 GCAir, 然后 A = GCAir() 与 GCA 建立连接,
    最后使用其它 API 操纵 GCA

    所有 API 均通过异常反馈错误
    """

    # 仿真正在进行
    SIM_RUNING = 0
    # 仿真暂停
    SIM_PAUSE = 1
    # 仿真已经结束（此时还没有点击仿真返回）
    SIM_FINISH = 2
    # 仿真还未开始
    SIM_NOT_START = 3

    def __init__(self) -> None:
        # result = await get_sim_params()
        # 仿真的 token
        self.__TOKEN = "" # result["token"]
        # 仿真的URL
        self.__URL = "" #result["url"]
        # 仿真的项目ID
        self.__PROJECT_ID = "" # result["projectId"]
        # 用于存放方针结果
        self.__SIM_RESULT = []

    # 打开工程
    def OpenProject(self, projectFilePath):
        """
        打开 GCA 工程

        参数
        ----
        projectFilePath : str
            GCA 工程的路径

        注意
        --------
        若 projectFilePath 不是一个合法的文件路径，则抛出 ProjectPathError 异常
        """

        # 目前web 端不支持 打开工程的功能
        raise Error("目前web 端不支持 打开工程的功能")


    # 工程保存
    def SaveProject(self):
        """
        保存工程

        参数
        ----
        无参数
        """
        # 目前web 端不支持 保存工程
        raise ValueError("目前web 端不支持 保存工程")

    # 工程另存为
    def SaveAsProject(self, projectPath, isOverwrite=False):
        """
        另存工程

        参数
        ----
        projectPath : str
            目标工程路径，.文件的路径

        isOverwrite : bool
            是否覆盖已有的文件
        """
        # 目前web 端不支持 另存工程
        raise ValueError("目前web 端不支持 另存工程")

        # 创建工程

    def CreateProject(self, projectPath, isOverwrite=False):
        """
        创建工程

        参数
        ----
        projectPath : str
            目标工程路径，.gck文件的路径

        isOverwrite : bool
            是否覆盖已有的文件
        """
        # 目前web 端不支持 创建工程
        raise ValueError("目前web 端不支持 创建工程")

    def SimulationStart(self, blocked: bool = True):
        """
        仿真开始

        参数
        ----
        blocked : bool
            是否阻塞

        返回值
        -----
        无返回值
        """
        # self.__comm.ExecuteCommand("SimulationStart", blocked)

    def SimulationReset(self):
        """
        重置仿真

        参数
        ----
        blocked : bool
            是否阻塞

        返回值
        -----
        无返回值
        """
        # self.__comm.ExecuteCommand("SimulationReset")

    def SimulationPause(self):
        '''
        仿真暂停
        '''
        # self.__comm.ExecuteCommand("SimulationPause")

    def SimulationContinue(self):
        '''
        仿真继续
        '''
        # self.__comm.ExecuteCommand("SimulationContinue")

    def SimulationComeback(self):
        '''
        仿真返回（重置仿真）
        '''
        # self.__comm.ExecuteCommand("SimulationComeback")

    # 获取仿真结果
    def GetSimulationResult(self):
        """
        获取仿真结果

        参数
        ----
        无参数

        返回值
        -----
        仿真结果 : list[list[str], list[float], list[float]...]
            第一行: list[str]，模型中变量名，例如 simTime, Subsystem1.Function_x0

            第二行开始: list[float], 依次保存各个变量在每一个步长的值
        """
        # resp = self.__comm.ExecuteCommand("GetSimulationResult")
        # return PackSimulationResult(resp.resultArray)

    # 根据子系统或FMU名称全路径获取子系统或FMU仿真结果
    def GetSimulationResultByName(self, name : str, simTimeFlag : bool = True):
        """
        根据子系统或FMU名称全路径获取子系统或FMU仿真结果

        参数
        ----
        name : str 子系统或FMU名称全路径(子系统与子系统之间及子系统与fmu之间均用"/"隔开)
        例如: subSystem/subSystem 或 subSystem/Function
        simTimeFlag : bool 是否返回仿真时间数据,默认返回
        返回值
        -----
        仿真结果 : list[list[str], list[float], list[float]...]
            第一行: list[str]，模型中变量名，例如 simTime, Subsystem1/Function_x0

            第二行开始: list[float], 依次保存各个变量在每一个步长的值
        """

    def SetSimulationTime(self, **kwargs):
        """
        设置仿真时间

        可选参数
        ----
        time : float
            仿真总时长
        step : float
            仿真步长
        sample : float
            采样步长

        返回值
        ---
        无返回值
        """
        # self.__comm.ExecuteCommand("SetSimulationTotalTime", kwargs)

    def SetEngineIP(self, IP: str):
        '''
        设置仿真引擎IP
        '''
        # self.__comm.ExecuteCommand("SetEngineIP", IP)

    def SetSimSpeed(self, speed: float):
        """
        设置仿真速度

        参数
        ----
        speed : float
            仿真速度，可选值：
            0.1
            0.5
            1
            2
            10
            20
            50
            100
            1000
            float("inf")

        返回值
        -----
        无返回值
        """
        if speed not in (0.1, 0.5, 1, 2, 10, 20, 50, 100, 1000, float("inf")):
            raise ValueError(
                "仿真速度只能从 0.1, 0.5, 1, 2, 10, 20, 50, 100, 1000, float(\"inf\") 中选")
        # self.__comm.ExecuteCommand("SetSimSpeed", speed)

    def CreateBreakPoint(self, **kwargs):
        """
        创建断点

        可选参数
        ----
        express : str
            断点表达式
        type : str
            触发类型 {trigger: 表达式成立时触发, change: 值改变时触发}
        enable : bool
            是否启动

        返回值
        ------
        无返回值
        """
        # self.__comm.ExecuteCommand("BreakPoint::CreateBreakPoint", kwargs)

    def ChangeBreakPoint(self, index: int, **kwargs):
        """
        修改断点

        参数
        ----
        index : int
            要修改的断点的序号

        可选参数
        --------
        express : str
            断点表达式
        type : str
            触发类型, 可选值 trigger: 表达式成立时触发, change: 值改变时触发
        enable : bool
            是否启动

        返回值
        ------
        无返回值
        """

    def DeleteBreakPoint(self, index: int):
        """
        删除断点

        参数
        ----
        index : int
            要修改的断点的序号

        返回值
        ------
        无返回值
        """

    def GetSimulationStatus(self) -> int:
        """
        获取仿真状态

        参数
        ----
        无参数

        返回值
        ------
        当前仿真状态 : int
            GCAir.SIM_RUNING    仿真正在进行

            GCAir.SIM_PAUSE     仿真暂停

            GCAir.SIM_FINISH    仿真已经结束（此时还没有点击仿真返回）

            GCAir.SIM_NOT_START 仿真还未开始

        """

    def ChangeVariableValue(self, varName: str, value: any):
        """
        修改变量的值（仿真中）

        参数
        ----
        varName : str
            变量名称，例如 BlankSubSystem/UserVar_1.in0

        value : float / int/ bool
            要修改的目标值

        返回值
        ------
        无返回值
        """

    def SetParameterValue(self, paraName: str, value):
        """
        修改参数的值 (仿真前)

        参数
        ----
        paraName : str
            参数名称，例如 BlankSubSystem/UserVar_1.in0

        value : float / int / bool
            要修改的目标值

        返回值
        ------
        无返回值

        示例
        ----
        A.SetParameterValue("BlankSubSystem/BouncingBall.e", 0.3)
        """

    def Open2DPanel(self):
        '''
        打开2D面板
        '''
        # 目前web 端不支持 打开2D面板
        raise ValueError("目前web 端不支持 打开2D面板")