[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](code_of_conduct.md)  [![Build Status](https://app.travis-ci.com/noodles8436/THE-CROSS.svg?branch=main)](https://app.travis-ci.com/noodles8436/THE-CROSS) [![Python 3.8](https://img.shields.io/badge/python-3.6~3.9-blue.svg)](https://www.python.org/downloads/release/python-3812/) [![codecov](https://codecov.io/gh/noodles8436/THE-CROSS/branch/main/graph/badge.svg?token=785SLIJ1OO)](https://codecov.io/gh/noodles8436/THE-CROSS)
# THE-CROSS - 스마트 신호등 제어 시스템 

- 본 프로젝트는 과학기술정보통신부에서 주최한 OSS 개발자 대회 제출용입니다.

설치 방법
-----------------------

설치에 앞서, 아래의 두 가지 사항을 확인하시기 바랍니다.
1. 프로그램을 실행하고자 하는 장치에 **아나콘다를 설치**해야 합니다. ( WINDOWS OS 환경에서 설치하는 것을 권장합니다.)
2. 프로그램을 실행하고자 하는 장치에 **1~2개의 카메라가 연결**되어 있어야 합니다.   
( WebCam 과 USB CAM 둘 다 사용 가능하나, USB CAM 을 사용하는 것을 권장합니다. )   

   
명령 프롬프트 창을 열고, conda 가상 환경 구축해야 합니다.
```
conda create -n <env-name> python=3.8
conda activate <env-name>


:: CONDA 예제 ::
conda create -n cross python=3.8
conda activate cross
```

![1](https://github.com/noodles8436/THE-CROSS/blob/main/README_PHOTO/1.png)
![2](https://github.com/noodles8436/THE-CROSS/blob/main/README_PHOTO/2.PNG)
![3](https://github.com/noodles8436/THE-CROSS/blob/main/README_PHOTO/3.PNG)

그다음, 이 프로젝트를 다운받고 해당 폴더안에서 CONDA 명령창을 열은 후
**필요 항목들을 설치**하기 위해서, 아래의 명령어를 실행해야 합니다.
```
git clone https://github.com/noodles8436/THE-CROSS.git
cd THE-CROSS

pip install -r requirements.txt
```

![4](https://github.com/noodles8436/THE-CROSS/blob/main/README_PHOTO/4.PNG)
![5](https://github.com/noodles8436/THE-CROSS/blob/main/README_PHOTO/5.PNG)


마지막으로, **전이 학습된 Object Detection Model을 설치**하기 위해 아래의 명령어를 실행해야 합니다.   
( **이 모델은 EfficientDet-D2 model 모델을 전이학습한 모델입니다** )

```
python download_model.py
```

![6](https://github.com/noodles8436/THE-CROSS/blob/main/README_PHOTO/6.PNG)

사용 방법
-----------------------

 1. ### Image Detection Server 실행   
    Image Detection Server 실행하기 위해서, 아래의 명령어를 실행해야 합니다.    
    :: 주의 :: **Socket이 열렸다는 메세지가 출력될 때까지 기다려야 합니다**
    ```
    python Server.py --ip=XXX.XXX.XXX.XXX --port=XXXX
    
    :: 예시 ::
    python Server.py --ip=127.0.0.1 --port=7777
    ```   
    
    ![7](https://github.com/noodles8436/THE-CROSS/blob/main/README_PHOTO/7.PNG)
    
 2. ### Client Program 실행   
    **프로젝트 파일 내에서 새로운 Conda 명령창 ( 설치 과정에서 생성한 `<env-name>` 환경에서) 을 열어야 합니다.**
    ```
    conda activate <env-name>
    cd THE-CROSS
    ```
    **Client Program 을 실행하기 위해** 아래의 명령어를 실행해야 합니다.   
    :: 주의 :: **Client의 IP & PORT는 Server의 IP & PORT와 동일해야 합니다**
    ```
    python Client.py --ip=XXX.XXX.XXX.XXX --port=XXXX
    
    :: 예제 ::
    python Client.py --ip=127.0.0.1 --port=7777
    ```
    
    ![8](https://github.com/noodles8436/THE-CROSS/blob/main/README_PHOTO/8.PNG)
    ![9](https://github.com/noodles8436/THE-CROSS/blob/main/README_PHOTO/9.PNG)
   
3. ### 횡단보도 영역 & 차도 영역 설정
   1. 프로그램의 우측 하단에서, 설정하기를 원하는 영역을 찾아 설정 버튼을 누릅니다.
   2. 버튼을 누르고 난 후에 보이는 팝업 창에서, 장치와 연결된 실시간 카메라의 영상이 보일 때까지 기다립니다.
   3. 팝업 창에서 실시간 카메라 영상이 보일 경우, 팝업창의 **화면에 4 개의 점을 마우스 클릭을 통해 사각형 영역을 설정**해야 합니다.
   4. 만약 4 개의 점 이상을 설정할 경우, **앞서 설정한 4 개의 점은 초기화** 됨으로써 다시 영역을 설정할 수 있습니다.
   5. 설정한 영역을 저장하려면, **키보드 Q KEY**를 입력하면 됩니다.

4. ### 신호등 시간 증감값 설정
   1. 프로그램의 우측하단에 표시된 시간 값들을 원하는 값으로 입력하여 변경합니다.
   2. "설정 변경"을 누르면, 값이 저장됨과 동시에 프로그램이 변경한 설정을 따르게 됩니다.

개발 & 실험 환경
----------------------
    OS  : Windows 10 Education 64 Bit (10.0, Build 19042)
    CPU : Intel(R) Core(TM) i5-4570 CPU @ 3.20GHz (4 CPUs), ~3.2GHz
    RAM : DDR3 16GB
    GPU : NVIDIA GeForce GTX 1050 Ti 4GB

FAQ
----------------------
  - Q: 텐서플로우 허브 사용시 SavedModel file does not exist at: [File Location] 라는 오류가 발생합니다.   
    A: [이 페이지](https://github.com/noodles8436/THE-CROSS/issues/41)를 참고하셔서 해결하시기 바랍니다.

Library License
----------------------
```
tensorflow = Apache 2.0   
tensorflow-hub = Apache 2.0   
OpenCV = Apache 2.0   
PyQT5 = GPL v3   
Sphinx = BSD
Numpy = BSD 3-Clause   
sounddevice = MIT   
gdown = MIT   
sphinx_rtd_theme = MIT   
```

개발방법론
----------------------
깃허브 위키페이지에서 ['HOW TO CONTUTE'](https://github.com/noodles8436/THE-CROSS/wiki/How-To-Contribute) 항목을  확인하세요.

도움을 주신 분들
----------------------
***도움을 주신 모든 분들께 진심으로 감사드립니다.***
- 휠체어 대여 : 연세대학교 미래캠퍼스, SW중심대학사업단 
- 평가 및 조언 : 연세대학교 미래캠퍼스 손정우 교수님
- 실험에 사용되는 영상 촬영 도움 : 이승우, 이재규, 신동휘
- 조언 : 송영우
