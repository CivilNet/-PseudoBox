FROM gemfield/deepvac:10.2-cudnn7-runtime-ubuntu18.04
LABEL maintainer "Gemfield <gemfield@civilnet.cn>"
RUN apt-get update && apt-get install -y vim libsm6 libxrender1 libxext6 python3-setuptools ffmpeg nodejs npm
RUN pip3 --no-cache-dir install -i https://pypi.tuna.tsinghua.edu.cn/simple/ requests-toolbelt requests

#COPY face_det.deepvac /gemfield/libdeepvac/install/lib/deepvac/
#COPY faceid.deepvac.so /gemfield/libdeepvac/install/lib/deepvac/

COPY . /root/codes/
WORKDIR /root/codes
RUN npm install


