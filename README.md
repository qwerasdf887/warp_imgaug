# **warp imgaug**  
將imgaug用python整合，可以透過設定檔調整所需的augmentation function。  
參數採用uniform方式選取，所以某些增強方式也有機率不改變圖像。  
相似的augmentation method會隨機挑選一種。  
目前沒有加入會影響顏色的增強方式，若需要加入可自行依照邏輯新增。  
相關詳細用法請參閱[imgaug](https://imgaug.readthedocs.io/en/latest/index.html)  
[run_test](https://github.com/qwerasdf887/wrap_imgaug/blob/master/run_test.ipynb)有些用法的demo。

# **類別細分**  
+ Noise：AddElementwise、GaussianNoise、LaplaceNoise、MultiplyElementwise  
+ bright：MultiplyAndAddToBrightness、GammaContrast、SigmoidContrast、LogContrast、LinearContrast、HistogramEqualization  
+ blur：GaussianBlur、AverageBlur、MedianBlur  
+ geometric：Scale、Translate、Rotate、ShearX  
+ another：MotionBlur(模擬移動模糊)、JpegCompression(Jpeg壓縮損失)、Fliplr、Flipud  
其中針對`Noise`與`blur`會擇一選擇，因為blur也算是一種denoise方法。  
(Noise or blur)、bright、geometric在有增強的情況下隨機挑`1~Max`個，並且順序隨機。  
another function每個皆為**獨立機率**增強並且機率設定為`50%`。  