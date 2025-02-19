**Instructions To Activate Environment**
1. Install python
2. !python -m venv venv
  a. Mac: !source ./venv/bin/activate
  b. Windows: ./venv/Scripts/activate
3. !pip install -r requirements.txt

**Instructions To Use DepthMap**
1. !python depthMap.py
2. follow runtime instructions to insert parameters

this installs the Apple DepthPro HuggingFace model on your computer locally in the repository image_processor folder and model folder
DepthMap.py is slow, the first download will take about 1 minute, and subsequent runs will take about 30 seconds each

**Instructions To Use RotateImage.py**

1. Use DepthMap to generate the depthmap input
2. !python rotateImage.py
3. follow runtime instructions to insert parameters
