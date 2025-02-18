**Instructions To Use DepthMap**

1. Install python
2. !python -m venv venv
  a. Mac: !source ./venv/bin/activate
  b. Windows: ./venv/Scripts/activate
3. !pip install -r requirements.txt
4. !python ./depthMap.py
5. The output is depthmap.jpg

**Warning**... this installs the Apple DepthPro HuggingFace model on your computer locally in the repository image_processor folder and model folder
DepthMap.py is slow, the first download will take about 1 minute, and subsequent runs will take about 30 seconds each

**Instructions To Use Depth2Normal.py**

1. Use DepthMap to generate the depthmap input
2. !python depth2normal.py --input depthmap.jpg
3. The output is normal_map.png
