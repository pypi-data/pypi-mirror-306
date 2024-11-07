'''
 parForWorker worker used for parfor
 '''

from typing import Callable
from .PaIRS_pypacks import *


# To me, pylint is correct in flagging this error here the top level module is database (it contains an __init__.py file)
# Your import should look like (fully absolute) 
# https://stackoverflow.com/a/51236340
#from PIV_ParFor import callBack, FlagStopWorkers

from .preProcParFor import *
from .pivParFor import *
from .stereoPivParFor import *

prTime = PrintTA(PrintTA.yellow, PrintTA.faceStd,  PrintTAPriority.medium).prTime

class WorkerSignals(QObject):
    progress = Signal(int,int,int,list,str)
    result = Signal(int,int,list,str)
    finished = Signal(object,str)
    initialized = Signal()
    completed = Signal()
    kill = Signal(int)

class ParForWorker(QRunnable):
    def __init__(self,data:dataTreePar,indWorker:int,indProc:int,numUsedThreadsPIV:int,pfPool:ParForPool,parForMul:ParForMul,nameWorker:str,mainFun:Callable):
        #super(MIN_ParFor_Worker,self).__init__(data,indWorker,indProc,pfPool=ParForPool,parForMul=ParForMul)
        super().__init__()
        self.pfPool=pfPool
        self.parForMul=parForMul
        self.nameWorker=nameWorker # diverso per le due classi
        self.data=data.duplicate() #OPTIMIZE TA GP controllare se le modifiche fatte nel workers interferiscono con quelle fatte in progress_proc ed eventualmente evitare l'aggiornamento in resetProc e in store_proc
        self.indWorker = indWorker
        self.indProc = indProc
        self.numUsedThreadsPIV=numUsedThreadsPIV
        self.signals=WorkerSignals()
        self.isKilled = False
        self.isStoreCompleted = False
        self.numCallBackTotOk=0
        
        self.mainFun=mainFun

    @Slot()
    def run(self):
        if Flag_DEBUG_PARPOOL: debugpy.debug_this_thread()
        try:
            #pr(f'ParForWorker.run self.isKilled={self.isKilled}  self.indWorker={self.indWorker}  self.indProc={self.indProc}  ')
            self.parForMul.numUsedCores=self.numUsedThreadsPIV
            while self.indWorker!=self.indProc:# and not self.isKilled:
                timesleep(SleepTime_Workers) 
                if self.isKilled: 
                   self.signals.completed.emit()
                   return # in this case we are killing all the threads
            pri.Process.blue(f'ParForWorker.run starting {self.nameWorker} self.isKilled={self.isKilled}  self.indWorker={self.indWorker}  self.indProc={self.indProc}  ')
            self.mainFun()
        except:
            Message=printException('ParForWorker',flagMessage=True)
            self.signals.finished.emit(self.data,Message)
        #finally:#also after return eliminated
        while not self.isStoreCompleted:
           timesleep(SleepTime_Workers) 
        self.signals.completed.emit()
        pri.Process.blue(f'End of ParForWorker {self.nameWorker} ({self.indWorker}, {self.numCallBackTotOk} )')
                      
    @Slot()
    def killOrReset(self,isKilled):
        #pr('\n***********************\n*************************    ParForWorker.die {isKilled}')
        global FlagStopWorkers
        self.isKilled=isKilled
        FlagStopWorkers[0]=1 if isKilled else 0
        
    @Slot(int)
    def updateIndProc(self,indProc):
        #pr(f'updateIndProc {self.nameWorker} ({self.indWorker})')          
        self.indProc=indProc
        
    @Slot(int)
    def setNumCallBackTot(self,numCallBackTotOk):
        #if (self.numCallBackTotnumCallBackTotOk>numCallBackTotOk):         prLock(f'setNumCallBackTot numCallBackTotOk={numCallBackTotOk}')
        self.numCallBackTotOk=numCallBackTotOk

    @Slot()
    def storeCompleted(self):
       self.isStoreCompleted=True

class MIN_ParFor_Worker(ParForWorker):
  def __init__(self,data:dataTreePar,indWorker:int,indProc:int,numUsedThreadsPIV:int,pfPool:ParForPool,parForMul:ParForMul):
    super().__init__(data,indWorker,indProc,numUsedThreadsPIV,pfPool,parForMul,nameWorker='calcMin_Worker',mainFun=self.calcmin)

  def calcmin(self):
        stringaErr=''
        global FlagStopWorkers
        pri.Time.blue(0,'calcmin')
        FlagStopWorkers[0]=0
        
        #pp=ParForMul()
        #pp.sleepTime=ParFor_sleepTime #time between calls of callBack
        #pp.numCoresParPool=numUsedThreadsPIV
        
        self.data.compMin.restoreMin()
        args=(self.data,self.numUsedThreadsPIV)
        kwargs={} 
        numCallBackTotOk=self.data.numFinalized  #su quelli non finalized ci ripassiamo quindi inizialmente il num di callback ok = num di finalized

        nImg=range(self.data.nimg)
        #nImg=range(2*self.data.nimg)
        
        myCallBack=lambda a,b,c,d,e,f: callBackMin(a,b,c,d,e,f,self.signals.progress)
        #for ii,f in enumerate(self.data.list_pim):          pr(f'{ii}-{hex(f)}  ',end='')
        pri.Process.blue(f'Init calcmin Contab={self.data.compMin.contab}   numCallBackTotOk={numCallBackTotOk}  numUsedThreadsPIV={self.numUsedThreadsPIV}')
        self.signals.initialized.emit()
        #TBD TA all the exceptions should be managed inside parForExtPool therefore the try should be useless just in case I check
        try:
          
          if self.pfPool:
            (mi,flagOut,VarOut,flagError)=self.parForMul.parForExtPool(self.pfPool.parPool,procMIN,nImg,initTask=initMIN,finalTask=finalMIN, wrapUp=saveAndMin, callBack=myCallBack,*args,**kwargs)
          else:
            (mi,flagOut,VarOut,flagError)=self.parForMul.simpleFor(procMIN,nImg,initTask=initMIN,finalTask=finalMIN, wrapUp=saveAndMin, callBack=myCallBack,*args,**kwargs)
        except Exception as e:  
          PrintTA().printEvidenced('Calcmin exception raised.\nThis should never happen.')
          raise (e)
        if flagError: 
          self.signals.finished.emit(self.data,printException('calcmin',flagMessage=True,exception=self.parForMul.exception))
          return
          
        pri.Time.blue(0,'dopo  parForExtPool ****************************************')
        '''
        def callBackSaveMin(f3):
          pri.Time.blue(0,'callBackSaveMin')
          #(pfPool,parForMul)=f3.result()
        async def callSaveMin(data:dataTreePar,Imin=list): 
           #t1=asyncio.create_task(saveMin(self.data,mi.Imin)) 
           #await t1
           saveMin(self.data,mi.Imin) #nel caso controllare errore come sotto
        '''
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        if mi.contab[0]!=0:
          mi.calcMed()
          #OPTIMIZE TAGP sul mio pc (TA) saveMin è lenta (5 secondi) forse si può organizzare con una funzione async tanto non ci interessa quando finisce
          #f3=executor.submit(asyncio.run,callSaveMin(self.data,mi.Imin))
          #f3.add_done_callback(callBackSaveMin)
          try:
            saveMin(self.data,mi.Imin) 
          except:
             stringaErr+=printException('calcmin',flagMessage=True)+'\n'
        pri.Time.blue(0,'dopo  saveMin ****************************************')
        #for ii,f in enumerate(flagOut):          pr(f'{ii}-{hex(f)}  ',end='')
        numCallBackTotOk+=sum(1 if x&FLAG_CALLBACK_INTERNAL else 0 for x in flagOut)     

        #initTime=time()
        self.data.flagParForCompleted=True
        while self.numCallBackTotOk!=numCallBackTotOk:
            pri.Process.blue (f'Error Calcmin self.numCallBackTotOk={self.numCallBackTotOk} numCallBackTotOk={numCallBackTotOk} ')
            timesleep(SleepTime_Workers)
        
        #numProcOrErrTot=sum(1 if (f&FLAG_FINALIZED_OR_ERR[0])and (f&FLAG_FINALIZED_OR_ERR[1]) else 0 for f  in flagOut)   
        numProcOrErrTot=sum(1 if f else 0 for f  in flagOut)   
        pri.Process.blue (f'Fine calcmin **************  numCallBackTotOk={numCallBackTotOk}  numProcOrErrTot={numProcOrErrTot} numFinalized={self.data.numFinalized}')
        pri.Time.blue(0,'fine calcmin ****************************************')
        

        if mi.contab[0]!=0:
          pri.Time.blue(0,f'Min value coord(20,20) Min=[{mi.Imin[0][20][20]},{mi.Imin[1][20][20]}]  med=[{mi.med[0][20][20]},{mi.med[1][20][20]}]')
          pri.Time.blue(0,f'Min value coord(52,52) Min=[{mi.Imin[0][52][52]} {mi.Imin[1][52][52]}]  med=[{mi.med[0][52][52]} {mi.med[1][52][52]}]')
                # In pause_MINproc oltre a salvare il minimo si verifica se tutte le img programmate sono state processate anche con esito negativo, nel caso si passa al task successivo
        
        self.data.compMin=mi
        self.data.FlagFinished=self.data.nimg==numProcOrErrTot
        self.signals.finished.emit(self.data,stringaErr)

class PIV_ParFor_Worker(ParForWorker):
  def __init__(self,data:dataTreePar,indWorker:int,indProc:int,numUsedThreadsPIV:int,pfPool:ParForPool,parForMul:ParForMul):
    super().__init__(data,indWorker,indProc,numUsedThreadsPIV,pfPool,parForMul,nameWorker='PIV_Worker',mainFun=self.runPIVParFor)
  
  def runPIVParFor(self):
        stringaErr=''
        global FlagStopWorkers
        pri.Time.cyan(3,'runPIVParFor')
        FlagStopWorkers[0]=0
        # TODEL
        
        flagDebugMem=False
        if flagDebugMem:# TODEL?
          m1=memoryUsagePsutil() 
        filename_preproc=self.data.filename_proc[StepTypes.min]

        self.data.mediaPIV.restoreSum()
        
        #args=(self.data,)
        
        
        nPivOpt,nProcOpt=optimalPivCores(self.numUsedThreadsPIV,self.data.nimg,penCore=0.95)
        #nProcOpt=floor(totCore/nPivOpt)#todo GP we should print the number of piv cores and processes in the  log
        args=(self.data,nProcOpt)
        self.data.NumThreads=nPivOpt   #numThreadsPiv
        self.data.numUsedThreadsPIV=self.numUsedThreadsPIV# TODO GP now this is misleading we should change the name everywhere maybe numTotUsedThreads
        #­args=(self.data,self.numUsedThreadsPIV)
        #self.data.NumThreads=1 
        kwargs={'finalPIVPIppo': self.data.nimg}#unused just for example
        kwargs={}
        numCallBackTotOk=self.data.numFinalized  #su quelli non finalized ci ripassiamo quindi inizialmente il num di callback ok = num di finalized


        nImg=range(self.data.nimg)
        myCallBack=lambda a,b,c,d,e,f: callBackPIV(a,b,c,d,e,f,self.signals.progress)
        pri.Process.blue(f'runPIVParFor   mediaPIV cont={self.data.mediaPIV.cont}  self.numCallBackTotOk={self.numCallBackTotOk}   self.data.nimg={self.data.nimg}  numProc={nProcOpt}  numPivProc={nPivOpt}')

        self.signals.initialized.emit()
        #TBD TA all the exceptions should be managed inside parForExtPool therefore the try should be useless just in case I check
        parForFun= self.parForMul.parForExtPool if self.pfPool else self.parForMul.simpleFor
        try:
          if self.data.Step==StepTypes.piv:
            (me,flagOut,VarOut,flagError)=parForFun(self.pfPool.parPool,procPIV,nImg,initTask=initPIV,finalTask=finalPIV, wrapUp=saveAndMean, callBack=myCallBack,*args,**kwargs)
          elif self.data.Step==StepTypes.spiv:
            (me,flagOut,VarOut,flagError)=parForFun(self.pfPool.parPool,procStereoPIV,nImg,initTask=initStereoPIV,finalTask=finalStereoPIV, wrapUp=saveAndMean, callBack=myCallBack,*args,**kwargs)
          
        except Exception as e:
          PrintTA().printEvidenced('Calcmin exception raised\nThis should never happen ')
          raise (e)
        if flagError: 
          self.signals.finished.emit(self.data,printException('calcmin',flagMessage=True,exception=self.parForMul.exception))
          return
        
        try:
          if me.cont:
            me:MediaPIV
            me.calcMedia()
            nameFields=me.namesPIV.avgVelFields
            Var=[getattr(me,f) for f in nameFields ]#me.x,me.y,me.u,me.v,me.up,me.vp,me.uvp,me.sn,me.Info]
            nameVar=me.namesPIV.avgVel  
            saveResults(self.data,-1,Var,nameVar)
        except:
           stringaErr+=printException('calcmin',flagMessage=True,exception=self.parForMul.exception)+'\n'
        numCallBackTotOk+=sum(1 if x&FLAG_CALLBACK_INTERNAL else 0 for x in flagOut)            
        
        # Tbd 
        '''
        if flagDebugMem:
          pri.Time.cyan(0,'Save results')
          pr(f"Number of garbage element not collected before {gc.get_count()}",end='')   
          gc.collect()
          pr(f" after {gc.get_count()}")
          pr(f"********************** End Fun Main -> {(memoryUsagePsutil()-m1)/ float(2 ** 20)}MByte")
          pr(*gc.garbage)
        '''
        
        
        
        #initTime=time()
        self.data.flagParForCompleted=True
        while self.numCallBackTotOk!=numCallBackTotOk :
            pri.Process.blue (f'Error runPIVParFor self.numCallBackTotOk={self.numCallBackTotOk} numCallBackTotOk={numCallBackTotOk}    numProc={nProcOpt}  numPivProc={nPivOpt}')
            timesleep(SleepTime_Workers)
               
        if me.cont:
          pri.Time.cyan(f'u={me.u[5][4]} v={me.v[5][4]}  up={me.up[5][4]} vp={me.vp[5][4]} uvp={me.uvp[5][4]} sn={me.sn[5][4]} Info={me.Info[5][4]}')
    
        #self.numFinalized=sum(1 if f&FLAG_FINALIZED[0]  else 0 for f  in flagOut)   
        numProcOrErrTot=sum(1 if f else 0 for f  in flagOut)   

        #for ii,f in enumerate(flagOut):          pr(f'{ii}-{hex(f)}  ',end='')
        pri.Process.blue (f'Fine runPIVParFor **************  numCallBackTotOk={numCallBackTotOk}  numProcOrErrTot={numProcOrErrTot} numFinalized={self.data.numFinalized}')
        
        self.data.mediaPIV=me
        self.data.FlagFinished=self.data.nimg==numProcOrErrTot
        self.signals.finished.emit(self.data,stringaErr)  

class StereoPIV_ParFor_Worker(ParForWorker):
  def __init__(self,data:dataTreePar,indWorker:int,indProc:int,numUsedThreadsPIV:int,pfPool:ParForPool,parForMul:ParForMul):
    super().__init__(data,indWorker,indProc,numUsedThreadsPIV,pfPool,parForMul,nameWorker='SPIV_Worker',mainFun=self.runStereoPIVParFor)
  
  def runStereoPIVParFor(self):
        stringaErr=''
        global FlagStopWorkers
        pri.Time.cyan(3,'runStereoPIVParFor')
        FlagStopWorkers[0]=0
        # TODEL
        
        flagDebugMem=False
        if flagDebugMem:# TODEL?
          m1=memoryUsagePsutil() 
        
        filename_preproc=self.data.filename_proc[StepTypes.min]# todo serve?

        self.data.mediaPIV.restoreSum()#todo modificare in mediaStereoPIV
        
        #args=(self.data,)
        args=(self.data,self.numUsedThreadsPIV)
        #kwargs={'finalPIVPIppo': self.data.nimg}#unused just for example
        kwargs={}
        numCallBackTotOk=self.data.numFinalized  #su quelli non finalized ci ripassiamo quindi inizialmente il num di callback ok = num di finalized


        nImg=range(self.data.nimg)
        myCallBack=lambda a,b,c,d,e,f: callBackPIV(a,b,c,d,e,f,self.signals.progress)
        pri.Process.blue(f'runStereoPIVParFor   mediaPIV cont={self.data.mediaPIV.cont}  self.numCallBackTotOk={self.numCallBackTotOk}   self.data.nimg={self.data.nimg}')

        self.signals.initialized.emit()
        #TBD TA all the exceptions should be managed inside parForExtPool therefore the try should be useless just in case I check
        try:
          if self.pfPool:
            (me,flagOut,VarOut,flagError)=self.parForMul.parForExtPool(self.pfPool.parPool,procStereoPIV,nImg,initTask=initStereoPIV,finalTask=finalStereoPIV, wrapUp=saveAndMean, callBack=myCallBack,*args,**kwargs)
          else:
            (me,flagOut,VarOut,flagError)=self.parForMul.simpleFor(procStereoPIV,nImg,initTask=initStereoPIV,finalTask=finalStereoPIV, wrapUp=saveAndMean, callBack=myCallBack,*args,**kwargs)
        except Exception as e:
          PrintTA().printEvidenced('runStereoPIVParFor exception raised\nThis should never happen ')
          raise (e)
        if flagError: 
          self.signals.finished.emit(self.data,printException('runStereoPIVParFor',flagMessage=True,exception=self.parForMul.exception))
          return
        
        try:
          if me.cont:
            me:MediaPIV
            me.calcMedia()
            nameFields=me.namesPIV.avgVelFields
            Var=[getattr(me,f) for f in nameFields ]#me.x,me.y,me.u,me.v,me.up,me.vp,me.uvp,me.sn,me.Info]
            nameVar=me.namesPIV.avgVel  
            saveResults(self.data,-1,Var,nameVar)
        except:
           stringaErr+=printException('runStereoPIVParFor',flagMessage=True,exception=self.parForMul.exception)+'\n'
        numCallBackTotOk+=sum(1 if x&FLAG_CALLBACK_INTERNAL else 0 for x in flagOut)            
        
        # Tbd 
        '''
        if flagDebugMem:
          pri.Time.cyan(0,'Save results')
          pr(f"Number of garbage element not collected before {gc.get_count()}",end='')   
          gc.collect()
          pr(f" after {gc.get_count()}")
          pr(f"********************** End Fun Main -> {(memoryUsagePsutil()-m1)/ float(2 ** 20)}MByte")
          pr(*gc.garbage)
        '''
        
        
        
        #initTime=time()
        self.data.flagParForCompleted=True
        while self.numCallBackTotOk!=numCallBackTotOk :
            pri.Process.blue (f'Error runStereoPIVParFor self.numCallBackTotOk={self.numCallBackTotOk} numCallBackTotOk={numCallBackTotOk}    numUsedThreadsPIV={self.numUsedThreadsPIV}')
            timesleep(SleepTime_Workers)
               
        if me.cont:
          pri.Time.cyan(f'u={me.u[5][4]} v={me.v[5][4]}  up={me.up[5][4]} vp={me.vp[5][4]} uvp={me.uvp[5][4]} sn={me.sn[5][4]} Info={me.Info[5][4]}')
    
        #self.numFinalized=sum(1 if f&FLAG_FINALIZED[0]  else 0 for f  in flagOut)   
        numProcOrErrTot=sum(1 if f else 0 for f  in flagOut)   

        #for ii,f in enumerate(flagOut):          pr(f'{ii}-{hex(f)}  ',end='')
        pri.Process.blue (f'Fine runStereoPIVParFor **************  numCallBackTotOk={numCallBackTotOk}  numProcOrErrTot={numProcOrErrTot} numFinalized={self.data.numFinalized}')
        
        self.data.mediaPIV=me
        self.data.FlagFinished=self.data.nimg==numProcOrErrTot
        self.signals.finished.emit(self.data,stringaErr)  


class StereoDisparity_ParFor_Worker(ParForWorker):
  def __init__(self,data:dataTreePar,indWorker:int,indProc:int,numUsedThreadsPIV:int,pfPool:ParForPool,parForMul:ParForMul):
    super().__init__(data,indWorker,indProc,numUsedThreadsPIV,pfPool,parForMul,nameWorker='Disp_Worker',mainFun=self.runDisparity)

  def runDisparity(self):
      ''' main proc function called for all the images one time per processor 
      k=0 always
      In output flagOut and varOut[0] can be:
        Already processed:      varOut[0]=-1 flagOut=FLAG_PROC[k]|FLAG_READ[k]|FLAG_FINALIZED[k]
        Error reading:          varOut[0]=i  flagOut=FLAG_READ_ERR[k]
        Error processing:       varOut[0]=i  flagOut=FLAG_READ[k]
        Process stoped by user: varOut[0]=-1 flagOut=FLAG_READ[k]
        Error saving:           varOut[0]=i  flagOut=FLAG_PROC[k]|FLAG_READ[k]
        Read and processed:     varOut[0]=i  flagOut=FLAG_PROC[k]|FLAG_READ[k]|FLAG_FINALIZED[k]|FLAG_CALLBACK_INTERNAL
      '''
      self.signals.initialized.emit()
      data=self.data
      
      it=0
      Var=[]
      procID=-1

      flagOut=flagOutIter=0
      kConst=0
      self.disp=data2Disp(data)
      spivIn=self.disp.SPIVIn
      dP=self.disp.dataProc
      dAC=self.disp.dispAvCo
      ve=self.disp.vect
      ve.PianoLaser[0]=np.float32(data.OUT_dict['zconst'])
      ve.PianoLaser[1]=np.float32(data.OUT_dict['xterm'])
      ve.PianoLaser[2]=np.float32(data.OUT_dict['yterm'])

      stringaErr=''
      if self.isKilled: return self.stopDisparity(it,flagOut,flagOutIter)
      try:
        #1/0  #***************** delete
        self.disp.evalCommonZone()
      except Exception as inst: #ValueError as exc:
        FlagInitError=True
        stringaErr=f'\n!!!!!!!!!! Error while evaluating common region:\n{inst}\n'
        pri.Error.red(stringaErr)
        flagOut|=FLAG_READ_ERR[kConst]
      else:
        FlagInitError=False

      """
      if self.isKilled: return self.stopDisparity(it,flagOut,flagOutIter)
      if not FlagInitError:
        self.imgs=[]
        ind=np.ix_(np.arange(spivIn.RigaPart,spivIn.RigaPart+dP.ImgH),np.arange(spivIn.ColPart,spivIn.ColPart+dP.ImgW))
        #data.list_Image_Files[c][f][k]
        imList=data.list_Image_Files
        for p in range(len(imList[0][0])):
          if self.isKilled: return self.stopDisparity(it,flagOut,flagOutIter)
          ic=[]
          #print(f'reading {p}')
          try:
            for cam in range(len(imList[0])):
              da=db=None
              if spivIn.FlagImgTau in (0,1):
                if self.isKilled: return self.stopDisparity(it,flagOut,flagOutIter)
                nomeImg=data.inpPath+imList[cam][0][p]
                da=np.ascontiguousarray(np.array(Image.open(nomeImg),dtype=float)[ind],dtype= np.uint16)
              if spivIn.FlagImgTau in (0,2):
                if self.isKilled: return self.stopDisparity(it,flagOut,flagOutIter)
                nomeImg=data.inpPath+imList[cam][1][p]
                db=np.ascontiguousarray(np.array(Image.open(nomeImg),dtype=float)[ind],dtype= np.uint16)
             
              ic.append([da,db])
          except Exception as inst: #ValueError as exc:
            FlagInitError=True
            stringaErr=f"\n!!!!!!!!!! Error while reading the image {nomeImg}:\n{inst}\n" 
            pri.Error.red(stringaErr)
            flagOut|=FLAG_READ_ERR[kConst]
            break
          else:
            self.imgs.append(ic)
            #self.imgs.append(np.ascontiguousarray(da[spivIn.RigaPart:spivIn.RigaPart+dP.ImgH,spivIn.ColPart:spivIn.ColPart+dP.ImgW],dtype= np.uint16))
      """

      imList=data.list_Image_Files
      indim=np.ix_(np.arange(spivIn.RigaPart,spivIn.RigaPart+dP.ImgH),np.arange(spivIn.ColPart,spivIn.ColPart+dP.ImgW))
      if data.FlagMIN:
        data.compMin.Imin=[[np.zeros(1) for _ in range(data.nframe)] for _ in range(data.ncam)]
        for c,Iminc in enumerate(data.Imin):
          for k,filename in enumerate(Iminc):
            try:
              data.compMin.Imin[c][k]=np.ascontiguousarray(np.array(Image.open(filename),dtype=float)[indim],dtype= np.uint16)
            except Exception as inst:  
                FlagInitError=True
                stringaErr=f'\n!!!!!!!!!! Error while reading background image {filename}:\n{inst}\n'
                pri.Error.red(stringaErr)
                flagOut|=FLAG_READ_ERR[kConst]
                break
            
      if not FlagInitError:
        if self.isKilled: return self.stopDisparity(it,flagOut,flagOutIter)
        try:
          self.disp.initAllocDisp()
        except Exception as inst: #ValueError as exc:
          FlagInitError=True
          stringaErr=f'\n!!!!!!!!!! Error during disparity process initialization:\n{inst}\n'
          pri.Error.red(stringaErr)
          flagOut|=FLAG_READ_ERR[kConst]

      #print(f'Esempio risoluzione utilizzata {self.disp.dataProc.RisxRadd} {1/self.disp.dataProc.RisxRadd}')
      #sleepTimeWorkers=0.2 #for multithreading and other stuff
      #if FlagInitError: flagOut|=FLAG_FINALIZED[kConst]|FLAG_CALLBACK_INTERNAL
      flagOutIter=FLAG_READ[kConst]
      for it in range(spivIn.Niter):
        if FlagInitError:
           if data.list_pim[it]&FLAG_READ_ERR[kConst]: ind=-1# no log already written
           if it==0: stampa=stringaErr
           else: stampa=''
           data.list_print[it]=stampa
           data.list_pim[it]=flagOut
           self.signals.progress.emit(procID,-1,flagOut,Var,stringaErr)
           continue
        if data.list_pim[it]&FLAG_FINALIZED[kConst]:
          flagOut=FLAG_READ[kConst]|FLAG_PROC[kConst]|FLAG_FINALIZED[kConst]  # It has been already processed. Exit without calling the callback  core 
          stampa=''
          ind=-1
          self.signals.progress.emit(procID,ind,flagOut,Var,stampa)
          continue
        flagOut=flagOutIter
        Var=[]
        stampa=f"Iteration {it+1}\n"
        ind=it
        if self.isKilled: return self.stopDisparity(it,flagOut,flagOutIter)
        try:
          errorType='evaluating viewing angles'
          self.disp.evaldXdY()  
          if self.isKilled: return self.stopDisparity(it,flagOut,flagOutIter)
          for p in range(len(imList[0][0])):
            if self.isKilled: return self.stopDisparity(it,flagOut,flagOutIter)
            ic=[]
            #print(f'reading {p}')
            for cam in range(len(imList[0])):
              da=db=None
              if spivIn.FlagImgTau in (0,1):
                if self.isKilled: return self.stopDisparity(it,flagOut,flagOutIter)
                nomeImg=data.inpPath+imList[cam][0][p]
                errorType=f'reading the image {nomeImg}'
                da=np.ascontiguousarray(np.array(Image.open(nomeImg),dtype=float)[indim],dtype= np.uint16)
                if data.FlagMIN:
                  if data.FlagTR and p%2:
                    da=da-data.compMin.Imin[cam][1]
                  else:
                    da=da-data.compMin.Imin[cam][0]
                  da=np.ascontiguousarray(da,dtype= np.uint16)
              if spivIn.FlagImgTau in (0,2):
                if self.isKilled: return self.stopDisparity(it,flagOut,flagOutIter)
                nomeImg=data.inpPath+imList[cam][1][p]
                errorType=f'reading the image {nomeImg}'
                db=np.ascontiguousarray(np.array(Image.open(nomeImg),dtype=float)[indim],dtype= np.uint16)
                if data.FlagMIN:
                  if data.FlagTR and p%2:
                    db=db-data.compMin.Imin[cam][0]
                  else:
                    db=db-data.compMin.Imin[cam][1]
                  db=np.ascontiguousarray(db,dtype= np.uint16)
            
              ic.append([da,db])
            
            errorType=f'dewarping and computing disparity ({imList[0][0][p]},...,{imList[1][1][p]})'
            self.disp.deWarpAndCalcCC(ic)
            #while self.disp.flagWorking==2:# and not self.isKilled:            sleep (sleepTimeWorkers) 
            if self.isKilled: return self.stopDisparity(it,flagOut,flagOutIter)
          
          errorType=f'computing the laser plane constants'
          self.disp.calcDisparity()
          if self.isKilled: return self.stopDisparity(it,flagOut,flagOutIter)
          #while self.disp.flagWorking==2:# and not self.isKilled:          sleep (sleepTimeWorkers) 
        except Exception as inst:
          if (data.list_pim[it]&FLAG_READ[kConst]): ind=-1# no log already written
          #dum=str(inst.__cause__).split('\n')[3] #solved
          dum=str(inst.args[0])
          #varOut[1]+=f"\n!!!!!!!!!! Error while processing the above image pair: {dum}"  
          errorPrint=f"!!!!!!!!!! Error while {errorType}:\n{dum}\n"  
          stampa+=errorPrint  
          stringaErr+=stampa
          pri.Error.red(stringaErr)
        else:
          flagOut|=FLAG_PROC[kConst]# per completezza aggiungo anche processato
          stampa+=f"   Laser plane eq. : z (mm) = {ve.PianoLaser[0]:.4g} + {ve.PianoLaser[1]:.4g} * x + {ve.PianoLaser[2]:.4g} * y\n   Residual calib. error    = {dAC.dOrtMean:.4g} pixels\n   Estimated laser thick.   = {dAC.DeltaZ:.4g} pixels (approx. {dAC.DeltaZ * dP.RisxRadd / abs(dAC.ta0Mean - dAC.ta1Mean):.4g} mm)\n"
          data.OUT_dict['zconst']=float(ve.PianoLaser[0])
          data.OUT_dict['xterm']=float(ve.PianoLaser[1])
          data.OUT_dict['yterm']=float(ve.PianoLaser[2])
          try:
            nameVar=data.namesPIV.instVel 
            Var=[getattr(self.disp.vect,f) for f in nameVar ]
            #if it==spivIn.Niter-1:
            #  saveResults(data,-1,Var,nameVar)
            #else:
            saveResults(data,f'it{it+1}',Var,nameVar)
          except Exception as inst:
            errorPrint=f"\n!!!!!!!!!! Error while saving the results:\n{str(inst)}\n"
            stampa+=errorPrint
            stringaErr+=stampa
            pri.Error.red(stringaErr)
            FlagFinalized=False
          else:
            FlagFinalized=True
            if it==spivIn.Niter-1:
              errorPrint=self.writeLaserPlaneConst(filename=data.outPathRoot+'.clz',planeConst=ve.PianoLaser,resolution=self.disp.dataProc.RisxRadd)
              if errorPrint:
                stampa+=errorPrint
                stringaErr+=stampa
                pri.Error.red(stringaErr)
                FlagFinalized=False
              else:
                 data.res=1./self.disp.dataProc.RisxRadd
                 data.laserConst=[float(const) for const in ve.PianoLaser]
          if FlagFinalized:
            flagOut|=FLAG_FINALIZED[kConst]|FLAG_CALLBACK_INTERNAL
       
        data.list_print[it]=stampa
        data.list_pim[it]=flagOut
        self.signals.progress.emit(procID,ind,flagOut,Var,stampa)
        if stringaErr: break
        timesleep(3)
      
      for j in range(it+1,spivIn.Niter):
        data.list_print[j]=''
        data.list_pim[j]=flagOut
        self.signals.progress.emit(procID,j,flagOut,[],'')

      self.data.FlagFinished=True
      self.signals.finished.emit(data,stringaErr)  

  def writeLaserPlaneConst(self,filename:str, planeConst:list, resolution:float):
      try:
        with open(filename, "w") as cfg:
            cfg.write(f"%SP00007\n")
            cfg.write(f"% Used resolution={1 / resolution:.6g}pix/mm\n")
            cfg.write(f"% Laser plane constants\n")
            cfg.write(f"{planeConst[0]:.14e},\n")
            cfg.write(f"{planeConst[1]:.14e},\n")
            cfg.write(f"{planeConst[2]:.14e},\n")
      except Exception as inst:
        errorPrint=f"\n!!!!!!!!!! Error while saving the results:\n{str(inst)}\n"
          #pri.Error.red(f'Error while saving the laser plane constants!\n{traceback.format_exc()}\n')
      else:
        errorPrint=''
      return errorPrint
  
  def stopDisparity(self,it,flagOut,flagOutIter):
     procID=-1
     ind=-1
     data=self.data
     spivIn=self.disp.SPIVIn
     for j in range(it,spivIn.Niter):
        data.list_print[j]=''
        data.list_pim[j]=flagOut if j==it else flagOutIter
        self.signals.progress.emit(procID,ind,flagOutIter,[],'')
     self.signals.finished.emit(data,'')  